#!/usr/bin/env python
"""
Django management command to load sample data into MySQL database.
Run with: python manage.py load_sample_data
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from hospital_app.models import Patient, Doctor, HospitalUser, Appointment, Treatment, Medication, Prescription, Billing
from datetime import date, time


class Command(BaseCommand):
    help = 'Load sample data into the database'

    def handle(self, *args, **options):
        self.stdout.write('Loading sample data...')
        
        # Create sample patients
        patients_data = [
            ('John Smith', 'Male', '1985-03-15', '+1-555-0101', 'A+'),
            ('Sarah Johnson', 'Female', '1990-07-22', '+1-555-0102', 'B+'),
            ('Michael Brown', 'Male', '1978-11-08', '+1-555-0103', 'O+'),
            ('Emily Davis', 'Female', '1992-05-14', '+1-555-0104', 'AB+'),
            ('David Wilson', 'Male', '1988-09-30', '+1-555-0105', 'A-'),
            ('Lisa Anderson', 'Female', '1983-12-03', '+1-555-0106', 'B-'),
            ('Robert Taylor', 'Male', '1975-04-18', '+1-555-0107', 'O-'),
            ('Jennifer Martinez', 'Female', '1995-08-25', '+1-555-0108', 'AB-'),
            ('William Garcia', 'Male', '1980-01-12', '+1-555-0109', 'A+'),
            ('Amanda Rodriguez', 'Female', '1987-06-07', '+1-555-0110', 'B+'),
        ]
        
        patients = []
        for name, gender, dob, contact, blood_group in patients_data:
            patient, created = Patient.objects.get_or_create(
                name=name,
                defaults={
                    'gender': gender,
                    'dob': dob,
                    'contact': contact,
                    'blood_group': blood_group
                }
            )
            patients.append(patient)
            if created:
                self.stdout.write(f'Created patient: {name}')
        
        # Create sample doctors
        doctors_data = [
            ('Dr. John Smith', 'General Medicine', '+1-555-1001'),
            ('Dr. Sarah Johnson', 'Cardiology', '+1-555-1002'),
            ('Dr. Michael Brown', 'Pediatrics', '+1-555-1003'),
            ('Dr. Emily Davis', 'Dermatology', '+1-555-1004'),
            ('Dr. David Wilson', 'Orthopedics', '+1-555-1005'),
            ('Dr. Lisa Anderson', 'Neurology', '+1-555-1006'),
            ('Dr. Robert Taylor', 'Oncology', '+1-555-1007'),
            ('Dr. Jennifer Martinez', 'Gynecology', '+1-555-1008'),
        ]
        
        doctors = []
        for name, specialization, contact in doctors_data:
            doctor, created = Doctor.objects.get_or_create(
                name=name,
                defaults={
                    'specialization': specialization,
                    'contact': contact
                }
            )
            doctors.append(doctor)
            if created:
                self.stdout.write(f'Created doctor: {name}')
        
        # Create sample appointments
        appointments_data = [
            (patients[0], doctors[0], '2024-09-25', '09:00:00', 'Completed'),
            (patients[1], doctors[1], '2024-09-25', '10:30:00', 'Completed'),
            (patients[2], doctors[2], '2024-09-25', '14:00:00', 'Completed'),
            (patients[3], doctors[3], '2024-09-26', '09:30:00', 'Completed'),
            (patients[4], doctors[4], '2024-09-26', '11:00:00', 'Completed'),
            (patients[5], doctors[5], '2024-09-26', '15:30:00', 'Completed'),
            (patients[6], doctors[6], '2024-09-27', '10:00:00', 'Completed'),
            (patients[7], doctors[7], '2024-09-27', '13:00:00', 'Completed'),
            (patients[0], doctors[1], '2024-09-28', '09:00:00', 'Scheduled'),
            (patients[1], doctors[2], '2024-09-28', '14:30:00', 'Scheduled'),
        ]
        
        appointments = []
        for patient, doctor, appt_date, appt_time, status in appointments_data:
            appointment, created = Appointment.objects.get_or_create(
                patient=patient,
                doctor=doctor,
                appointment_date=appt_date,
                appointment_time=appt_time,
                defaults={'status': status}
            )
            appointments.append(appointment)
            if created:
                self.stdout.write(f'Created appointment: {patient.name} with {doctor.name}')
        
        # Create sample treatments
        treatments_data = [
            (appointments[0], 'Routine Checkup', 'Patient in good health, recommended annual follow-up'),
            (appointments[1], 'Chest Pain Evaluation', 'ECG normal, stress test recommended'),
            (appointments[2], 'Child Vaccination', 'Administered MMR vaccine, no adverse reactions'),
            (appointments[3], 'Skin Rash', 'Prescribed topical cream, follow-up in 2 weeks'),
            (appointments[4], 'Knee Pain', 'X-ray shows mild arthritis, physical therapy recommended'),
        ]
        
        treatments = []
        for appointment, diagnosis, notes in treatments_data:
            treatment, created = Treatment.objects.get_or_create(
                appointment=appointment,
                defaults={
                    'diagnosis': diagnosis,
                    'notes': notes
                }
            )
            treatments.append(treatment)
            if created:
                self.stdout.write(f'Created treatment for appointment {appointment.appointment_id}')
        
        # Create sample medications
        medications_data = [
            ('Paracetamol', '500mg', 'MedPharm Inc'),
            ('Ibuprofen', '400mg', 'HealthCorp'),
            ('Amoxicillin', '250mg', 'Antibio Labs'),
            ('Lisinopril', '10mg', 'CardioMed'),
            ('Metformin', '500mg', 'DiabCare'),
            ('Atorvastatin', '20mg', 'CholestCorp'),
            ('Omeprazole', '20mg', 'DigestMed'),
            ('Cetirizine', '10mg', 'AllergyRelief'),
        ]
        
        medications = []
        for name, dosage, manufacturer in medications_data:
            medication, created = Medication.objects.get_or_create(
                name=name,
                defaults={
                    'dosage': dosage,
                    'manufacturer': manufacturer
                }
            )
            medications.append(medication)
            if created:
                self.stdout.write(f'Created medication: {name}')
        
        # Create sample prescriptions
        prescriptions_data = [
            (treatments[0], medications[0], 30, '7 days', 'Take 1 tablet every 6 hours as needed for pain'),
            (treatments[1], medications[1], 20, '5 days', 'Take 1 tablet twice daily with food'),
            (treatments[2], medications[2], 21, '7 days', 'Take 1 capsule three times daily'),
            (treatments[3], medications[3], 30, '30 days', 'Take 1 tablet daily in the morning'),
            (treatments[4], medications[4], 60, '30 days', 'Take 1 tablet twice daily with meals'),
        ]
        
        for treatment, medication, quantity, duration, instructions in prescriptions_data:
            prescription, created = Prescription.objects.get_or_create(
                treatment=treatment,
                medication=medication,
                defaults={
                    'quantity': quantity,
                    'duration': duration,
                    'instructions': instructions
                }
            )
            if created:
                self.stdout.write(f'Created prescription: {medication.name} for {treatment.appointment.patient.name}')
        
        # Create sample billing (only for completed appointments)
        billing_data = [
            (appointments[0], 150.00, 'Paid', 'Card', '2024-09-25'),
            (appointments[1], 300.00, 'Pending', None, '2024-09-25'),
            (appointments[2], 100.00, 'Paid', 'Cash', '2024-09-25'),
            (appointments[3], 200.00, 'Pending', None, '2024-09-26'),
            (appointments[4], 250.00, 'Paid', 'UPI', '2024-09-26'),
            (appointments[5], 400.00, 'Pending', None, '2024-09-26'),
            (appointments[6], 350.00, 'Paid', 'Insurance', '2024-09-27'),
            (appointments[7], 180.00, 'Pending', None, '2024-09-27'),
        ]
        
        for appointment, amount, payment_status, payment_method, billing_date in billing_data:
            billing, created = Billing.objects.get_or_create(
                appointment=appointment,
                defaults={
                    'amount': amount,
                    'payment_status': payment_status,
                    'payment_method': payment_method,
                    'billing_date': billing_date
                }
            )
            if created:
                self.stdout.write(f'Created billing for appointment {appointment.appointment_id}: ${amount}')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully loaded sample data!')
        )
