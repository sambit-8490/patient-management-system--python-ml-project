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
from typing import List, Tuple


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


def list_session_credentials(session_creds: List[Tuple[str, str, str]]) -> None:
    if not session_creds:
        print("\nNo credentials created in this session yet.\n")
        return
    print("\n=== Credentials Created in This Session ===")
    for role, username, password in session_creds:
        print(f"- {role}: username='{username}'  password='{password}'")
    print("")


def list_all_credentials() -> None:
    """Show all user login credentials (username and default password rule).

    Notes:
    - Passwords are stored hashed; we cannot read actual passwords.
    - We show the default password based on the rule '<username>123'.
    - If the password was changed later, the default may not work.
    """
    _bootstrap_django()
    from hospital_app.models import HospitalUser

    profiles = HospitalUser.objects.select_related('user', 'doctor').all()
    if not profiles:
        print("\nNo HospitalUser profiles found in the database.\n")
        return

    print("\n=== All User Credentials (by default rule) ===")
    print("Note: If passwords were changed, the defaults below may not work.\n")
    for p in profiles:
        username = p.user.username
        role = p.role
        default_password = f"{username}123"
        line = f"- {role}: username='{username}'  default_password='{default_password}'"
        # For doctors, also show normalized from doctor name if it differs
        if p.doctor is not None:
            doc_username = _normalize_username(p.doctor.name)
            if doc_username != username:
                line += f"  (doctor_name_normalized='{doc_username}' -> '{doc_username}123')"
        print(line)
    print("")


def delete_credentials_by_username() -> None:
    """Delete a user's login credentials (Django User) by username.
    Also deletes the associated HospitalUser profile if present.
    Doctor records are NOT deleted.
    """
    _bootstrap_django()
    from django.contrib.auth.models import User
    from hospital_app.models import HospitalUser

    username = input("Enter the username to delete: ").strip()
    if not username:
        print("Username cannot be empty.\n")
        return

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        print(f"\nUser '{username}' does not exist.\n")
        return

    # Fetch role if HospitalUser exists
    try:
        profile = HospitalUser.objects.get(user=user)
        role = profile.role
    except HospitalUser.DoesNotExist:
        profile = None
        role = '(no profile)'

    print("\nUser found:")
    print(f"- username: {user.username}")
    print(f"- role: {role}")
    if user.is_superuser:
        print("- WARNING: This is a superuser account.")

    confirm = input("Type 'DELETE' to confirm deletion: ").strip()
    if confirm != 'DELETE':
        print("Deletion cancelled.\n")
        return

    # Delete HospitalUser first (if exists), then the auth user
    if profile:
        profile.delete()
    user.delete()
    print(f"\n✓ Deleted credentials for '{username}'. HospitalUser profile removed if present.\n")


def _prompt_non_empty(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Value cannot be empty. Please try again.")


def main() -> None:
    print("\n=== Patient Management System: Create Users ===\n")
    session_created: List[Tuple[str, str, str]] = []  # (role, username, password)
    while True:
        print("Choose an option:")
        print("  1) Create Admin")
        print("  2) Create Doctor")
        print("  3) Create Staff")
        print("  4) Show session-created credentials")
        print("  5) Show ALL user credentials (default rule)")
        print("  6) Delete credentials by username")
        print("  7) Exit")

        choice = input("Enter choice [1-7]: ").strip()

        if choice == '1':
            full_name = _prompt_non_empty("Admin full name: ")
            email = input("Email (optional): ").strip()
            username, password = create_admin(full_name, email=email)
            print(f"\n✓ Admin created/exists -> username: {username}  password: {password}\n")
            session_created.append(("Admin", username, password))

        elif choice == '2':
            full_name = _prompt_non_empty("Doctor full name: ")
            specialization = _prompt_non_empty("Specialization: ")
            contact = input("Contact (optional): ").strip()
            email = input("Email (optional): ").strip()
            username, password = create_doctor(full_name, specialization, contact=contact, email=email)
            print(f"\n✓ Doctor created/exists -> username: {username}  password: {password}\n")
            session_created.append(("Doctor", username, password))

        elif choice == '3':
            full_name = _prompt_non_empty("Staff full name: ")
            email = input("Email (optional): ").strip()
            username, password = create_staff(full_name, email=email)
            print(f"\n✓ Staff created/exists -> username: {username}  password: {password}\n")
            session_created.append(("Staff", username, password))

        elif choice == '4':
            list_session_credentials(session_created)

        elif choice == '5':
            list_all_credentials()

        elif choice == '6':
            delete_credentials_by_username()

        elif choice == '7':
            print("Goodbye!")
            return
        else:
            print("Invalid choice. Please enter 1, 2, 3, 4, 5, or 6.\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted. Exiting.")