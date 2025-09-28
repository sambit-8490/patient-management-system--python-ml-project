#!/usr/bin/env python
import re
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from hospital_app.models import Doctor, HospitalUser


def _normalize_username(full_name: str) -> str:
    return re.sub(r"[^A-Za-z0-9]", "", full_name).lower()


class Command(BaseCommand):
    help = 'Create/Link Django users for all doctors from MySQL Doctors table'

    def handle(self, *args, **options):
        created_users = 0
        linked_profiles = 0

        for doctor in Doctor.objects.all():
            username = _normalize_username(doctor.name)
            password = f"{username}123"

            # Attempt to split name into first and last by space
            parts = [p for p in re.split(r"\s+", doctor.name.strip()) if p]
            # Remove common prefixes like 'Dr' or 'Dr.'
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
                created_users += 1

            hospital_user, profile_created = HospitalUser.objects.get_or_create(
                user=user,
                defaults={'role': 'Doctor', 'doctor': doctor},
            )
            if profile_created:
                linked_profiles += 1

            self.stdout.write(
                f"Doctor: {doctor.name} -> username='{username}' password='{password}'"
            )

        self.stdout.write(self.style.SUCCESS(
            f"Completed linking. New users: {created_users}, new profiles: {linked_profiles}."
        ))