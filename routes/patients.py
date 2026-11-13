import uuid
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from models.models import db, Patient
from security.encryption import encrypt_field, decrypt_field, mask
from security.access_control import requires_role, log_access
from ai_engine.predict import predict_risk
from models.models import SecurityAlert

patients_bp = Blueprint("patients", __name__)

PAGE_SIZE = 10


def _maybe_alert(user_id, action, patient_id):
    risk_score, is_anomaly, reasons, feats = predict_risk(user_id, action, patient_id)
    log = log_access(action, "SUCCESS", details=None, patient_id=patient_id, risk_score=risk_score)
    if is_anomaly:
        alert = SecurityAlert(
            log_id=log.id,
            user_id=user_id,
            alert_type="SUSPICIOUS_ACCESS",
            risk_score=risk_score,
            reason="; ".join(reasons),
        )
        db.session.add(alert)
        db.session.commit()


@patients_bp.route("/patients")
@login_required
@requires_role("Admin", "Doctor", "Nurse", "Receptionist", "Lab Technician")
def list_patients():
    q = request.args.get("q", "").strip()
    page = max(1, int(request.args.get("page", 1)))

    query = Patient.query
    if q:
        like = f"%{q}%"
        query = query.filter(
            db.or_(Patient.first_name.ilike(like), Patient.last_name.ilike(like))
        )
    total = query.count()
    patients = (
        query.order_by(Patient.id.desc())
        .offset((page - 1) * PAGE_SIZE)
        .limit(PAGE_SIZE)
        .all()
    )
    total_pages = max(1, (total + PAGE_SIZE - 1) // PAGE_SIZE)

    _maybe_alert(current_user.id, "LIST_PATIENTS", None)

    return render_template(
        "patients.html",
        patients=patients,
        q=q,
        page=page,
        total_pages=total_pages,
        total=total,
    )


@patients_bp.route("/patients/<int:pid>")
@login_required
@requires_role("Admin", "Doctor", "Nurse", "Receptionist", "Lab Technician")
def view_patient(pid):
    p = Patient.query.get_or_404(pid)
    role = current_user.role.name

    _maybe_alert(current_user.id, "VIEW_PATIENT", pid)

    # Field-level disclosure is enforced on the server.
    # SSN is restricted to Admin; it is masked for every staff role.
    ssn_value = decrypt_field(p.encrypted_ssn)
    ssn = ssn_value if role == "Admin" else mask(ssn_value)

    history = diagnosis = prescriptions = lab_reports = "*** restricted ***"
    if role == "Admin":
        history = decrypt_field(p.encrypted_medical_history)
        diagnosis = decrypt_field(p.encrypted_diagnosis)
        prescriptions = decrypt_field(p.encrypted_prescriptions)
        lab_reports = decrypt_field(p.encrypted_lab_reports)
    elif role == "Doctor":
        history = decrypt_field(p.encrypted_medical_history)
        diagnosis = decrypt_field(p.encrypted_diagnosis)
        prescriptions = decrypt_field(p.encrypted_prescriptions)
        lab_reports = decrypt_field(p.encrypted_lab_reports)
    elif role == "Nurse":
        history = decrypt_field(p.encrypted_medical_history)
        diagnosis = decrypt_field(p.encrypted_diagnosis)
        prescriptions = decrypt_field(p.encrypted_prescriptions)
        lab_reports = decrypt_field(p.encrypted_lab_reports)
    elif role == "Lab Technician":
        lab_reports = decrypt_field(p.encrypted_lab_reports)

    masked = role != "Admin"

    return render_template(
        "patient_view.html",
        p=p,
        ssn=ssn,
        history=history,
        diagnosis=diagnosis,
        prescriptions=prescriptions,
        lab_reports=lab_reports,
        masked=masked,
    )


@patients_bp.route("/patients/new", methods=["GET", "POST"])
@login_required
@requires_role("Admin", "Doctor", "Receptionist")
def new_patient():
    if request.method == "POST":
        try:
            first_name = request.form["first_name"].strip()
            last_name = request.form["last_name"].strip()
            dob = datetime.strptime(request.form["date_of_birth"], "%Y-%m-%d").date()
            gender = request.form["gender"]
            phone = request.form.get("phone", "").strip()
            address = request.form.get("address", "").strip()
            role = current_user.role.name if current_user.role else ""
            # Reception staff may register demographics only.
            if role == "Receptionist":
                ssn = history = diagnosis = prescriptions = lab_reports = ""
            else:
                ssn = request.form.get("ssn", "").strip()
                history = request.form.get("medical_history", "").strip()
                diagnosis = request.form.get("diagnosis", "").strip()
                prescriptions = request.form.get("prescriptions", "").strip()
                lab_reports = request.form.get("lab_reports", "").strip()

            if not first_name or not last_name:
                raise ValueError("First and last name required.")

            p = Patient(
                patient_uuid=str(uuid.uuid4()),
                first_name=first_name,
                last_name=last_name,
                date_of_birth=dob,
                gender=gender,
                phone=phone,
                address=address,
                encrypted_ssn=encrypt_field(ssn),
                encrypted_medical_history=encrypt_field(history),
                encrypted_diagnosis=encrypt_field(diagnosis),
                encrypted_prescriptions=encrypt_field(prescriptions),
                encrypted_lab_reports=encrypt_field(lab_reports),
                created_by=current_user.id,
            )
            db.session.add(p)
            db.session.commit()
            log_access("CREATE_PATIENT", "SUCCESS", patient_id=p.id)
            flash("Patient created successfully.", "success")
            return redirect(url_for("patients.list_patients"))
        except Exception as e:
            flash(f"Error: {e}", "danger")

    return render_template("patient_form.html", p=None)