
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()


# =====================================================
# ROLE MODEL
# =====================================================

class Role(db.Model):

    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    description = db.Column(db.String(255))

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    users = db.relationship(
        "User",
        back_populates="role",
        lazy=True
    )

    role_permissions = db.relationship(
        "RolePermission",
        back_populates="role",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Role {self.name}>"


# =====================================================
# PERMISSION MODEL
# =====================================================

class Permission(db.Model):

    __tablename__ = "permissions"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    description = db.Column(
        db.String(255)
    )

    role_permissions = db.relationship(
        "RolePermission",
        back_populates="permission",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Permission {self.name}>"


# =====================================================
# ROLE PERMISSION MODEL
# =====================================================

class RolePermission(db.Model):

    __tablename__ = "role_permissions"

    role_id = db.Column(
        db.Integer,
        db.ForeignKey("roles.id", ondelete="CASCADE"),
        primary_key=True
    )

    permission_id = db.Column(
        db.Integer,
        db.ForeignKey("permissions.id", ondelete="CASCADE"),
        primary_key=True
    )

    role = db.relationship(
        "Role",
        back_populates="role_permissions"
    )

    permission = db.relationship(
        "Permission",
        back_populates="role_permissions"
    )


# =====================================================
# USER MODEL
# =====================================================

class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(80),
        unique=True,
        nullable=False,
        index=True
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False,
        index=True
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    full_name = db.Column(
        db.String(120),
        nullable=False
    )

    role_id = db.Column(
        db.Integer,
        db.ForeignKey("roles.id"),
        nullable=False
    )

    is_active = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    last_login = db.Column(
        db.DateTime
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    role = db.relationship(
        "Role",
        back_populates="users"
    )

    created_patients = db.relationship(
        "Patient",
        foreign_keys="Patient.created_by",
        back_populates="creator"
    )

    access_logs = db.relationship(
        "AccessLog",
        foreign_keys="AccessLog.user_id",
        back_populates="user"
    )

    created_alerts = db.relationship(
        "SecurityAlert",
        foreign_keys="SecurityAlert.user_id",
        back_populates="user"
    )

    resolved_alerts = db.relationship(
        "SecurityAlert",
        foreign_keys="SecurityAlert.resolved_by",
        back_populates="resolver"
    )

    def set_password(self, password):

        self.password_hash = generate_password_hash(password)

    def check_password(self, password):

        return check_password_hash(
            self.password_hash,
            password
        )

    @property
    def is_active_user(self):

        return self.is_active

    def __repr__(self):

        return f"<User {self.username}>"


# =====================================================
# PATIENT MODEL
# =====================================================

class Patient(db.Model):

    __tablename__ = "patients"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    patient_uuid = db.Column(
        db.String(36),
        unique=True,
        nullable=False,
        index=True
    )

    first_name = db.Column(
        db.String(100),
        nullable=False
    )

    last_name = db.Column(
        db.String(100),
        nullable=False
    )

    date_of_birth = db.Column(
        db.Date,
        nullable=False
    )

    gender = db.Column(
        db.Enum("Male", "Female", "Other"),
        nullable=False
    )

    phone = db.Column(
        db.String(20)
    )

    address = db.Column(
        db.Text
    )

    encrypted_ssn = db.Column(
        db.Text
    )

    encrypted_medical_history = db.Column(
        db.Text
    )

    encrypted_diagnosis = db.Column(
        db.Text
    )

    encrypted_prescriptions = db.Column(
        db.Text
    )

    encrypted_lab_reports = db.Column(
        db.Text
    )

    created_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="SET NULL")
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    creator = db.relationship(
        "User",
        foreign_keys=[created_by],
        back_populates="created_patients"
    )

    access_logs = db.relationship(
        "AccessLog",
        back_populates="patient"
    )

    def __repr__(self):

        return f"<Patient {self.patient_uuid}>"


# =====================================================
# ACCESS LOG MODEL
# =====================================================

class AccessLog(db.Model):

    __tablename__ = "access_logs"

    id = db.Column(
        db.BigInteger,
        primary_key=True,
        autoincrement=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="SET NULL"),
        index=True
    )

    patient_id = db.Column(
        db.Integer,
        db.ForeignKey("patients.id", ondelete="SET NULL"),
        index=True
    )

    action = db.Column(
        db.String(100),
        nullable=False,
        index=True
    )

    status = db.Column(
        db.Enum("SUCCESS", "BLOCKED", "FAILED"),
        nullable=False,
        index=True
    )

    ip_address = db.Column(
        db.String(45)
    )

    user_agent = db.Column(
        db.String(255)
    )

    details = db.Column(
        db.Text
    )

    risk_score = db.Column(
        db.Float
    )

    timestamp = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True
    )

    user = db.relationship(
        "User",
        foreign_keys=[user_id],
        back_populates="access_logs"
    )

    patient = db.relationship(
        "Patient",
        foreign_keys=[patient_id],
        back_populates="access_logs"
    )

    alerts = db.relationship(
        "SecurityAlert",
        back_populates="log",
        cascade="all, delete-orphan"
    )

    def __repr__(self):

        return f"<AccessLog {self.action} - {self.status}>"


# =====================================================
# SECURITY ALERT MODEL
# =====================================================

class SecurityAlert(db.Model):

    __tablename__ = "security_alerts"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    log_id = db.Column(
        db.BigInteger,
        db.ForeignKey("access_logs.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="SET NULL"),
        index=True
    )

    alert_type = db.Column(
        db.String(50),
        nullable=False,
        index=True
    )

    risk_score = db.Column(
        db.Float,
        nullable=False
    )

    reason = db.Column(
        db.Text,
        nullable=False
    )

    is_resolved = db.Column(
        db.Boolean,
        default=False,
        nullable=False,
        index=True
    )

    resolved_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="SET NULL")
    )

    resolved_at = db.Column(
        db.DateTime
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True
    )

    log = db.relationship(
        "AccessLog",
        foreign_keys=[log_id],
        back_populates="alerts"
    )

    user = db.relationship(
        "User",
        foreign_keys=[user_id],
        back_populates="created_alerts"
    )

    resolver = db.relationship(
        "User",
        foreign_keys=[resolved_by],
        back_populates="resolved_alerts"
    )

    def __repr__(self):

        return f"<SecurityAlert {self.alert_type}>"
 
# =====================================================
# HL7 PREDICTION HISTORY MODEL
# =====================================================

class HL7Prediction(db.Model):

    __tablename__ = "hl7_prediction_history"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True
    )

    message_type = db.Column(
        db.String(20),
        nullable=False
    )

    prediction = db.Column(
        db.String(20),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    user = db.relationship("User")

    def __repr__(self):
        return f"<HL7Prediction {self.message_type}: {self.prediction}>"
