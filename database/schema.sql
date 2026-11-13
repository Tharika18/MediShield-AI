
-- =====================================================
-- MEDISHIELD AI DATABASE
-- Healthcare Data Privacy and Unauthorized Access Detection
-- =====================================================

CREATE DATABASE IF NOT EXISTS medishield_ai
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE medishield_ai;


-- =====================================================
-- 1. ROLES TABLE
-- =====================================================

CREATE TABLE IF NOT EXISTS roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    description VARCHAR(255),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;


-- =====================================================
-- 2. PERMISSIONS TABLE
-- =====================================================

CREATE TABLE IF NOT EXISTS permissions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description VARCHAR(255)
) ENGINE=InnoDB;


-- =====================================================
-- 3. ROLE PERMISSIONS TABLE
-- =====================================================

CREATE TABLE IF NOT EXISTS role_permissions (
    role_id INT NOT NULL,
    permission_id INT NOT NULL,

    PRIMARY KEY (role_id, permission_id),

    FOREIGN KEY (role_id)
        REFERENCES roles(id)
        ON DELETE CASCADE,

    FOREIGN KEY (permission_id)
        REFERENCES permissions(id)
        ON DELETE CASCADE

) ENGINE=InnoDB;


-- =====================================================
-- 4. USERS TABLE
-- =====================================================

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,

    username VARCHAR(80) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,

    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(120) NOT NULL,

    role_id INT NOT NULL,

    is_active BOOLEAN NOT NULL DEFAULT TRUE,

    last_login DATETIME NULL,

    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    updated_at DATETIME NOT NULL
        DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (role_id)
        REFERENCES roles(id)
        ON DELETE RESTRICT,

    INDEX idx_user_role (role_id),
    INDEX idx_user_active (is_active),
    INDEX idx_user_username (username),
    INDEX idx_user_email (email)

) ENGINE=InnoDB;


-- =====================================================
-- 5. PATIENTS TABLE
-- =====================================================

CREATE TABLE IF NOT EXISTS patients (
    id INT AUTO_INCREMENT PRIMARY KEY,

    patient_uuid VARCHAR(36) NOT NULL UNIQUE,

    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,

    date_of_birth DATE NOT NULL,

    gender ENUM('Male', 'Female', 'Other') NOT NULL,

    phone VARCHAR(20),
    address TEXT,

    encrypted_ssn TEXT,
    encrypted_medical_history TEXT,
    encrypted_diagnosis TEXT,
    encrypted_prescriptions TEXT,
    encrypted_lab_reports TEXT,

    created_by INT,

    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    updated_at DATETIME NOT NULL
        DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (created_by)
        REFERENCES users(id)
        ON DELETE SET NULL,

    INDEX idx_patient_uuid (patient_uuid),
    INDEX idx_patient_name (last_name, first_name)

) ENGINE=InnoDB;


-- =====================================================
-- 6. ACCESS LOGS TABLE
-- =====================================================

CREATE TABLE IF NOT EXISTS access_logs (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,

    user_id INT,
    patient_id INT,

    action VARCHAR(100) NOT NULL,

    status ENUM('SUCCESS', 'BLOCKED', 'FAILED') NOT NULL,

    ip_address VARCHAR(45),
    user_agent VARCHAR(255),

    details TEXT,

    risk_score FLOAT DEFAULT NULL,

    timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE SET NULL,

    FOREIGN KEY (patient_id)
        REFERENCES patients(id)
        ON DELETE SET NULL,

    INDEX idx_log_user (user_id),
    INDEX idx_log_patient (patient_id),
    INDEX idx_log_action (action),
    INDEX idx_log_status (status),
    INDEX idx_log_timestamp (timestamp)

) ENGINE=InnoDB;


-- =====================================================
-- 7. SECURITY ALERTS TABLE
-- =====================================================

CREATE TABLE IF NOT EXISTS security_alerts (
    id INT AUTO_INCREMENT PRIMARY KEY,

    log_id BIGINT NOT NULL,

    user_id INT,

    alert_type VARCHAR(50) NOT NULL,

    risk_score FLOAT NOT NULL,

    reason TEXT NOT NULL,

    is_resolved BOOLEAN NOT NULL DEFAULT FALSE,

    resolved_by INT,

    resolved_at DATETIME NULL,

    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (log_id)
        REFERENCES access_logs(id)
        ON DELETE CASCADE,

    FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE SET NULL,

    FOREIGN KEY (resolved_by)
        REFERENCES users(id)
        ON DELETE SET NULL,

    INDEX idx_alert_log (log_id),
    INDEX idx_alert_user (user_id),
    INDEX idx_alert_type (alert_type),
    INDEX idx_alert_resolved (is_resolved),
    INDEX idx_alert_score (risk_score),
    INDEX idx_alert_created (created_at)

) ENGINE=InnoDB;



-- =====================================================
-- 8. HL7 PREDICTION HISTORY TABLE
-- =====================================================

CREATE TABLE IF NOT EXISTS hl7_prediction_history (

    id INT AUTO_INCREMENT PRIMARY KEY,

    user_id INT NULL,

    message_type VARCHAR(20) NOT NULL,

    prediction VARCHAR(20) NOT NULL,

    created_at DATETIME NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE SET NULL,

    INDEX idx_hl7_prediction_date (created_at),

    INDEX idx_hl7_prediction_result (prediction)

) ENGINE=InnoDB;


-- =====================================================
-- DATABASE STRUCTURE COMPLETED
-- =====================================================

