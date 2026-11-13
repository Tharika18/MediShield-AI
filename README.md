# MediShield AI
### Intelligent Healthcare Data Privacy and Unauthorized Access Detection System

<p align="center">
  <strong>AI-Powered Healthcare Data Protection and Security Monitoring</strong>
</p>

## 1. Project Overview

**MediShield AI** is an intelligent healthcare data privacy and security system developed to protect sensitive patient information and monitor suspicious activities in healthcare environments.

The system combines role-based access control, data encryption, patient record management, security monitoring and machine learning-based anomaly detection.

It provides different access permissions for healthcare personnel, helping protect confidential patient information and improve healthcare data security.

## 2. Problem Statement

Healthcare applications maintain sensitive information such as patient details, medical records and clinical data.

Unauthorized access, improper handling of confidential information and suspicious activities can expose patient data to security risks.

MediShield AI addresses these challenges by providing controlled access to healthcare records, data protection mechanisms and security monitoring.

## 3. Project Objectives

- Protect sensitive healthcare information.
- Implement role-based access control.
- Secure confidential patient information through encryption.
- Provide controlled access to patient records.
- Monitor user activities through security logs.
- Identify suspicious patterns using machine learning.
- Provide centralized security monitoring through dashboards.

## 4. Key Features

### User Authentication
- User login and authentication.
- Role-based user access.
- Different dashboards based on user roles.

### Patient Management
- Add and manage patient information.
- View patient records.
- Control access to confidential healthcare information.

### Data Privacy and Security
- Encryption of sensitive information.
- Data masking.
- Role-based permissions.
- Controlled access to healthcare records.

### Security Monitoring
- Access activity logs.
- Security alerts.
- Monitoring of user activities.
- Security event history.

### AI-Based Anomaly Detection
- Machine learning-based healthcare data analysis.
- HL7 message anomaly prediction.
- Saved trained model files.
- Training and prediction modules.

## 5. User Roles

MediShield AI supports five user roles:

| Role | Responsibilities |
|---|---|
| Admin | Manage users, monitor security and manage system activities |
| Doctor | Access permitted patient information and clinical records |
| Nurse | Access patient information according to assigned permissions |
| Receptionist | Handle permitted patient and administrative information |
| Lab Technician | Access permitted laboratory-related information |

Access permissions are controlled through the role and permission management system.

## 6. Technologies Used

| Component | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python |
| Web Framework | Flask |
| Database | MySQL / MariaDB |
| Database Management | phpMyAdmin |
| Machine Learning | Scikit-learn |
| Data Processing | Pandas, NumPy |
| Model Storage | Pickle, Joblib |
| Encryption | Python Cryptography |
| Development Environment | Visual Studio Code |
| Local Server | XAMPP |

## 7. Project Architecture

The project is organized into separate modules for application management, database operations, security, AI processing and user interfaces.

```text
MediShield_AI/
│
├── ai_engine/
│   ├── predict.py
│   ├── train.py
│   ├── train_hl7.py
│   └── saved_models/
│
├── database/
│   ├── schema.sql
│   └── seed.sql
│
├── datasets/
│   └── emr/
│
├── models/
│   └── models.py
│
├── routes/
│   ├── admin.py
│   ├── auth.py
│   ├── patients.py
│   ├── security.py
│   └── staff.py
│
├── security/
│   ├── access_control.py
│   └── encryption.py
│
├── static/
│   ├── css/
│   └── js/
│
├── templates/
│
├── app.py
├── config.py
├── requirements.txt
├── .gitignore
└── README.md
```

## 8. AI and Machine Learning Modules

The AI engine contains training and prediction components for healthcare-related anomaly analysis.

### Included components

- `train.py` – Model training module.
- `train_hl7.py` – HL7 anomaly model training.
- `predict.py` – Prediction functionality.
- `model.pkl` – Saved model artifact.
- `hl7_anomaly_model.joblib` – Saved HL7 model artifact.
- `training_results.json` – Stored training evaluation results.

The current HL7 anomaly model uses message-type information for classification. Its predictions are intended as an experimental anomaly detection aid and should not be treated as a complete security verification system.

## 9. Dataset

