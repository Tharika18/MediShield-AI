# MediShield AI

## Intelligent Healthcare Data Privacy and Unauthorized Access Detection System

**AI-Powered Healthcare Data Protection and Security Monitoring**

---

## 1. Project Overview

**MediShield AI** is an intelligent healthcare data privacy and security system developed to protect sensitive patient information and monitor suspicious activities in healthcare environments.

Healthcare applications store sensitive information, including patient details, medical records, clinical observations and other confidential healthcare data. Protecting this information from unauthorized access is an important requirement.

MediShield AI combines Role-Based Access Control (RBAC), data encryption, patient record management, security monitoring and Machine Learning-based anomaly detection.

The system provides different access permissions for healthcare personnel according to their assigned roles. It also monitors user activities and identifies potentially suspicious behaviour through AI-based analysis.

The main goal is to improve healthcare data confidentiality, controlled access and security monitoring through an intelligent healthcare security platform.

## 2. Problem Statement

Healthcare applications maintain sensitive information such as patient details, medical records, clinical observations and healthcare-related information.

Unauthorized access, improper handling of confidential information, suspicious login attempts and unusual data access activities can expose patient information to security risks.

Traditional access management systems may not be sufficient to identify unusual user activities or suspicious access patterns.

MediShield AI addresses these challenges by providing:

- Controlled access to healthcare records.
- Role-based user authentication.
- Encryption of sensitive information.
- User activity monitoring.
- Security event logging.
- AI-based anomaly detection.
- Centralized security monitoring.

The system aims to improve healthcare data protection by combining access control mechanisms with intelligent security analysis.

## 3. Project Objectives

The main objectives of MediShield AI are:

1. Protect sensitive healthcare information from unauthorized access.
2. Implement Role-Based Access Control for different healthcare personnel.
3. Secure confidential patient information through encryption.
4. Provide controlled access to patient records.
5. Monitor user activities through access logs.
6. Identify suspicious access patterns using Machine Learning.
7. Detect potentially anomalous HL7 messages.
8. Generate security alerts for suspicious activities.
9. Maintain security event history for monitoring.
10. Provide centralized security monitoring through administrative dashboards.

## 4. Key Features

### 4.1 User Authentication

- Secure user login and authentication.
- Role-based user access.
- Different dashboards based on user roles.
- User account management.
- Active and inactive account status management.

### 4.2 Patient Management

- Add and manage patient information.
- View patient records.
- Maintain healthcare-related information.
- Control access to confidential patient information.
- Provide role-based patient record access.

### 4.3 Data Privacy and Security

- Encryption of sensitive information.
- Data masking.
- Role-based permissions.
- Controlled access to healthcare records.
- Protection of confidential patient information.

### 4.4 Security Monitoring

- Access activity logs.
- Security alerts.
- Monitoring of user activities.
- Security event history.
- Monitoring of suspicious access patterns.

### 4.5 AI-Based Anomaly Detection

- Machine Learning-based healthcare data analysis.
- Behavioural anomaly detection.
- HL7 message anomaly prediction.
- Saved trained model files.
- Training and prediction modules.
- Detection of potentially suspicious activities.

### 4.6 Administrative Dashboard

- Centralized system monitoring.
- User management.
- Role and permission management.
- Security alert monitoring.
- Access activity monitoring.
- HL7 prediction history.

## 5. User Roles

MediShield AI supports five user roles.

| Role | Responsibilities |
|---|---|
| Admin | Manage users, monitor security and manage system activities |
| Doctor | Access permitted patient information and clinical records |
| Nurse | Access patient information according to assigned permissions |
| Receptionist | Handle permitted patient and administrative information |
| Lab Technician | Access permitted laboratory-related information |

### Role-Based Access Control

The system uses a role and permission management mechanism to control access to different functionalities.

Each user is assigned a role. The permissions associated with that role determine which system resources and operations the user can access.

This helps prevent users from accessing information outside their assigned responsibilities.

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
| Data Handling | Python |
| Development Environment | Visual Studio Code |
| Local Server | XAMPP |
| Version Control | Git and GitHub |

