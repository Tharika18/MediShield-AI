
import os
import json
from datetime import datetime, timedelta

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import login_required, current_user
from sqlalchemy import func

from models.models import (
    db,
    User,
    Role,
    Patient,
    AccessLog,
    SecurityAlert,
    HL7Prediction
)

from security.access_control import requires_role


admin_bp = Blueprint("admin", __name__)


# =====================================================
# ADMIN DASHBOARD
# =====================================================

@admin_bp.route("/")
@login_required
@requires_role("Admin")
def dashboard():

    total_users = User.query.count()
    total_patients = Patient.query.count()

    successful_logins = AccessLog.query.filter_by(
        action="LOGIN",
        status="SUCCESS"
    ).count()

    failed_logins = AccessLog.query.filter_by(
        action="LOGIN",
        status="FAILED"
    ).count()

    suspicious_alerts = SecurityAlert.query.filter_by(
        is_resolved=False
    ).count()

    blocked_attempts = AccessLog.query.filter_by(
        status="BLOCKED"
    ).count()

    recent_logs = (
        AccessLog.query
        .order_by(AccessLog.timestamp.desc())
        .limit(10)
        .all()
    )

    recent_alerts = (
        SecurityAlert.query
        .filter_by(is_resolved=False)
        .order_by(SecurityAlert.created_at.desc())
        .limit(5)
        .all()
    )

    today = datetime.utcnow().date()

    labels = []
    ok_series = []
    fail_series = []

    for i in range(6, -1, -1):

        day = today - timedelta(days=i)

        labels.append(day.strftime("%b %d"))

        success_count = (
            AccessLog.query
            .filter(
                func.date(AccessLog.timestamp) == day,
                AccessLog.action == "LOGIN",
                AccessLog.status == "SUCCESS"
            )
            .count()
        )

        failure_count = (
            AccessLog.query
            .filter(
                func.date(AccessLog.timestamp) == day,
                AccessLog.action == "LOGIN",
                AccessLog.status == "FAILED"
            )
            .count()
        )

        ok_series.append(success_count)
        fail_series.append(failure_count)

    alert_data = (
        db.session.query(
            SecurityAlert.alert_type,
            func.count(SecurityAlert.id)
        )
        .group_by(SecurityAlert.alert_type)
        .all()
    )

    alert_types = [
        {
            "label": alert_type,
            "count": count
        }
        for alert_type, count in alert_data
    ]

    return render_template(
        "dashboard.html",
        total_users=total_users,
        total_patients=total_patients,
        successful_logins=successful_logins,
        failed_logins=failed_logins,
        suspicious_alerts=suspicious_alerts,
        blocked_attempts=blocked_attempts,
        recent_logs=recent_logs,
        recent_alerts=recent_alerts,
        chart_labels=labels,
        chart_ok=ok_series,
        chart_fail=fail_series,
        alert_types=alert_types
    )


# =====================================================
# USER MANAGEMENT
# =====================================================

@admin_bp.route("/users", methods=["GET", "POST"])
@login_required
@requires_role("Admin")
def users():

    if request.method == "POST":

        action = request.form.get("action", "").strip()

        if action == "create":

            username = request.form.get("username", "").strip()
            email = request.form.get("email", "").strip().lower()
            full_name = request.form.get("full_name", "").strip()
            password = request.form.get("password", "")

            try:
                role_id = int(request.form.get("role_id", "0"))
            except (ValueError, TypeError):
                role_id = 0

            if not all([username, email, full_name, password, role_id]):

                flash("All fields are required.", "danger")

            elif "@" not in email:

                flash("Please enter a valid email address.", "danger")

            elif len(password) < 8:

                flash("Password must contain at least 8 characters.", "danger")

            elif User.query.filter_by(username=username).first():

                flash("Username already exists.", "danger")

            elif User.query.filter_by(email=email).first():

                flash("Email already in use.", "danger")

            else:

                role = db.session.get(Role, role_id)

                if not role:

                    flash("Invalid role selected.", "danger")

                else:

                    try:

                        new_user = User(
                            username=username,
                            email=email,
                            full_name=full_name,
                            role_id=role_id
                        )

                        new_user.set_password(password)

                        db.session.add(new_user)
                        db.session.commit()

                        flash(
                            f"User '{username}' created successfully.",
                            "success"
                        )

                    except Exception:

                        db.session.rollback()

                        flash(
                            "Unable to create user. Please check the entered details.",
                            "danger"
                        )

        elif action == "toggle":

            try:
                user_id = int(request.form.get("user_id", "0"))
            except (ValueError, TypeError):
                user_id = 0

            user = db.session.get(User, user_id)

            if not user:

                flash("User not found.", "danger")

            elif user.id == current_user.id:

                flash("You cannot disable your own account.", "warning")

            else:

                user.is_active = not user.is_active

                try:

                    db.session.commit()

                    status = "enabled" if user.is_active else "disabled"

                    flash(
                        f"User '{user.username}' {status} successfully.",
                        "success"
                    )

                except Exception:

                    db.session.rollback()
                    flash("Unable to update user status.", "danger")

        else:

            flash("Invalid action requested.", "danger")

        return redirect(url_for("admin.users"))

    all_users = User.query.order_by(User.id.asc()).all()
    roles = Role.query.order_by(Role.id.asc()).all()

    return render_template(
        "users.html",
        users=all_users,
        roles=roles
    )


