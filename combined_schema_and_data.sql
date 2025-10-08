-- Combined schema and sample data for Patient Management System
-- Run this once in MySQL Workbench

CREATE DATABASE IF NOT EXISTS PatientManagementDB;
USE PatientManagementDB;

-- Drop in dependency order
SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS Prescriptions;
DROP TABLE IF EXISTS Billing;
DROP TABLE IF EXISTS Treatments;
DROP TABLE IF EXISTS Appointments;
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Medications;
DROP TABLE IF EXISTS Doctors;
DROP TABLE IF EXISTS Patients;
SET FOREIGN_KEY_CHECKS = 1;

-- Tables
CREATE TABLE Patients (
    PatientID INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    gender VARCHAR(10),
    dob DATE NOT NULL,
    contact VARCHAR(50),
    blood_group VARCHAR(5)
);

CREATE TABLE Doctors (
    DoctorID INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    specialization VARCHAR(100),
    contact VARCHAR(50)
);

CREATE TABLE Appointments (
    AppointmentID INT PRIMARY KEY AUTO_INCREMENT,
    patient_id INT,
    doctor_id INT,
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    status VARCHAR(20) DEFAULT 'Scheduled',
    FOREIGN KEY (patient_id) REFERENCES Patients(PatientID) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES Doctors(DoctorID) ON DELETE CASCADE
);

CREATE TABLE Treatments (
    TreatmentID INT PRIMARY KEY AUTO_INCREMENT,
    appointment_id INT,
    diagnosis VARCHAR(200),
    notes TEXT,
    FOREIGN KEY (appointment_id) REFERENCES Appointments(AppointmentID) ON DELETE CASCADE
);

CREATE TABLE Medications (
    MedicationID INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    dosage VARCHAR(50),
    manufacturer VARCHAR(100)
);

CREATE TABLE Prescriptions (
    PrescriptionID INT PRIMARY KEY AUTO_INCREMENT,
    treatment_id INT,
    medication_id INT,
    quantity INT,
    duration VARCHAR(50),
    instructions TEXT,
    FOREIGN KEY (treatment_id) REFERENCES Treatments(TreatmentID) ON DELETE CASCADE,
    FOREIGN KEY (medication_id) REFERENCES Medications(MedicationID) ON DELETE CASCADE
);

CREATE TABLE Billing (
    BillID INT PRIMARY KEY AUTO_INCREMENT,
    appointment_id INT,
    amount DECIMAL(10,2) NOT NULL,
    payment_status VARCHAR(20) DEFAULT 'Pending',
    payment_method VARCHAR(50),
    billing_date DATE,
    FOREIGN KEY (appointment_id) REFERENCES Appointments(AppointmentID) ON DELETE CASCADE
);

CREATE TABLE Users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    role VARCHAR(20) NOT NULL,
    doctor_id INT,
    FOREIGN KEY (doctor_id) REFERENCES Doctors(DoctorID) ON DELETE CASCADE
);

-- Sample Data


-- Alternative approach using patient IDs if you have them
UPDATE Patients SET name = 'Carlos Hernández' WHERE name = 'John Smith';
UPDATE Patients SET name = 'María García' WHERE name = 'Sarah Johnson';
UPDATE Patients SET name = 'Miguel López' WHERE name = 'Michael Brown';
UPDATE Patients SET name = 'Ana Martínez' WHERE name = 'Emily Davis';
UPDATE Patients SET name = 'José González' WHERE name = 'David Wilson';
UPDATE Patients SET name = 'Isabel Rodríguez' WHERE name = 'Lisa Anderson';
UPDATE Patients SET name = 'Francisco Pérez' WHERE name = 'Robert Taylor';
UPDATE Patients SET name = 'Carmen Sánchez' WHERE name = 'Jennifer Martinez';
UPDATE Patients SET name = 'Javier Ramírez' WHERE name = 'William Garcia';
UPDATE Patients SET name = 'Elena Torres' WHERE name = 'Amanda Rodriguez';

