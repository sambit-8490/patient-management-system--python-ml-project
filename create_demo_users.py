#!/usr/bin/env python
"""
Script to create demo users for the Patient Management System.
This script creates Django User accounts and their corresponding HospitalUser profiles.
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patient_management.settings')
django.setup()

from django.contrib.auth.models import User
from hospital_app.models import HospitalUser, Doctor

def create_demo_users():
    """Create demo users with proper HospitalUser profiles"""
    
    print("Creating demo users...")
    
    # Create or get admin user
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@hospital.com',
            'first_name': 'Admin',
            'last_name': 'User',
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        print("✓ Created admin user")
    else:
        print("✓ Admin user already exists")
    
    # Create or get doctor user
    doctor_user, created = User.objects.get_or_create(
        username='doctor',
        defaults={
            'email': 'doctor@hospital.com',
            'first_name': 'Dr. John',
            'last_name': 'Smith',
            'is_staff': False,
            'is_superuser': False
        }
    )
    if created:
        doctor_user.set_password('doctor123')
        doctor_user.save()
        print("✓ Created doctor user")
    else:
        print("✓ Doctor user already exists")
    
    # Create or get staff user
    staff_user, created = User.objects.get_or_create(
        username='staff',
        defaults={
            'email': 'staff@hospital.com',
            'first_name': 'Jane',
            'last_name': 'Doe',
            'is_staff': False,
            'is_superuser': False
        }
    )
    if created:
        staff_user.set_password('staff123')
        staff_user.save()
        print("✓ Created staff user")
    else:
        print("✓ Staff user already exists")
    
    # Create sample doctors
    doctor_record, created = Doctor.objects.get_or_create(
        name='Dr. John Smith',
        defaults={
            'specialization': 'General Medicine',
            'contact': '+1-555-0101'
        }
    )
    if created:
        print("✓ Created doctor record: Dr. John Smith")
    else:
        print("✓ Doctor record already exists: Dr. John Smith")
    
    # Create another doctor for variety
    doctor_record2, created = Doctor.objects.get_or_create(
        name='Dr. Sarah Johnson',
        defaults={
            'specialization': 'Cardiology',
            'contact': '+1-555-0102'
        }
    )
    if created:
        print("✓ Created doctor record: Dr. Sarah Johnson")
    else:
        print("✓ Doctor record already exists: Dr. Sarah Johnson")
    
    # Create HospitalUser profiles
    # Admin profile
    admin_profile, created = HospitalUser.objects.get_or_create(
        user=admin_user,
        defaults={
            'role': 'Admin',
            'doctor': None
        }
    )
    if created:
        print("✓ Created admin HospitalUser profile")
    else:
        print("✓ Admin HospitalUser profile already exists")
    
    # Doctor profile
    doctor_profile, created = HospitalUser.objects.get_or_create(
        user=doctor_user,
        defaults={
            'role': 'Doctor',
            'doctor': doctor_record
        }
    )
    if created:
        print("✓ Created doctor HospitalUser profile")
    else:
        print("✓ Doctor HospitalUser profile already exists")
    
    # Staff profile
    staff_profile, created = HospitalUser.objects.get_or_create(
        user=staff_user,
        defaults={
            'role': 'Staff',
            'doctor': None
        }
    )
    if created:
        print("✓ Created staff HospitalUser profile")
    else:
        print("✓ Staff HospitalUser profile already exists")
    
    print("\n" + "="*50)
    print("DEMO USERS CREATED SUCCESSFULLY!")
    print("="*50)
    print("Login Credentials:")
    print("Admin:  admin/admin123")
    print("Doctor: doctor/doctor123")
    print("Staff:  staff/staff123")
    print("="*50)
    print("\nYou can now login to the system at: http://127.0.0.1:8000")

if __name__ == '__main__':
    create_demo_users()
