-- Sample Data for Patient Management System
-- Run these INSERT statements to populate your database with sample data

-- Insert Sample Patients
INSERT INTO Patients (Name, Gender, DOB, Contact, BloodGroup) VALUES
('John Smith', 'Male', '1985-03-15', '+1-555-0101', 'A+'),
('Sarah Johnson', 'Female', '1990-07-22', '+1-555-0102', 'B+'),
('Michael Brown', 'Male', '1978-11-08', '+1-555-0103', 'O+'),
('Emily Davis', 'Female', '1992-05-14', '+1-555-0104', 'AB+'),
('David Wilson', 'Male', '1988-09-30', '+1-555-0105', 'A-'),
('Lisa Anderson', 'Female', '1983-12-03', '+1-555-0106', 'B-'),
('Robert Taylor', 'Male', '1975-04-18', '+1-555-0107', 'O-'),
('Jennifer Martinez', 'Female', '1995-08-25', '+1-555-0108', 'AB-'),
('William Garcia', 'Male', '1980-01-12', '+1-555-0109', 'A+'),
('Amanda Rodriguez', 'Female', '1987-06-07', '+1-555-0110', 'B+');

-- Insert Sample Doctors
INSERT INTO Doctors (Name, Specialization, Contact) VALUES
('Dr. John Smith', 'General Medicine', '+1-555-1001'),
('Dr. Sarah Johnson', 'Cardiology', '+1-555-1002'),
('Dr. Michael Brown', 'Pediatrics', '+1-555-1003'),
('Dr. Emily Davis', 'Dermatology', '+1-555-1004'),
('Dr. David Wilson', 'Orthopedics', '+1-555-1005'),
('Dr. Lisa Anderson', 'Neurology', '+1-555-1006'),
('Dr. Robert Taylor', 'Oncology', '+1-555-1007'),
('Dr. Jennifer Martinez', 'Gynecology', '+1-555-1008');

-- Insert Sample Appointments
INSERT INTO Appointments (PatientID, DoctorID, AppointmentDate, AppointmentTime, Status) VALUES
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

-- Insert Sample Treatments
INSERT INTO Treatments (AppointmentID, Diagnosis, Notes) VALUES
(1, 'Routine Checkup', 'Patient in good health, recommended annual follow-up'),
(2, 'Chest Pain Evaluation', 'ECG normal, stress test recommended'),
(3, 'Child Vaccination', 'Administered MMR vaccine, no adverse reactions'),
(4, 'Skin Rash', 'Prescribed topical cream, follow-up in 2 weeks'),
(5, 'Knee Pain', 'X-ray shows mild arthritis, physical therapy recommended');

-- Insert Sample Medications
INSERT INTO Medications (Name, Dosage, Manufacturer) VALUES
('Paracetamol', '500mg', 'MedPharm Inc'),
('Ibuprofen', '400mg', 'HealthCorp'),
('Amoxicillin', '250mg', 'Antibio Labs'),
('Lisinopril', '10mg', 'CardioMed'),
('Metformin', '500mg', 'DiabCare'),
('Atorvastatin', '20mg', 'CholestCorp'),
('Omeprazole', '20mg', 'DigestMed'),
('Cetirizine', '10mg', 'AllergyRelief');

-- Insert Sample Prescriptions
INSERT INTO Prescriptions (TreatmentID, MedicationID, Quantity, Duration, Instructions) VALUES
(1, 1, 30, '7 days', 'Take 1 tablet every 6 hours as needed for pain'),
(2, 2, 20, '5 days', 'Take 1 tablet twice daily with food'),
(3, 3, 21, '7 days', 'Take 1 capsule three times daily'),
(4, 4, 30, '30 days', 'Take 1 tablet daily in the morning'),
(5, 5, 60, '30 days', 'Take 1 tablet twice daily with meals');

-- Insert Sample Billing
INSERT INTO Billing (AppointmentID, Amount, PaymentStatus, PaymentMethod, BillingDate) VALUES
(1, 150.00, 'Paid', 'Card', '2024-09-25'),
(2, 300.00, 'Pending', NULL, '2024-09-25'),
(3, 100.00, 'Paid', 'Cash', '2024-09-25'),
(4, 200.00, 'Pending', NULL, '2024-09-26'),
(5, 250.00, 'Paid', 'UPI', '2024-09-26'),
(6, 400.00, 'Pending', NULL, '2024-09-26'),
(7, 350.00, 'Paid', 'Insurance', '2024-09-27'),
(8, 180.00, 'Pending', NULL, '2024-09-27');
