
from datetime import date
import uuid

from flask import Flask, jsonify, render_template
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from sqlalchemy import text

from config import Config
from models.models import db, Role, User, Patient


# =====================================================
# FLASK EXTENSIONS
# =====================================================

login_manager = LoginManager()
csrf = CSRFProtect()


# =====================================================
# APPLICATION FACTORY
# =====================================================

def create_app():

    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static"
    )

    app.config.from_object(Config)

    # Validate essential configuration
    if not app.config.get("SQLALCHEMY_DATABASE_URI"):
        raise RuntimeError("DATABASE_URL is missing in .env")

    if not app.config.get("ENCRYPTION_KEY"):
        raise RuntimeError(
            "FERNET_KEY or ENCRYPTION_KEY is missing in .env"
        )

    # Initialize database
    db.init_app(app)

    # Initialize authentication
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "warning"

    # Initialize CSRF protection
    csrf.init_app(app)

    # =================================================
    # USER SESSION LOADER
    # =================================================

    @login_manager.user_loader
    def load_user(user_id):

        try:
            return db.session.get(User, int(user_id))

        except (ValueError, TypeError):
            return None

    # =================================================
    # REGISTER BLUEPRINTS
    # =================================================

    from routes.auth import auth_bp
    from routes.admin import admin_bp
    from routes.patients import patients_bp
    from routes.security import security_bp
    from routes.staff import staff_bp

    app.register_blueprint(auth_bp)

    # Admin dashboard URL: /dashboard/
    app.register_blueprint(
        admin_bp,
        url_prefix="/dashboard"
    )

    app.register_blueprint(patients_bp)
    app.register_blueprint(security_bp)
    app.register_blueprint(staff_bp)

    # =================================================
    # PUBLIC HOMEPAGE
    # =================================================

    @app.route("/")
    def home():
        return render_template("home.html")

    # =================================================
    # HEALTH CHECK
    # =================================================

    @app.route("/health")
    def health():

        try:
            db.session.execute(text("SELECT 1"))

            return jsonify(
                status="healthy",
                database="connected",
                application="MediShield AI"
            ), 200

        except Exception:

            db.session.rollback()

            return jsonify(
                status="unhealthy",
                database="disconnected"
            ), 503

    # =================================================
    # ERROR HANDLERS
    # =================================================

    @app.errorhandler(403)
    def forbidden(error):
        return "403 - Access Denied", 403

    @app.errorhandler(404)
    def page_not_found(error):
        return "404 - Page Not Found", 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return "500 - Internal Server Error", 500

    # =================================================
    # INITIALIZE DEMO DATA
    # =================================================

    with app.app_context():
        init_demo_data()

    return app


# =====================================================
# DEMO DATA INITIALIZATION
# =====================================================

def init_demo_data():

    """
    Create synthetic demo patients independently
    of existing user accounts.

    Existing users and patients are preserved.
    """

    from security.encryption import encrypt_field

    # -------------------------------------------------
    # CHECK EXISTING PATIENTS
    # -------------------------------------------------

    if Patient.query.count() > 0:

        print("[INFO] Existing patients found.")
        print("[INFO] Skipping patient initialization.")

        return

    # -------------------------------------------------
    # FIND EXISTING ADMIN USER
    # -------------------------------------------------

    admin_user = User.query.filter_by(
        username="admin"
    ).first()

    if admin_user is None:

        raise RuntimeError(
            "Admin account not found. "
            "Create an admin account before initializing patients."
        )

    # -------------------------------------------------
    # SYNTHETIC PATIENT DATA
    # -------------------------------------------------

    demo_patients = [

        (
            "John", "Doe", date(1985, 4, 12), "Male",
            "555-0101", "123 Main St", "123-45-6789",
            "Hypertension, no known allergies.",
            "Essential hypertension",
            "Lisinopril 10mg daily",
            "Normal CBC"
        ),

        (
            "Mary", "Johnson", date(1978, 9, 3), "Female",
            "555-0102", "45 Oak Ave", "987-65-4321",
            "Type 2 diabetes",
            "T2DM",
            "Metformin 500mg BID",
            "Elevated HbA1c"
        ),

        (
            "Ravi", "Patel", date(1992, 1, 28), "Male",
            "555-0103", "88 Elm Rd", "111-22-3333",
            "Asthma since childhood",
            "Mild persistent asthma",
            "Albuterol PRN",
            "Spirometry normal"
        ),

        (
            "Anna", "Garcia", date(1965, 12, 9), "Female",
            "555-0104", "22 Pine St", "444-55-6666",
            "Post-op recovery",
            "Cholecystectomy follow-up",
            "Ibuprofen 400mg PRN",
            "WBC normal"
        ),

        (
            "Tom", "Chen", date(2000, 6, 15), "Male",
            "555-0105", "77 Cedar Ln", "777-88-9999",
            "No significant history",
            "Routine checkup",
            "None",
            "All values normal"
        )

    ]

    # -------------------------------------------------
    # ENCRYPT AND STORE PATIENT RECORDS
    # -------------------------------------------------

    try:

        for (
            first_name,
            last_name,
            dob,
            gender,
            phone,
            address,
            ssn,
            history,
            diagnosis,
            prescriptions,
            lab_reports
        ) in demo_patients:

            patient = Patient(

                patient_uuid=str(uuid.uuid4()),

                first_name=first_name,
                last_name=last_name,

                date_of_birth=dob,
                gender=gender,

                phone=phone,
                address=address,

                # Encrypted sensitive information
                encrypted_ssn=encrypt_field(ssn),

                encrypted_medical_history=encrypt_field(
                    history
                ),

                encrypted_diagnosis=encrypt_field(
                    diagnosis
                ),

                encrypted_prescriptions=encrypt_field(
                    prescriptions
                ),

                encrypted_lab_reports=encrypt_field(
                    lab_reports
                ),

                created_by=admin_user.id
            )

            db.session.add(patient)

        db.session.commit()

        print("[OK] Five synthetic patients created.")
        print("[OK] Existing users preserved.")
        print("[OK] Sensitive patient fields encrypted.")

    except Exception:

        db.session.rollback()

        raise


# =====================================================
# RUN APPLICATION
# =====================================================

if __name__ == "__main__":

    app = create_app()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=app.config.get("DEBUG", True)
    )
