from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class Patient(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]
    
    PatientID = models.AutoField(primary_key=True, db_column='PatientID')
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    dob = models.DateField()
    contact = models.CharField(max_length=50, blank=True, null=True)
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES, blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} (ID: {self.PatientID})"
    
    class Meta:
        db_table = 'Patients'
        managed = False


class Doctor(models.Model):
    DoctorID = models.AutoField(primary_key=True, db_column='DoctorID')
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    contact = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return f"Dr. {self.name} - {self.specialization}"
    
    class Meta:
        db_table = 'Doctors'
        managed = False


class HospitalUser(models.Model):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Doctor', 'Doctor'),
        ('Staff', 'Staff'),
    ]
    
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username} ({self.role})"
    
    class Meta:
        db_table = 'Users'
        managed = False


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]
    
    AppointmentID = models.AutoField(primary_key=True, db_column='AppointmentID')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Scheduled')
    
    def __str__(self):
        return f"Appointment {self.AppointmentID} - {self.patient.name} with Dr. {self.doctor.name}"
    
    class Meta:
        db_table = 'Appointments'
        managed = False


class Treatment(models.Model):
    TreatmentID = models.AutoField(primary_key=True, db_column='TreatmentID')
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    diagnosis = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Treatment for {self.appointment}"
    
    class Meta:
        db_table = 'Treatments'
        managed = False


class Medication(models.Model):
    MedicationID = models.AutoField(primary_key=True, db_column='MedicationID')
    name = models.CharField(max_length=100, unique=True)
    dosage = models.CharField(max_length=50, blank=True, null=True)
    manufacturer = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} ({self.dosage})"
    
    class Meta:
        db_table = 'Medications'
        managed = False


class Prescription(models.Model):
    PrescriptionID = models.AutoField(primary_key=True, db_column='PrescriptionID')
    treatment = models.ForeignKey(Treatment, on_delete=models.CASCADE)
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    duration = models.CharField(max_length=50, blank=True, null=True)
    instructions = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.medication.name} for {self.treatment.appointment.patient.name}"
    
    class Meta:
        db_table = 'Prescriptions'
        managed = False


class Billing(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('Paid', 'Paid'),
        ('Pending', 'Pending'),
        ('Cancelled', 'Cancelled'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('Cash', 'Cash'),
        ('Card', 'Card'),
        ('UPI', 'UPI'),
        ('Insurance', 'Insurance'),
    ]
    
    BillID = models.AutoField(primary_key=True, db_column='BillID')
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='Pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, blank=True, null=True)
    billing_date = models.DateField()
    
    def __str__(self):
        return f"Bill {self.BillID} - {self.appointment.patient.name} - ${self.amount}"
    
    class Meta:
        db_table = 'Billing'
        managed = False
