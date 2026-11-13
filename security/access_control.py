
from functools import wraps

from flask import abort, request
from flask_login import current_user

from models.models import db, AccessLog


def _log(user_id, action, status, details=None, patient_id=None):
    """Create an audit log entry safely."""
    log = AccessLog(
        user_id=user_id,
        patient_id=patient_id,
        action=action,
        status=status,
        ip_address=request.remote_addr,
        user_agent=(
            request.user_agent.string[:255]
            if request.user_agent else None
        ),
        details=details,
    )

    try:
        db.session.add(log)
        db.session.commit()
        return log
    except Exception:
        db.session.rollback()
        raise


def requires_role(*role_names):
    """Enforce backend role-based access control."""

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):

            if not current_user.is_authenticated:
                abort(401)

            user_role = (
                current_user.role.name
                if current_user.role else None
            )

            if user_role not in role_names:
                _log(
                    user_id=current_user.id,
                    action=f"ACCESS_DENIED:{fn.__name__}",
                    status="BLOCKED",
                    details=f"Required roles: {', '.join(role_names)}",
                )
                abort(403)

            return fn(*args, **kwargs)

        return wrapper

    return decorator


def log_access(
    action,
    status="SUCCESS",
    details=None,
    patient_id=None,
    risk_score=None,
):
    """Record user activity and optional AI risk score."""

    user_id = (
        current_user.id
        if current_user.is_authenticated
        else None
    )

    log = _log(
        user_id=user_id,
        action=action,
        status=status,
        details=details,
        patient_id=patient_id,
    )

    if risk_score is not None:
        try:
            log.risk_score = risk_score
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

    return log
