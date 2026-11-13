USE medishield_ai;

INSERT INTO roles (name, description) VALUES
('Admin', 'System administrator with full access'),
('Doctor', 'Medical doctor – full clinical access'),
('Nurse', 'Nursing staff – limited clinical access'),
('Receptionist', 'Front-desk – demographics only'),
('Lab Technician', 'Lab staff – lab reports only');

INSERT INTO permissions (name, description) VALUES
('manage_users', 'Create/edit/disable users'),
('view_all_patients', 'View all patients'),
('view_patient_medical', 'View sensitive medical fields'),
('edit_patient', 'Edit patient records'),
('view_audit', 'View audit logs'),
('view_alerts', 'View AI security alerts'),
('manage_alerts', 'Resolve security alerts');

-- Admin gets everything
INSERT INTO role_permissions (role_id, permission_id)
SELECT 1, id FROM permissions;

-- Doctor
INSERT INTO role_permissions (role_id, permission_id) VALUES
(2, 2), (2, 3), (2, 4);

-- Nurse
INSERT INTO role_permissions (role_id, permission_id) VALUES
(3, 2);

-- Receptionist
INSERT INTO role_permissions (role_id, permission_id) VALUES
(4, 2);

-- Lab Tech
INSERT INTO role_permissions (role_id, permission_id) VALUES
(5, 2);