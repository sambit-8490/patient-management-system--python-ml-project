#!/usr/bin/env python
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from hospital_app.models import HospitalUser, Doctor


class Command(BaseCommand):
    help = 'Create demo users (admin/doctor/staff) and associated HospitalUser profiles and Doctor records.'

    def handle(self, *args, **options):
        self.stdout.write('Creating demo users...')

        # Admin user
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@hospital.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True,
            },
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write('✓ Created admin user')
        else:
            self.stdout.write('✓ Admin user already exists')

        admin_profile, created = HospitalUser.objects.get_or_create(
            user=admin_user,
            defaults={'role': 'Admin', 'doctor': None},
        )
        if created:
            self.stdout.write('✓ Created admin HospitalUser profile')
        else:
            self.stdout.write('✓ Admin HospitalUser profile already exists')

        # Doctor record(s)
        doctor_record, dr_created = Doctor.objects.get_or_create(
            name='Dr. John Smith',
            defaults={'specialization': 'General Medicine', 'contact': '+1-555-0101'},
        )
        self.stdout.write('✓ {} doctor record: Dr. John Smith'.format('Created' if dr_created else 'Existing'))

        # Another doctor for variety
        doctor_record2, dr2_created = Doctor.objects.get_or_create(
            name='Dr. Sarah Johnson',
            defaults={'specialization': 'Cardiology', 'contact': '+1-555-0102'},
        )
        self.stdout.write('✓ {} doctor record: Dr. Sarah Johnson'.format('Created' if dr2_created else 'Existing'))

        # Doctor user
        doctor_user, created = User.objects.get_or_create(
            username='doctor',
            defaults={
                'email': 'doctor@hospital.com',
                'first_name': 'Dr. John',
                'last_name': 'Smith',
                'is_staff': False,
                'is_superuser': False,
            },
        )
        if created:
            doctor_user.set_password('doctor123')
            doctor_user.save()
            self.stdout.write('✓ Created doctor user')
        else:
            self.stdout.write('✓ Doctor user already exists')

        doctor_profile, created = HospitalUser.objects.get_or_create(
            user=doctor_user,
            defaults={'role': 'Doctor', 'doctor': doctor_record},
        )
        if created:
            self.stdout.write('✓ Created doctor HospitalUser profile')
        else:
            # If profile exists without doctor, try to set doctor linkage
            if not doctor_profile.doctor:
                doctor_profile.doctor = doctor_record
                doctor_profile.save()
            self.stdout.write('✓ Doctor HospitalUser profile already exists')

        # Staff user
        staff_user, created = User.objects.get_or_create(
            username='staff',
            defaults={
                'email': 'staff@hospital.com',
                'first_name': 'Jane',
                'last_name': 'Doe',
                'is_staff': False,
                'is_superuser': False,
            },
        )
        if created:
            staff_user.set_password('staff123')
            staff_user.save()
            self.stdout.write('✓ Created staff user')
        else:
            self.stdout.write('✓ Staff user already exists')

        staff_profile, created = HospitalUser.objects.get_or_create(
            user=staff_user,
            defaults={'role': 'Staff', 'doctor': None},
        )
        if created:
            self.stdout.write('✓ Created staff HospitalUser profile')
        else:
            self.stdout.write('✓ Staff HospitalUser profile already exists')

        self.stdout.write('\n' + '=' * 50)
        self.stdout.write('DEMO USERS READY')
        self.stdout.write('=' * 50)
        self.stdout.write('Login Credentials:')
        self.stdout.write('Admin:  admin/admin123')
        self.stdout.write('Doctor: doctor/doctor123')
        self.stdout.write('Staff:  staff/staff123')
        self.stdout.write('=' * 50)