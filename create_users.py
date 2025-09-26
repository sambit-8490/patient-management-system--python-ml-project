#!/usr/bin/env python
"""
Interactive user/role creation utility for Patient Management System.

Features:
- Create Admin, Doctor, or Staff users.
- Username is derived from the person's name (letters only, lowercase).
- Password is "<normalized_name>123" (e.g., "johnsmith123").
- Doctors also get a `Doctors` record and are linked in `Users` table.

Run with:
  python create_users.py
"""

import os
import re
import sys


def _bootstrap_django() -> None:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patient_management.settings')
    import django  # lazy import to avoid cost when showing help
    django.setup()


def _normalize_username(full_name: str) -> str:
    # keep letters and digits only; remove spaces and punctuation; lowercase
    letters_digits = re.sub(r"[^A-Za-z0-9]", "", full_name)
    return letters_digits.lower()


def _generate_password_from_name(full_name: str) -> str:
    return f"{_normalize_username(full_name)}123"


def _create_or_get_user(username: str, password: str, *, is_staff: bool, is_superuser: bool, first_name: str = "", last_name: str = "", email: str = ""):
    from django.contrib.auth.models import User

    user, created = User.objects.get_or_create(
        username=username,
        defaults={
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'is_staff': is_staff,
            'is_superuser': is_superuser,
        },
    )
    if created:
        user.set_password(password)
        user.save()
    return user, created


def create_admin(admin_full_name: str, email: str = "") -> tuple[str, str]:
    _bootstrap_django()
    from hospital_app.models import HospitalUser

    username = _normalize_username(admin_full_name)
    password = _generate_password_from_name(admin_full_name)

    first, _, last = admin_full_name.strip().partition(" ")
    user, created = _create_or_get_user(
        username,
        password,
        is_staff=True,
        is_superuser=True,
        first_name=first,
        last_name=last,
        email=email,
    )

    HospitalUser.objects.get_or_create(
        user=user,
        defaults={'role': 'Admin', 'doctor': None},
    )

    return username, password


def create_doctor(doctor_full_name: str, specialization: str, contact: str = "", email: str = "") -> tuple[str, str]:
    _bootstrap_django()
    from hospital_app.models import HospitalUser, Doctor

    username = _normalize_username(doctor_full_name)
    password = _generate_password_from_name(doctor_full_name)

    first, _, last = doctor_full_name.strip().partition(" ")
    user, created = _create_or_get_user(
        username,
        password,
        is_staff=False,
        is_superuser=False,
        first_name=first,
        last_name=last,
        email=email,
    )

    doctor, _ = Doctor.objects.get_or_create(
        name=doctor_full_name,
        defaults={'specialization': specialization, 'contact': contact},
    )

    HospitalUser.objects.get_or_create(
        user=user,
        defaults={'role': 'Doctor', 'doctor': doctor},
    )

    return username, password


def create_staff(staff_full_name: str, email: str = "") -> tuple[str, str]:
    _bootstrap_django()
    from hospital_app.models import HospitalUser

    username = _normalize_username(staff_full_name)
    password = _generate_password_from_name(staff_full_name)

    first, _, last = staff_full_name.strip().partition(" ")
    user, created = _create_or_get_user(
        username,
        password,
        is_staff=False,
        is_superuser=False,
        first_name=first,
        last_name=last,
        email=email,
    )

    HospitalUser.objects.get_or_create(
        user=user,
        defaults={'role': 'Staff', 'doctor': None},
    )

    return username, password


def _prompt_non_empty(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Value cannot be empty. Please try again.")


def main() -> None:
    print("\n=== Patient Management System: Create Users ===\n")
    while True:
        print("Choose an option:")
        print("  1) Create Admin")
        print("  2) Create Doctor")
        print("  3) Create Staff")
        print("  4) Exit")

        choice = input("Enter choice [1-4]: ").strip()

        if choice == '1':
            full_name = _prompt_non_empty("Admin full name: ")
            email = input("Email (optional): ").strip()
            username, password = create_admin(full_name, email=email)
            print(f"\n✓ Admin created/exists -> username: {username}  password: {password}\n")

        elif choice == '2':
            full_name = _prompt_non_empty("Doctor full name: ")
            specialization = _prompt_non_empty("Specialization: ")
            contact = input("Contact (optional): ").strip()
            email = input("Email (optional): ").strip()
            username, password = create_doctor(full_name, specialization, contact=contact, email=email)
            print(f"\n✓ Doctor created/exists -> username: {username}  password: {password}\n")

        elif choice == '3':
            full_name = _prompt_non_empty("Staff full name: ")
            email = input("Email (optional): ").strip()
            username, password = create_staff(full_name, email=email)
            print(f"\n✓ Staff created/exists -> username: {username}  password: {password}\n")

        elif choice == '4':
            print("Goodbye!")
            return
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted. Exiting.")


