# 🏥 Patient Management System (Mini Project)

A comprehensive web-based Hospital Management System designed to streamline patient appointments, doctor management, treatment records, and billing processes. This mini project demonstrates full-stack development with a normalized database design.

## 🌟 Features

- **Patient Management**: Register and manage patient information
- **Doctor Management**: Maintain doctor profiles and specializations
- **Appointment Scheduling**: Book, view, and manage appointments
- **Treatment Records**: Maintain diagnosis and treatment history
- **Prescription System**: Digital prescription management with medication database
- **Billing System**: Generate and manage patient bills
- **User Authentication**: Role-based login system (Admin/Doctor)
- **Responsive Design**: Mobile-friendly interface

## 🗄️ Database Schema

### Tables Structure

#### 1. Core Tables
```sql
-- Doctors Table
CREATE TABLE Doctors (
    DoctorID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Specialization VARCHAR(100),
    Contact VARCHAR(15)
);

-- Patients Table
CREATE TABLE Patients (
    PatientID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Gender ENUM('Male', 'Female', 'Other'),
    DOB DATE,
    Contact VARCHAR(15),
    BloodGroup ENUM('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-')
);

-- Appointments Table
CREATE TABLE Appointments (
    AppointmentID INT AUTO_INCREMENT PRIMARY KEY,
    PatientID INT NOT NULL,
    DoctorID INT NOT NULL,
    AppointmentDate DATE NOT NULL,
    AppointmentTime TIME NOT NULL,
    Status ENUM('Scheduled', 'Completed', 'Cancelled') DEFAULT 'Scheduled',
    FOREIGN KEY (PatientID) REFERENCES Patients(PatientID) ON DELETE CASCADE,
    FOREIGN KEY (DoctorID) REFERENCES Doctors(DoctorID) ON DELETE CASCADE
);

-- Treatments Table
CREATE TABLE Treatments (
    TreatmentID INT AUTO_INCREMENT PRIMARY KEY,
    AppointmentID INT NOT NULL UNIQUE,
    Diagnosis TEXT NOT NULL,
    Notes TEXT,
    FOREIGN KEY (AppointmentID) REFERENCES Appointments(AppointmentID) ON DELETE CASCADE
);

-- Medications Table
CREATE TABLE Medications (
    MedicationID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL UNIQUE,
    Dosage VARCHAR(50),
    Manufacturer VARCHAR(100)
);

-- Prescriptions Table
CREATE TABLE Prescriptions (
    PrescriptionID INT AUTO_INCREMENT PRIMARY KEY,
    TreatmentID INT NOT NULL,
    MedicationID INT NOT NULL,
    Quantity INT DEFAULT 1,
    Duration VARCHAR(50),
    Instructions TEXT,
    FOREIGN KEY (TreatmentID) REFERENCES Treatments(TreatmentID) ON DELETE CASCADE,
    FOREIGN KEY (MedicationID) REFERENCES Medications(MedicationID)
);

-- Billing Table
CREATE TABLE Billing (
    BillID INT AUTO_INCREMENT PRIMARY KEY,
    AppointmentID INT NOT NULL UNIQUE,
    Amount DECIMAL(10, 2) NOT NULL,
    PaymentStatus ENUM('Pending', 'Paid') DEFAULT 'Pending',
    PaymentMethod ENUM('Cash', 'Card', 'UPI'),
    BillingDate DATE,
    FOREIGN KEY (AppointmentID) REFERENCES Appointments(AppointmentID) ON DELETE CASCADE
);

-- Users Table
CREATE TABLE Users (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(50) UNIQUE NOT NULL,
    Password VARCHAR(255) NOT NULL,
    Role ENUM('Admin', 'Doctor') NOT NULL,
    DoctorID INT NULL,
    FOREIGN KEY (DoctorID) REFERENCES Doctors(DoctorID) ON DELETE CASCADE
);