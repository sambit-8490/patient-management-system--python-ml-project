#!/usr/bin/env python
import re
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from hospital_app.models import HospitalUser, Doctor


class Command(BaseCommand):
    help = 'Create admin user and link ALL doctors in DB to Django users (no hardcoded demo users)'

    def handle(self, *args, **options):
        self.stdout.write('Creating admin (if missing) and linking all doctors to users...')

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

        # Link ALL doctors from DB to Django users
        def _normalize_username(full_name: str) -> str:
            return re.sub(r"[^A-Za-z0-9]", "", full_name).lower()

        new_users = 0
        new_profiles = 0

        for doctor in Doctor.objects.all():
            username = _normalize_username(doctor.name)
            password = f"{username}123"

            # Split name into first/last and strip 'Dr' prefix if present
            parts = [p for p in re.split(r"\s+", doctor.name.strip()) if p]
            if parts and parts[0].lower().startswith('dr'):
                parts = parts[1:]
            first_name = parts[0] if parts else ''
            last_name = ' '.join(parts[1:]) if len(parts) > 1 else ''

            user, user_created = User.objects.get_or_create(
                username=username,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'is_staff': False,
                    'is_superuser': False,
                },
            )
            if user_created:
                user.set_password(password)
                user.save()
                new_users += 1

            hospital_user, profile_created = HospitalUser.objects.get_or_create(
                user=user,
                defaults={'role': 'Doctor', 'doctor': doctor},
            )
            if profile_created:
                new_profiles += 1

            self.stdout.write(
                f"Doctor: {doctor.name} -> username='{username}' password='{password}'"
            )

        self.stdout.write('\n' + '=' * 50)
        self.stdout.write('Linking complete')
        self.stdout.write('=' * 50)
        self.stdout.write(self.style.SUCCESS(
            f"New doctor users: {new_users}, new profiles: {new_profiles}"
        ))