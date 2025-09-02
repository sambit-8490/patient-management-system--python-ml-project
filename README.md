# 🏥 Patient Management System

## 📌 Overview
The **Patient Management System (PMS)** is a database-driven application designed to simplify hospital operations.  
It helps administrators, doctors, and staff manage patients, appointments, treatments, and billing efficiently.  
This system improves accuracy, reduces paperwork, and enhances overall patient care.  

---

## 🚀 Features
- 👤 **Patient Management** – Register, update, and view patient records.  
- 👨‍⚕️ **Doctor Management** – Store doctor details and specializations.  
- 📅 **Appointments** – Book, update, and track patient appointments.  
- 💊 **Treatments** – Record diagnosis, prescriptions, and notes.  
- 💳 **Billing** – Generate and manage patient bills with payment status.  
- 🔐 **User Roles** – Admin, Doctor, and Receptionist access.  

---

## 🗄️ Database Design
### Entities
- Patients  
- Doctors  
- Appointments  
- Treatments  
- Billing  
- Users  

### Relationships
- One Patient → Many Appointments  
- One Doctor → Many Appointments  
- One Appointment → One Treatment & One Bill  

---

## 📊 ER Diagram
*(Insert ER diagram image here, e.g. `assets/er_diagram.png`)*

---

## 📐 Schema Design
```sql
Patients(PatientID, Name, Age, Gender, Contact, Address)  
Doctors(DoctorID, Name, Specialization, Contact)  
Appointments(AppointmentID, PatientID, DoctorID, Date, Time, Status)  
Treatments(TreatmentID, AppointmentID, Diagnosis, Prescription, Notes)  
Billing(BillID, AppointmentID, Amount, PaymentStatus, Date)  
Users(UserID, Username, Password, Role)
