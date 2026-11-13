from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)

from models.models import db, User
from security.access_control import _log

auth_bp = Blueprint("auth", __name__)


def redirect_by_role(user):
    """Redirect users according to their assigned role."""

    if user.role and user.role.name == "Admin":
        return redirect(url_for("admin.dashboard"))

    return redirect(url_for("staff.dashboard"))


@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect_by_role(current_user)

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        user = User.query.filter_by(username=username).first()

        if not user or not user.check_password(password):
            _log(
                None,
                "LOGIN",
                "FAILED",
                details=f"Failed login for '{username}'"
            )

            flash("Invalid username or password.", "danger")
            return render_template("login.html")

        if not user.is_active:
            _log(
                user.id,
                "LOGIN",
                "BLOCKED",
                details="Inactive account"
            )

            flash("Account disabled. Contact administrator.", "danger")
            return render_template("login.html")

        login_user(user, remember=False)

        user.last_login = datetime.utcnow()
        db.session.commit()

        _log(user.id, "LOGIN", "SUCCESS")

        flash(f"Welcome, {user.full_name}!", "success")

        return redirect_by_role(user)

    return render_template("login.html")


@auth_bp.route("/logout")
@login_required
def logout():

    _log(current_user.id, "LOGOUT", "SUCCESS")

    logout_user()

    flash("You have been logged out.", "info")

    return redirect(url_for("auth.login"))