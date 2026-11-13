# MediShield AI
### Intelligent Healthcare Data Privacy and Unauthorized Access Detection System

**MediShield AI** is an intelligent healthcare data privacy and security system designed to protect sensitive patient information through role-based access control, data encryption, access monitoring, and AI-based anomaly detection.

## 1. Problem Statement

Healthcare applications store sensitive patient information, including medical records and personal details. Unauthorized access, improper data handling, and security threats can expose confidential information.

MediShield AI aims to improve healthcare data security by providing controlled access, protecting patient information, and identifying suspicious activities.

## 2. Project Objectives

- Protect sensitive healthcare information.
- Implement role-based access control.
- Secure patient data using encryption.
- Monitor user activities through security logs.
- Identify suspicious activities using AI-based detection.
- Provide a centralized healthcare security dashboard.

## 3. Key Features

- **User Authentication:** Secure login functionality.
- **Role-Based Access Control:** Different access permissions for Admin, Doctor, Nurse, Receptionist, and Lab Technician.
- **Patient Management:** Manage and view patient records according to user permissions.
- **Data Encryption:** Protect sensitive healthcare information.
- **Data Masking:** Restrict exposure of confidential information.
- **Security Monitoring:** Maintain access logs and security alerts.
- **AI-Based Detection:** Analyze healthcare-related data for suspicious or anomalous patterns.
- **Dashboard:** View system information and security activities.

## 4. Technologies Used

| Component | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python, Flask |
| Database | MySQL |
| Database Management | phpMyAdmin |
| Machine Learning | Scikit-learn |
| Data Processing | Pandas, NumPy |
| Encryption | Python Cryptography |
| Development Environment | VS Code, XAMPP |

## 5. Project Structure

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

## 6. Installation and Setup

### Requirements

- Python 3.11 or later
- XAMPP
- MySQL
- Git

### Step 1: Clone the repository

```bash
git clone https://github.com/Tharika18/MediShield-AI.git
cd MediShield-AI
```

### Step 2: Create a virtual environment

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Start XAMPP

Start Apache and MySQL using the XAMPP Control Panel or:

```bash
sudo /opt/lampp/lampp start
```

### Step 5: Configure the database

1. Open phpMyAdmin.
2. Create the database named `medishield_ai`.
3. Import `database/schema.sql`.
4. Import `database/seed.sql` if sample data is required.

### Step 6: Configure environment variables

Create a local `.env` file in the project root.

Configure the required values using the variable names expected by `config.py`, including:

- `SECRET_KEY`
- `DATABASE_URL`
- `ENCRYPTION_KEY` (or `FERNET_KEY`)

Use your own secure values. Never upload your `.env` file or actual encryption keys to GitHub.

### Step 7: Run the application

```bash
python3 app.py
```

Open the application in your browser:

```text
http://127.0.0.1:5000
```

## 7. Security Features

MediShield AI focuses on healthcare data protection through:

- Authentication and authorization.
- Role-based permissions.
- Encryption of sensitive information.
- Controlled access to patient records.
- Security activity monitoring.
- Suspicious activity detection.

## 8. AI-Based Detection

The project includes machine learning components for analyzing healthcare-related data and identifying anomalous patterns using trained models.

The AI engine contains prediction and training modules along with saved model files.

## 9. Future Enhancements

- Advanced real-time threat detection.
- Improved anomaly detection models.
- Enhanced security analytics.
- Additional healthcare system integrations.
- More comprehensive audit and reporting features.

## 10. Repository

**GitHub:** https://github.com/Tharika18/MediShield-AI

---

**Project Name:** MediShield AI  
**Domain:** Artificial Intelligence and Healthcare Cybersecurity  
**Project Type:** Intelligent Healthcare Data Privacy and Unauthorized Access Detection System