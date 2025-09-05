-- Create Database

CREATE DATABASE PatientManagementDB;
USE PatientManagementDB;

-- ================================
-- PATIENT MANAGEMENT SYSTEM SCHEMA
-- ================================

CREATE TABLE Patients (
    PatientID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100) NOT NULL,
    Gender VARCHAR(10) CHECK (Gender IN ('Male','Female','Other')),
    DOB DATE NOT NULL,
    Contact VARCHAR(50),
    BloodGroup VARCHAR(5) CHECK (BloodGroup IN ('A+','A-','B+','B-','AB+','AB-','O+','O-'))
);

CREATE TABLE Doctors (
    DoctorID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100) NOT NULL,
    Specialization VARCHAR(100) NOT NULL,
    Contact VARCHAR(50)
);

CREATE TABLE Users (
    UserID INT PRIMARY KEY AUTO_INCREMENT,
    Username VARCHAR(50) UNIQUE NOT NULL,
    Password VARCHAR(255) NOT NULL,
    Role VARCHAR(20) CHECK (Role IN ('Admin','Doctor','Staff')),
    DoctorID INT,
    CONSTRAINT fk_users_doctor FOREIGN KEY (DoctorID)
        REFERENCES Doctors(DoctorID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE Appointments (
    AppointmentID INT PRIMARY KEY AUTO_INCREMENT,
    PatientID INT NOT NULL,
    DoctorID INT NOT NULL,
    AppointmentDate DATE NOT NULL,
    AppointmentTime TIME NOT NULL,
    Status VARCHAR(20) CHECK (Status IN ('Scheduled','Completed','Cancelled')),
    CONSTRAINT fk_appointments_patient FOREIGN KEY (PatientID)
        REFERENCES Patients(PatientID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_appointments_doctor FOREIGN KEY (DoctorID)
        REFERENCES Doctors(DoctorID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE INDEX idx_appointments_patient ON Appointments(PatientID);
CREATE INDEX idx_appointments_doctor ON Appointments(DoctorID);

CREATE TABLE Treatments (
    TreatmentID INT PRIMARY KEY AUTO_INCREMENT,
    AppointmentID INT NOT NULL,
    Diagnosis TEXT,
    Notes TEXT,
    CONSTRAINT fk_treatments_appointment FOREIGN KEY (AppointmentID)
        REFERENCES Appointments(AppointmentID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE INDEX idx_treatments_appointment ON Treatments(AppointmentID);

CREATE TABLE Medications (
    MedicationID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100) UNIQUE NOT NULL,
    Dosage VARCHAR(50),
    Manufacturer VARCHAR(100)
);

CREATE TABLE Prescriptions (
    PrescriptionID INT PRIMARY KEY AUTO_INCREMENT,
    TreatmentID INT NOT NULL,
    MedicationID INT NOT NULL,
    Quantity INT NOT NULL,
    Duration VARCHAR(50),
    Instructions TEXT,
    CONSTRAINT fk_prescriptions_treatment FOREIGN KEY (TreatmentID)
        REFERENCES Treatments(TreatmentID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_prescriptions_medication FOREIGN KEY (MedicationID)
        REFERENCES Medications(MedicationID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE INDEX idx_prescriptions_treatment ON Prescriptions(TreatmentID);
CREATE INDEX idx_prescriptions_medication ON Prescriptions(MedicationID);

CREATE TABLE Billing (
    BillID INT PRIMARY KEY AUTO_INCREMENT,
    AppointmentID INT NOT NULL,
    Amount DECIMAL(10,2) NOT NULL,
    PaymentStatus VARCHAR(20) CHECK (PaymentStatus IN ('Paid','Pending','Cancelled')),
    PaymentMethod VARCHAR(20) CHECK (PaymentMethod IN ('Cash','Card','UPI','Insurance')),
    BillingDate DATE NOT NULL,
    CONSTRAINT fk_billing_appointment FOREIGN KEY (AppointmentID)
        REFERENCES Appointments(AppointmentID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE INDEX idx_billing_appointment ON Billing(AppointmentID);

-- ================================
-- TRIGGERS (Optional - Placeholders)
-- ================================

-- Example: Ensure Billing is only created if Appointment status is 'Completed'
DELIMITER $$
CREATE TRIGGER trg_billing_before_insert
BEFORE INSERT ON Billing
FOR EACH ROW
BEGIN
    DECLARE appt_status VARCHAR(20);
    SELECT Status INTO appt_status FROM Appointments WHERE AppointmentID = NEW.AppointmentID;
    IF appt_status <> 'Completed' THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Billing can only be generated for completed appointments';
    END IF;
END$$
DELIMITER ;

-- Example: Auto-cancel appointments if patient is deleted (handled by cascade, trigger only for logging)
DELIMITER $$
CREATE TRIGGER trg_patient_delete
AFTER DELETE ON Patients
FOR EACH ROW
BEGIN
    INSERT INTO AuditLog (Action, Description, ActionDate)
    VALUES ('DELETE', CONCAT('Patient ', OLD.PatientID, ' deleted, related appointments removed'), NOW());
END$$
DELIMITER ;

-- Note: AuditLog table must exist if you use logging triggers


-- ================================
-- ADMIN ROLE VIEW
-- ================================
-- Admins should see EVERYTHING (all tables combined)
CREATE OR REPLACE VIEW vw_AdminDashboard AS
SELECT 
    p.PatientID, p.Name AS PatientName, p.Gender, p.DOB, p.Contact AS PatientContact, p.BloodGroup,
    d.DoctorID, d.Name AS DoctorName, d.Specialization, d.Contact AS DoctorContact,
    a.AppointmentID, a.AppointmentDate, a.AppointmentTime, a.Status AS AppointmentStatus,
    t.TreatmentID, t.Diagnosis, t.Notes,
    m.MedicationID, m.Name AS MedicationName, m.Dosage, m.Manufacturer,
    pr.PrescriptionID, pr.Quantity, pr.Duration, pr.Instructions,
    b.BillID, b.Amount, b.PaymentStatus, b.PaymentMethod, b.BillingDate
FROM Patients p
LEFT JOIN Appointments a ON p.PatientID = a.PatientID
LEFT JOIN Doctors d ON a.DoctorID = d.DoctorID
LEFT JOIN Treatments t ON a.AppointmentID = t.AppointmentID
LEFT JOIN Prescriptions pr ON t.TreatmentID = pr.TreatmentID
LEFT JOIN Medications m ON pr.MedicationID = m.MedicationID
LEFT JOIN Billing b ON a.AppointmentID = b.AppointmentID;

-- ================================
-- DOCTOR ROLE VIEW
-- ================================
-- Doctors should only see their own appointments, treatments, and prescriptions
CREATE OR REPLACE VIEW vw_DoctorDashboard AS
SELECT 
    d.DoctorID, d.Name AS DoctorName, d.Specialization,
    p.PatientID, p.Name AS PatientName, p.Gender, p.DOB, p.BloodGroup,
    a.AppointmentID, a.AppointmentDate, a.AppointmentTime, a.Status AS AppointmentStatus,
    t.TreatmentID, t.Diagnosis, t.Notes,
    pr.PrescriptionID, m.Name AS MedicationName, pr.Quantity, pr.Duration, pr.Instructions
FROM Doctors d
JOIN Appointments a ON d.DoctorID = a.DoctorID
JOIN Patients p ON a.PatientID = p.PatientID
LEFT JOIN Treatments t ON a.AppointmentID = t.AppointmentID
LEFT JOIN Prescriptions pr ON t.TreatmentID = pr.TreatmentID
LEFT JOIN Medications m ON pr.MedicationID = m.MedicationID;

-- ================================
-- STAFF ROLE VIEW
-- ================================
-- Staff should manage appointments, billing, and patient details but not see treatment notes
CREATE OR REPLACE VIEW vw_StaffDashboard AS
SELECT 
    p.PatientID, p.Name AS PatientName, p.Gender, p.DOB, p.Contact AS PatientContact,
    d.DoctorID, d.Name AS DoctorName, d.Specialization,
    a.AppointmentID, a.AppointmentDate, a.AppointmentTime, a.Status AS AppointmentStatus,
    b.BillID, b.Amount, b.PaymentStatus, b.PaymentMethod, b.BillingDate
FROM Patients p
JOIN Appointments a ON p.PatientID = a.PatientID
JOIN Doctors d ON a.DoctorID = d.DoctorID
LEFT JOIN Billing b ON a.AppointmentID = b.AppointmentID;

-- ================================
-- PATIENT SELF-SERVICE VIEW
-- ================================
-- Patients should only see their own info, appointments, prescriptions, and bills
CREATE OR REPLACE VIEW vw_PatientPortal AS
SELECT 
    p.PatientID, p.Name AS PatientName, p.Gender, p.DOB, p.Contact, p.BloodGroup,
    a.AppointmentID, a.AppointmentDate, a.AppointmentTime, a.Status AS AppointmentStatus,
    d.Name AS DoctorName, d.Specialization,
    t.Diagnosis, 
    pr.PrescriptionID, m.Name AS MedicationName, pr.Quantity, pr.Duration, pr.Instructions,
    b.BillID, b.Amount, b.PaymentStatus, b.PaymentMethod, b.BillingDate
FROM Patients p
JOIN Appointments a ON p.PatientID = a.PatientID
JOIN Doctors d ON a.DoctorID = d.DoctorID
LEFT JOIN Treatments t ON a.AppointmentID = t.AppointmentID
LEFT JOIN Prescriptions pr ON t.TreatmentID = pr.TreatmentID
LEFT JOIN Medications m ON pr.MedicationID = m.MedicationID
LEFT JOIN Billing b ON a.AppointmentID = b.AppointmentID;
