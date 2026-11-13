from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.security import check_password_hash
from models.models import db, User, Patient, AccessLog, SecurityAlert
from security.access_control import log_access

staff_bp = Blueprint("staff", __name__)

STAFF_ROLES = ("Doctor", "Nurse", "Receptionist", "Lab Technician")


@staff_bp.route("/staff/dashboard")
@login_required
def dashboard():
    role = current_user.role.name if current_user.role else ""
    if role not in STAFF_ROLES:
        return redirect(url_for("admin.dashboard"))

    total_patients = Patient.query.count()
    recent_patients = Patient.query.order_by(Patient.created_at.desc()).limit(5).all()
    recent_activity = AccessLog.query.filter_by(user_id=current_user.id).order_by(
        AccessLog.timestamp.desc()
    ).limit(5).all()

    # Counts are limited to information the role is permitted to use.
    stats = {"patients": total_patients}
    if role in ("Doctor", "Nurse"):
        stats["clinical"] = total_patients
    elif role == "Receptionist":
        stats["registrations"] = Patient.query.filter_by(created_by=current_user.id).count()
    elif role == "Lab Technician":
        stats["lab_records"] = total_patients

    log_access("OPEN_STAFF_DASHBOARD", "SUCCESS", details=f"Role: {role}")
    return render_template(
        "staff_dashboard.html",
        role=role,
        stats=stats,
        recent_patients=recent_patients,
        recent_activity=recent_activity,
    )


@staff_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "POST":
        action = request.form.get("action", "profile")

        if action == "password":
            current_password = request.form.get("current_password", "")
            new_password = request.form.get("new_password", "")
            confirm_password = request.form.get("confirm_password", "")

            if not current_user.check_password(current_password):
                flash("Current password is incorrect.", "danger")
            elif len(new_password) < 8:
                flash("New password must contain at least 8 characters.", "danger")
            elif new_password != confirm_password:
                flash("New passwords do not match.", "danger")
            else:
                current_user.set_password(new_password)
                db.session.commit()
                log_access("CHANGE_PASSWORD", "SUCCESS")
                flash("Password changed successfully.", "success")
                return redirect(url_for("staff.profile"))

        else:
            full_name = request.form.get("full_name", "").strip()
            email = request.form.get("email", "").strip().lower()

            if not full_name or not email:
                flash("Name and email are required.", "danger")
            elif User.query.filter(User.email == email, User.id != current_user.id).first():
                flash("This email is already used by another account.", "danger")
            else:
                current_user.full_name = full_name
                current_user.email = email
                db.session.commit()
                log_access("UPDATE_PROFILE", "SUCCESS")
                flash("Profile updated successfully.", "success")
                return redirect(url_for("staff.profile"))

    return render_template("profile.html")