INSERT INTO Doctors (name, specialization, contact) VALUES
('Dr. John Smith', 'General Medicine', '+1-555-1001'),
('Dr. Sarah Johnson', 'Cardiology', '+1-555-1002'),
('Dr. Michael Brown', 'Pediatrics', '+1-555-1003'),
('Dr. Emily Davis', 'Dermatology', '+1-555-1004'),
('Dr. David Wilson', 'Orthopedics', '+1-555-1005'),
('Dr. Lisa Anderson', 'Neurology', '+1-555-1006'),
('Dr. Robert Taylor', 'Oncology', '+1-555-1007'),
('Dr. Jennifer Martinez', 'Gynecology', '+1-555-1008');

INSERT INTO Appointments (patient_id, doctor_id, appointment_date, appointment_time, status) VALUES
(1, 1, '2024-09-25', '09:00:00', 'Completed'),
(2, 2, '2024-09-25', '10:30:00', 'Completed'),
(3, 3, '2024-09-25', '14:00:00', 'Completed'),
(4, 4, '2024-09-26', '09:30:00', 'Completed'),
(5, 5, '2024-09-26', '11:00:00', 'Completed'),
(6, 6, '2024-09-26', '15:30:00', 'Completed'),
(7, 7, '2024-09-27', '10:00:00', 'Completed'),
(8, 8, '2024-09-27', '13:00:00', 'Completed'),
(1, 2, '2024-09-28', '09:00:00', 'Scheduled'),
(2, 3, '2024-09-28', '14:30:00', 'Scheduled');

INSERT INTO Treatments (appointment_id, diagnosis, notes) VALUES
(1, 'Routine Checkup', 'Patient in good health, recommended annual follow-up'),
(2, 'Chest Pain Evaluation', 'ECG normal, stress test recommended'),
(3, 'Child Vaccination', 'Administered MMR vaccine, no adverse reactions'),
(4, 'Skin Rash', 'Prescribed topical cream, follow-up in 2 weeks'),
(5, 'Knee Pain', 'X-ray shows mild arthritis, physical therapy recommended');

INSERT INTO Medications (name, dosage, manufacturer) VALUES
('Paracetamol', '500mg', 'MedPharm Inc'),
('Ibuprofen', '400mg', 'HealthCorp'),
('Amoxicillin', '250mg', 'Antibio Labs'),
('Lisinopril', '10mg', 'CardioMed'),
('Metformin', '500mg', 'DiabCare'),
('Atorvastatin', '20mg', 'CholestCorp'),
('Omeprazole', '20mg', 'DigestMed'),
('Cetirizine', '10mg', 'AllergyRelief');

INSERT INTO Prescriptions (treatment_id, medication_id, quantity, duration, instructions) VALUES
(1, 1, 30, '7 days', 'Take 1 tablet every 6 hours as needed for pain'),
(2, 2, 20, '5 days', 'Take 1 tablet twice daily with food'),
(3, 3, 21, '7 days', 'Take 1 capsule three times daily'),
(4, 4, 30, '30 days', 'Take 1 tablet daily in the morning'),
(5, 5, 60, '30 days', 'Take 1 tablet twice daily with meals');

INSERT INTO Billing (appointment_id, amount, payment_status, payment_method, billing_date) VALUES
(1, 150.00, 'Paid', 'Card', '2024-09-25'),
(2, 300.00, 'Pending', NULL, '2024-09-25'),
(3, 100.00, 'Paid', 'Cash', '2024-09-25'),
(4, 200.00, 'Pending', NULL, '2024-09-26'),
(5, 250.00, 'Paid', 'UPI', '2024-09-26'),
(6, 400.00, 'Pending', NULL, '2024-09-26'),
(7, 350.00, 'Paid', 'Insurance', '2024-09-27'),
(8, 180.00, 'Pending', NULL, '2024-09-27');


