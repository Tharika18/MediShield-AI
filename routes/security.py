
from datetime import datetime

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import login_required, current_user

from models.models import db, AccessLog, SecurityAlert
from security.access_control import requires_role


security_bp = Blueprint("security", __name__)

PAGE_SIZE = 20


# =====================================================
# SECURITY AUDIT LOGS
# =====================================================

@security_bp.route("/logs")
@login_required
@requires_role("Admin")
def logs():

    # Safely read page number
    try:
        page = max(1, int(request.args.get("page", 1)))
    except (ValueError, TypeError):
        page = 1

    query = AccessLog.query

    q = request.args.get("q", "").strip()
    status = request.args.get("status", "").strip().upper()


    # Search by action
    if q:
        query = query.filter(
            AccessLog.action.ilike(f"%{q}%")
        )


    # Filter by status
    if status in ("SUCCESS", "BLOCKED", "FAILED"):
        query = query.filter(
            AccessLog.status == status
        )
    else:
        status = ""


    total = query.count()

    total_pages = max(
        1,
        (total + PAGE_SIZE - 1) // PAGE_SIZE
    )

    # Prevent invalid page numbers
    page = min(page, total_pages)

    log_entries = (
        query
        .order_by(AccessLog.timestamp.desc())
        .offset((page - 1) * PAGE_SIZE)
        .limit(PAGE_SIZE)
        .all()
    )


    return render_template(
        "security_logs.html",
        logs=log_entries,
        page=page,
        total_pages=total_pages,
        total=total,
        q=q,
        status=status
    )


# =====================================================
# SECURITY ALERTS
# =====================================================

@security_bp.route("/alerts")
@login_required
@requires_role("Admin")
def alerts():

    # Safely read page number
    try:
        page = max(1, int(request.args.get("page", 1)))
    except (ValueError, TypeError):
        page = 1

    q = request.args.get("q", "").strip()

    # Display all alerts, newest first
    query = SecurityAlert.query

    if q:
        query = query.filter(
            SecurityAlert.alert_type.ilike(f"%{q}%")
        )

    total = query.count()

    total_pages = max(
        1,
        (total + PAGE_SIZE - 1) // PAGE_SIZE
    )

    page = min(page, total_pages)

    alert_entries = (
        query
        .order_by(SecurityAlert.created_at.desc())
        .offset((page - 1) * PAGE_SIZE)
        .limit(PAGE_SIZE)
        .all()
    )

    return render_template(
        "alerts.html",
        alerts=alert_entries,
        page=page,
        total_pages=total_pages,
        total=total,
        q=q
    )


# =====================================================
# RESOLVE SECURITY ALERT
# =====================================================

@security_bp.route(
    "/alerts/<int:aid>/resolve",
    methods=["POST"]
)
@login_required
@requires_role("Admin")
def resolve_alert(aid):

    alert = db.get_or_404(SecurityAlert, aid)

    if alert.is_resolved:

        flash(
            "This alert has already been resolved.",
            "info"
        )

        return redirect(
            url_for("security.alerts")
        )


    try:

        alert.is_resolved = True
        alert.resolved_by = current_user.id
        alert.resolved_at = datetime.utcnow()

        db.session.commit()

        flash(
            "Security alert marked as resolved successfully.",
            "success"
        )

    except Exception:

        db.session.rollback()

        flash(
            "Unable to resolve the security alert.",
            "danger"
        )


    return redirect(
        url_for("security.alerts")
    )