## 7. Project Architecture

The project is organized into separate modules for application management, database operations, security, AI processing and user interfaces.

### 7.1 Project Folder Structure

```text
MediShield_AI/
│
├── ai_engine/
│   ├── predict.py
│   ├── train.py
│   ├── train_hl7.py
│   ├── model.pkl
│   ├── training_results.json
│   └── saved_models/
│       └── hl7_anomaly_model.joblib
│
├── database/
│   ├── schema.sql
│   └── seed.sql
│
├── datasets/
│   └── emr/
│       ├── payload-normal.csv
│       ├── payload-anomaly.csv
│       ├── README.md
│       └── LICENSE
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

### 7.2 Architecture Description

**Frontend Layer**

- HTML provides the structure of the application.
- CSS provides the user interface design.
- JavaScript handles client-side interactions.

**Application Layer**

- Flask handles application routing.
- Authentication routes manage user login.
- Patient routes manage patient-related operations.
- Staff routes handle staff-related functionality.
- Admin routes manage administrative operations.
- Security routes handle security-related operations.

**Database Layer**

- MySQL / MariaDB stores application information.
- User details and role information are maintained in database tables.
- Patient records and security activities are stored for application operations.

**Security Layer**

- Access control manages role-based permissions.
- Encryption functionality protects sensitive information.
- Activity logs help monitor user operations.

**AI Layer**

- Training modules prepare Machine Learning models.
- Prediction modules perform anomaly analysis.
- Saved model files are used for prediction operations.

## 8. AI and Machine Learning Modules

MediShield AI contains two main Machine Learning-based anomaly detection components.

1. Behavioural Anomaly Detection.
2. HL7 Message Anomaly Detection.

The AI engine contains training and prediction components for healthcare-related anomaly analysis.

### 8.1 Behavioural Anomaly Detection

The behavioural anomaly detection module analyses user access patterns to identify potentially unusual activities.

It uses an **Isolation Forest** model to identify activities that differ from expected behaviour patterns.

The model uses the following seven features:

| Feature | Description |
|---|---|
| hour_of_day | Hour at which the activity occurs |
| day_of_week | Day of the week |
| records_accessed_last_hour | Number of records accessed in the last hour |
| distinct_patients_last_day | Number of different patients accessed in one day |
| failed_logins_last_hour | Number of failed login attempts |
| is_outside_business_hours | Indicates activity outside normal business hours |
| action_frequency | Frequency of user actions |

**Model Configuration:**

- Algorithm: Isolation Forest.
- Number of estimators: 200.
- Contamination: 0.05.
- Random state: 42.

**Prediction Output:**

The model identifies activities as:

- Normal activity.
- Potentially anomalous activity.

The prediction module also calculates a risk score and provides reasons that can help administrators investigate suspicious activities.

The behavioural model is used for security monitoring and anomaly identification. Its prediction alone does not automatically prove unauthorized access.

### 8.2 HL7 Message Anomaly Detection

HL7 (Health Level Seven) is a healthcare messaging standard used to exchange healthcare-related information between systems.

MediShield AI includes an HL7 message anomaly detection module to classify healthcare message types as normal or anomalous based on the training dataset.

**Model Details:**

| Component | Description |
|---|---|
| Algorithm | Random Forest Classifier |
| Number of Estimators | 150 |
| Random State | 42 |
| Class Weight | Balanced |
| Input Feature | MSGTYPE |
| Encoding | OneHotEncoder |
| Model Storage | Joblib |

**Training Dataset:**

- Normal HL7 payload dataset.
- Anomalous HL7 payload dataset.

The training process uses a stratified train-test split with 75% training data and 25% testing data.

**Prediction Process:**

1. Receive an HL7 message.
2. Extract the message type.
3. Normalize the message type.
4. Check whether the message type is supported.
5. Pass supported message types to the trained model.
6. Generate a classification result.
7. Store the prediction history.
8. Display the prediction result.

Unsupported message types are treated as suspicious by the application's validation logic.

### 8.3 Model Training and Prediction Files

| File | Purpose |
|---|---|
| `train.py` | Behavioural model training module |
| `train_hl7.py` | HL7 model training module |
| `predict.py` | Behavioural anomaly prediction |
| `model.pkl` | Saved behavioural model |
| `hl7_anomaly_model.joblib` | Saved HL7 model |
| `training_results.json` | Stored HL7 model evaluation results |

### 8.4 HL7 Model Evaluation Results

The recorded evaluation results from the current training run are:

| Metric | Result |
|---|---:|
| Accuracy | 58.26% |
| Precision | 86.19% |
| Recall | 54.11% |
| F1-Score | 66.48% |
| Normal Records | 16,164 |
| Anomaly Records | 52,611 |
| Test Records | 17,194 |

**Confusion Matrix:**

| Actual / Predicted | Normal | Anomaly |
|---|---:|---:|
| Normal | 2,901 | 1,140 |
| Anomaly | 6,036 | 7,117 |

These values represent the recorded model evaluation results, not a guarantee of real-world detection accuracy.

**Important Limitation:**

The current HL7 model uses message-type information as its classification feature. It is an experimental anomaly detection component and does not independently verify the complete contents or security of an HL7 message.

## 9. Dataset

The project includes healthcare-related datasets and HL7 message data under:

```text
datasets/emr/
```

### 9.1 Dataset Components

The dataset folder includes:

- Patient information data.
- Appointment data.
- Encounter data.
- Observation data.
- Practitioner data.
- Normal HL7 payload data.
- Anomalous HL7 payload data.
- HL7 database files.

### 9.2 HL7 Training Datasets

The HL7 anomaly detection model uses:

- `payload-normal.csv`
- `payload-anomaly.csv`

These files provide the normal and anomalous message records used in model training.

### 9.3 Dataset Documentation

The included dataset documentation identifies the healthcare records as generated datasets.

Refer to:

- `datasets/emr/README.md`
- `datasets/emr/LICENSE`

for dataset documentation and licensing information.

## 10. Installation and Setup

### 10.1 System Requirements

- Python 3.11 or later.
- XAMPP.
- MySQL or MariaDB.
- Git.
- A modern web browser.
- Visual Studio Code or another code editor.

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

Activate the virtual environment.

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

**Note:** The six demo accounts listed in Section 11 are available in the current development database. They are not automatically guaranteed to be created by the SQL files on a fresh installation.

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
- Keep the same encryption key safe for accessing previously encrypted data.

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

## 11. Demo Login Credentials

The following six accounts are available in the current development database.

| Username | Password |
|---|---|
| `admin` | `Admin@12345` |
| `dr_smith` | `Doctor@12345` |
| `nurse_kim` | `Nurse@12345` |
| `reception` | `Recep@12345` |
| `labtech` | `Lab@12345` |
| `Radhika` | `Radhi@134` |

### Login Instructions

1. Start the Flask application.
2. Open `http://127.0.0.1:5000`.
3. Enter the username and corresponding password.
4. Click the Login button.
5. Access the dashboard according to the assigned role.