# =====================================================
# AI MODEL STATUS
# =====================================================

@admin_bp.route("/ai-model")
@login_required
@requires_role("Admin")
def ai_model():

    base_dir = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )

    results_path = os.path.join(
        base_dir,
        "ai_engine",
        "saved_models",
        "training_results.json"
    )

    results = None

    if os.path.exists(results_path):

        try:
            with open(results_path, "r") as file:
                results = json.load(file)

        except (OSError, json.JSONDecodeError):
            flash("Unable to read AI training results.", "danger")

    return render_template(
        "ai_model.html",
        results=results
    )


# =====================================================
# HL7 MESSAGE TYPE VALIDATION
# =====================================================

VALID_HL7_MESSAGE_TYPES = {
    "ADT^A01",
    "ADT^A02",
    "ADT^A03",
    "ADT^A05",
    "ADT^A13",
    "ADT^A28",
    "ADT^A31",
    "ADT^A38",
    "ADT^A40"
}


# =====================================================
# HL7 AI PREDICTION
# =====================================================

@admin_bp.route("/hl7-predict", methods=["GET", "POST"])
@login_required
@requires_role("Admin")
def hl7_predict():

    import joblib
    import pandas as pd

    base_dir = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )

    model_path = os.path.join(
        base_dir,
        "ai_engine",
        "saved_models",
        "hl7_anomaly_model.joblib"
    )

    result = None
    message_type = ""

    if request.method == "POST":

        message_type = request.form.get(
            "msgtype", ""
        ).strip().upper()

        if not message_type:

            flash(
                "Please enter an HL7 message type.",
                "danger"
            )

        else:

            try:

                # Validate the message type before AI prediction
                if message_type not in VALID_HL7_MESSAGE_TYPES:

                    label = "Anomaly"

                    result = {
                        "label": "Anomalous / Suspicious",
                        "is_anomaly": True
                    }

                    history = HL7Prediction(
                        user_id=current_user.id,
                        message_type=message_type,
                        prediction=label
                    )

                    db.session.add(history)
                    db.session.commit()

                    flash(
                        "Unknown HL7 message type detected. "
                        "Please investigate this input.",
                        "danger"
                    )

                elif not os.path.exists(model_path):

                    flash(
                        "Trained HL7 model not found.",
                        "danger"
                    )

                else:

                    model = joblib.load(model_path)

                    sample = pd.DataFrame({
                        "MSGTYPE": [message_type]
                    })

                    prediction = int(model.predict(sample)[0])

                    label = (
                        "Anomaly"
                        if prediction == 1
                        else "Normal"
                    )

                    result = {
                        "label": label,
                        "is_anomaly": prediction == 1
                    }

                    history = HL7Prediction(
                        user_id=current_user.id,
                        message_type=message_type,
                        prediction=label
                    )

                    db.session.add(history)
                    db.session.commit()

                    flash(
                        "Prediction saved successfully.",
                        "success"
                    )

            except Exception as error:

                db.session.rollback()

                flash(
                    f"Prediction failed: {error}",
                    "danger"
                )

    return render_template(
        "hl7_predict.html",
        result=result,
        message_type=message_type
    )


# =====================================================
# HL7 PREDICTION HISTORY
# =====================================================

@admin_bp.route("/prediction-history")
@login_required
@requires_role("Admin")
def prediction_history():

    total_predictions = HL7Prediction.query.count()

    normal_count = HL7Prediction.query.filter_by(
        prediction="Normal"
    ).count()

    anomaly_count = HL7Prediction.query.filter_by(
        prediction="Anomaly"
    ).count()

    history = HL7Prediction.query.order_by(
        HL7Prediction.created_at.desc()
    ).all()

    return render_template(
        "prediction_history.html",
        total_predictions=total_predictions,
        normal_count=normal_count,
        anomaly_count=anomaly_count,
        history=history
    )