The project includes healthcare-related datasets and HL7 message data under:

`datasets/emr/`

The dataset folder includes:

- Patient information data.
- Appointment data.
- Encounter data.
- Observation data.
- Practitioner data.
- Normal and anomalous HL7 payload data.
- HL7 database files.

The included dataset documentation identifies the healthcare records as generated datasets.

Refer to `datasets/emr/README.md` and `datasets/emr/LICENSE` for dataset documentation and licensing information.

## 10. Installation and Setup

### System Requirements

- Python 3.11 or later.
- XAMPP.
- MySQL or MariaDB.
- Git.
- A modern web browser.

### Step 1: Clone the Repository

```bash
git clone https://github.com/Tharika18/MediShield-AI.git
```

Move into the project directory:

```bash
cd MediShield-AI
```

### Step 2: Create a Virtual Environment

```bash
python3 -m venv venv
```

Activate the virtual environment:

**Linux:**

```bash
source venv/bin/activate
```

**Windows:**

```bash
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Start XAMPP

Start Apache and MySQL using the XAMPP Control Panel.

For Linux:

```bash
sudo /opt/lampp/lampp start
```

### Step 5: Create the Database

1. Open phpMyAdmin.
2. Create a database named `medishield_ai`.
3. Select the newly created database.
4. Import `database/schema.sql`.
5. Import `database/seed.sql`.

The seed file provides the database's initial seed data. The six existing development user accounts listed below are from the development database and are not automatically guaranteed to be created by these SQL files.

### Step 6: Configure Environment Variables

Create a local `.env` file in the project root.

Configure the environment variables expected by `config.py`:

```env
SECRET_KEY=your_own_secure_secret
DATABASE_URL=your_database_connection_string
ENCRYPTION_KEY=your_own_fernet_key
```

Use a valid database connection string for your MySQL setup and generate your own secure application and encryption keys.

Alternatively, configure `FERNET_KEY` if your configuration uses that variable.

**Security Warning:**
- Never upload `.env` to GitHub.
- Never share actual encryption keys or secret values.
- Use separate credentials for each installation.

### Step 7: Run the Application

Activate the virtual environment and execute:

```bash
python3 app.py
```

### Step 8: Open the Application

Open your browser and visit:

```text
http://127.0.0.1:5000
```

## 11. Demo Login Accounts

The following accounts are present in the current development database.

| Role | Username | Email |
|---|---|---|
| Admin | `admin` | admin@medishield.local |
| Doctor 1 | `dr_smith` | smith@medishield.local |
| Doctor 2 | `Radhika` | radhi@gmail.com |
| Nurse | `nurse_kim` | kim@medishield.local |
| Receptionist | `reception` | reception@medishield.local |
| Lab Technician | `labtech` | lab@medishield.local |

### Login Instructions

1. Start the Flask application.
2. Open `http://127.0.0.1:5000`.
3. Enter the assigned username and password.
4. Access the dashboard according to the user's role.

**Note:** Passwords are not published in this public repository. Demo passwords should be provided separately through a private channel. These development accounts must be provisioned on a fresh installation before they can be used there.

## 12. Security Implementation

MediShield AI includes the following security-related components:

- Authentication and user management.
- Role-based access control.
- Permission management.
- Encryption functionality.
- Data masking.
- Access logging.
- Security alerts.
- Anomaly prediction.

These mechanisms are intended to improve the confidentiality and controlled handling of healthcare information.

## 13. Future Enhancements

- Advanced real-time unauthorized access detection.
- Improved machine learning model performance.
- Enhanced security analytics and reporting.
- Additional healthcare data integrations.
- More comprehensive anomaly detection.
- Improved deployment and scalability.

## 14. GitHub Repository

**Project Repository:**

https://github.com/Tharika18/MediShield-AI

## 15. Project Information

| Field | Details |
|---|---|
| Project Name | MediShield AI |
| Domain | Artificial Intelligence and Healthcare Cybersecurity |
| Project Type | Healthcare Data Privacy and Security System |
| Backend | Python Flask |
| Database | MySQL |
| AI Technology | Machine Learning |

---

**MediShield AI – Protecting Healthcare Data Through Intelligent Security.**