**Note:** These credentials are for the current development accounts. They must be provisioned separately on a fresh installation. Verify each login before the project demonstration.

## 12. Database Structure

MediShield AI uses MySQL / MariaDB as its database management system.

The database name used by the current project is:

```text
medishield_ai
```

### 12.1 Database Tables

The current database contains the following tables:

| Table Name | Purpose |
|---|---|
| `users` | Stores user account information |
| `roles` | Stores user role information |
| `permissions` | Stores permission definitions |
| `role_permissions` | Maps roles to permissions |
| `patients` | Stores patient information |
| `access_logs` | Maintains user access activity logs |
| `security_alerts` | Stores security alert information |
| `hl7_prediction_history` | Maintains HL7 prediction history |

### 12.2 User Management

The `users` table contains fields such as:

- User ID.
- Username.
- Email.
- Password hash.
- Full name.
- Role ID.
- Account status.
- Last login.
- Created date.
- Updated date.

Passwords are stored as secure password hashes rather than readable plain-text passwords.

### 12.3 Role and Permission Management

The role and permission management system helps control access to application functionalities according to the assigned user role.

### 12.4 Security Activity Records

The system maintains access activity records and security alert information to support monitoring and investigation.

## 13. Security Implementation

MediShield AI includes multiple security-related components to improve healthcare data protection.

### 13.1 Authentication

- User login and authentication.
- Password hash verification.
- Account status management.
- User session management.

### 13.2 Role-Based Access Control

- Different user roles.
- Role-based permissions.
- Controlled access to patient records.
- Permission-based application functionality.

### 13.3 Data Encryption

- Encryption functionality for sensitive information.
- Secure handling of encryption keys.
- Protection of confidential healthcare information.

### 13.4 Data Masking

Data masking helps restrict the exposure of sensitive information when displaying healthcare-related records.

### 13.5 Access Logging

The system maintains access activity records to support monitoring of user operations.

### 13.6 Security Alerts

Security alerts help administrators identify and investigate potentially suspicious activities.

### 13.7 AI-Based Security Monitoring

Machine Learning-based anomaly detection helps identify unusual behavioural patterns and potentially anomalous HL7 messages.

These security mechanisms are intended to improve the confidentiality and controlled handling of healthcare information. They should not be considered a substitute for a complete production security audit.

## 14. Testing and Validation

The project includes testing of its authentication, database operations, security monitoring and AI prediction components.

### 14.1 User Authentication Testing

- Verify login using registered user accounts.
- Check role-based dashboard access.
- Verify account authentication.
- Check access restrictions.

### 14.2 Database Testing

- Verify database connectivity.
- Check user records.
- Verify patient information operations.
- Check access log storage.
- Verify security alert records.

### 14.3 Behavioural Model Testing

The behavioural model was tested using controlled normal and unusual activity patterns.

**Example normal activity:**

```text
Hour: 10
Day: 2
Records accessed: 2
Distinct patients: 3
Failed logins: 0
Outside business hours: 0
Action frequency: 2
```

Result: Normal.

**Example unusual activity:**

```text
Hour: 23
Day: 6
Records accessed: 40
Distinct patients: 50
Failed logins: 5
Outside business hours: 1
Action frequency: 60
```

Result: Anomaly.

These are controlled sample tests and do not represent validated real-world detection performance.

### 14.4 HL7 Model Testing

The HL7 prediction component was tested using supported and unsupported message types.

Example message types tested:

- `ADT^A01`
- `ADT^A02`
- `ADT^A03`
- `ADT^A05`
- `ADT^A13`
- `ADT^A28`
- `ADT^A31`
- `ADT^A38`
- `ADT^A40`
- `XYZ^999`

The prediction and validation results are intended to demonstrate the model's current classification and message-type validation functionality.

## 15. Future Enhancements

The following improvements can be considered for future development:

- Advanced real-time unauthorized access detection.
- Improved Machine Learning model performance.
- Enhanced security analytics and reporting.
- More comprehensive HL7 message analysis.
- Additional healthcare data integrations.
- Improved anomaly detection using additional features.
- Enhanced notification and alert mechanisms.
- Improved deployment and scalability.
- Stronger security testing and validation.
- More comprehensive audit reporting.

## 16. GitHub Repository

**Project Repository:**

https://github.com/Tharika18/MediShield-AI

The repository contains the project source code, database scripts, AI modules, dataset documentation and installation instructions.

## 17. Project Information

| Field | Details |
|---|---|
| Project Name | MediShield AI |
| Domain | Artificial Intelligence and Healthcare Cybersecurity |
| Project Type | Healthcare Data Privacy and Security System |
| Backend | Python Flask |
| Frontend | HTML, CSS, JavaScript |
| Database | MySQL / MariaDB |
| AI Technology | Machine Learning |
| Model Algorithms | Isolation Forest and Random Forest |
| Development Environment | Visual Studio Code |
| Local Server | XAMPP |

---

**MediShield AI – Protecting Healthcare Data Through Intelligent Security.**