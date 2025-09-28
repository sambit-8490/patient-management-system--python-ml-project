from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Count
from django.utils import timezone
from datetime import datetime, date
import json

from .models import (
    Patient, Doctor, HospitalUser, Appointment, Treatment, 
    Medication, Prescription, Billing
)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            # Validate HospitalUser profile to prevent redirect loops
            hospital_user = HospitalUser.objects.filter(user=user).first()
            if not hospital_user or hospital_user.role not in ('Admin', 'Doctor', 'Staff'):
                logout(request)
                messages.error(request, 'User profile not found or invalid role. Please contact administrator.')
                return redirect('login')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'hospital_app/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    try:
        hospital_user = HospitalUser.objects.get(user=request.user)
        role = hospital_user.role
    except HospitalUser.DoesNotExist:
        # Break potential login↔dashboard redirect loop by logging out
        logout(request)
        messages.error(request, 'User profile not found. Please contact administrator.')
        return redirect('login')
    
    context = {'role': role}
    
    if role == 'Admin':
        return admin_dashboard(request, context)
    elif role == 'Doctor':
        return doctor_dashboard(request, context)
    elif role == 'Staff':
        return staff_dashboard(request, context)
    else:
        # Invalid role: logout to avoid redirect loop
        logout(request)
        messages.error(request, 'Invalid user role')
        return redirect('login')


def admin_dashboard(request, context):
    # Get all data for admin
    patients_count = Patient.objects.count()
    doctors_count = Doctor.objects.count()
    appointments_count = Appointment.objects.count()
    pending_bills = Billing.objects.filter(payment_status='Pending').count()
    
    recent_appointments = Appointment.objects.select_related('patient', 'doctor').order_by('-appointment_date')[:10]
    recent_patients = Patient.objects.order_by('-PatientID')[:5]
    
    # Statistics for charts
    appointments_by_status = Appointment.objects.values('status').annotate(count=Count('status'))
    payments_by_status = Billing.objects.values('payment_status').annotate(count=Count('payment_status'))
    
    context.update({
        'patients_count': patients_count,
        'doctors_count': doctors_count,
        'appointments_count': appointments_count,
        'pending_bills': pending_bills,
        'recent_appointments': recent_appointments,
        'recent_patients': recent_patients,
        'appointments_by_status': list(appointments_by_status),
        'payments_by_status': list(payments_by_status),
    })
    
    return render(request, 'hospital_app/admin_dashboard.html', context)


def doctor_dashboard(request, context):
    try:
        hospital_user = HospitalUser.objects.get(user=request.user)
        doctor = hospital_user.doctor
        
        if not doctor:
            messages.error(request, 'Doctor profile not found')
            return redirect('login')
        
        # Get doctor's appointments
        today = date.today()
        upcoming_appointments = Appointment.objects.filter(
            doctor=doctor,
            appointment_date__gte=today,
            status='Scheduled'
        ).order_by('appointment_date', 'appointment_time')[:10]
        
        recent_appointments = Appointment.objects.filter(
            doctor=doctor
        ).order_by('-appointment_date')[:5]
        
        # Get patients for this doctor
        patients = Patient.objects.filter(
            appointment__doctor=doctor
        ).distinct()[:10]
        
        context.update({
            'doctor': doctor,
            'upcoming_appointments': upcoming_appointments,
            'recent_appointments': recent_appointments,
            'patients': patients,
        })
        
    except HospitalUser.DoesNotExist:
        messages.error(request, 'Doctor profile not found')
        return redirect('login')
    
    return render(request, 'hospital_app/doctor_dashboard.html', context)


def staff_dashboard(request, context):
    # Staff can see appointments, billing, and patient details
    today = date.today()
    upcoming_appointments = Appointment.objects.filter(
        appointment_date__gte=today,
        status='Scheduled'
    ).select_related('patient', 'doctor').order_by('appointment_date', 'appointment_time')[:10]
    
    pending_bills = Billing.objects.filter(
        payment_status='Pending'
    ).select_related('appointment__patient', 'appointment__doctor')[:10]
    
    recent_patients = Patient.objects.order_by('-PatientID')[:10]
    
    context.update({
        'upcoming_appointments': upcoming_appointments,
        'pending_bills': pending_bills,
        'recent_patients': recent_patients,
    })
    
    return render(request, 'hospital_app/staff_dashboard.html', context)


@login_required
def patients_list(request):
    try:
        hospital_user = HospitalUser.objects.get(user=request.user)
        role = hospital_user.role
    except HospitalUser.DoesNotExist:
        messages.error(request, 'User profile not found')
        return redirect('login')
    
    search_query = request.GET.get('search', '')
    patients = Patient.objects.all()
    
    if search_query:
        patients = patients.filter(
            Q(name__icontains=search_query) |
            Q(contact__icontains=search_query) |
            Q(PatientID__icontains=search_query)
        )
    
    context = {
        'patients': patients,
        'search_query': search_query,
        'role': role,
    }
    
    return render(request, 'hospital_app/patients_list.html', context)


@login_required
def patient_detail(request, PatientID):
    try:
        hospital_user = HospitalUser.objects.get(user=request.user)
        role = hospital_user.role
    except HospitalUser.DoesNotExist:
        messages.error(request, 'User profile not found')
        return redirect('login')
    
    patient = get_object_or_404(Patient, PatientID=PatientID)
    appointments = Appointment.objects.filter(patient=patient).select_related('doctor').order_by('-appointment_date')
    
    context = {
        'patient': patient,
        'appointments': appointments,
        'role': role,
    }
    
    return render(request, 'hospital_app/patient_detail.html', context)


@login_required
def appointments_list(request):
    try:
        hospital_user = HospitalUser.objects.get(user=request.user)
        role = hospital_user.role
    except HospitalUser.DoesNotExist:
        messages.error(request, 'User profile not found')
        return redirect('login')
    
    appointments = Appointment.objects.select_related('patient', 'doctor').order_by('-appointment_date')
    
    # Filter by status if provided
    status_filter = request.GET.get('status', '')
    if status_filter:
        appointments = appointments.filter(status=status_filter)
    
    # Filter by doctor if user is a doctor
    if role == 'Doctor':
        appointments = appointments.filter(doctor=hospital_user.doctor)
    
    context = {
        'appointments': appointments,
        'status_filter': status_filter,
        'role': role,
    }
    
    return render(request, 'hospital_app/appointments_list.html', context)


@login_required
def appointment_detail(request, AppointmentID):
    try:
        hospital_user = HospitalUser.objects.get(user=request.user)
        role = hospital_user.role
    except HospitalUser.DoesNotExist:
        messages.error(request, 'User profile not found')
        return redirect('login')
    
    appointment = get_object_or_404(Appointment, AppointmentID=AppointmentID)
    
    # Check if doctor can only see their own appointments
    if role == 'Doctor' and appointment.doctor != hospital_user.doctor:
        messages.error(request, 'You can only view your own appointments')
        return redirect('appointments_list')
    
    try:
        treatment = Treatment.objects.get(appointment=appointment)
        prescriptions = Prescription.objects.filter(treatment=treatment).select_related('medication')
    except Treatment.DoesNotExist:
        treatment = None
        prescriptions = []
    
    try:
        billing = Billing.objects.get(appointment=appointment)
    except Billing.DoesNotExist:
        billing = None
    
    context = {
        'appointment': appointment,
        'treatment': treatment,
        'prescriptions': prescriptions,
        'billing': billing,
        'role': role,
    }
    
    return render(request, 'hospital_app/appointment_detail.html', context)


@login_required
def add_appointment(request):
    try:
        hospital_user = HospitalUser.objects.get(user=request.user)
        role = hospital_user.role
    except HospitalUser.DoesNotExist:
        messages.error(request, 'User profile not found')
        return redirect('login')
    
    if request.method == 'POST':
        PatientID = request.POST.get('PatientID')
        DoctorID = request.POST.get('DoctorID')
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')
        
        try:
            patient = Patient.objects.get(PatientID=PatientID)
            doctor = Doctor.objects.get(DoctorID=DoctorID)
            
            appointment = Appointment.objects.create(
                patient=patient,
                doctor=doctor,
                appointment_date=appointment_date,
                appointment_time=appointment_time,
                status='Scheduled'
            )
            
            messages.success(request, 'Appointment created successfully')
            return redirect('appointment_detail', AppointmentID=appointment.AppointmentID)
            
        except (Patient.DoesNotExist, Doctor.DoesNotExist):
            messages.error(request, 'Invalid patient or doctor selected')
    
    patients = Patient.objects.all()
    doctors = Doctor.objects.all()
    
    context = {
        'patients': patients,
        'doctors': doctors,
        'role': role,
    }
    
    return render(request, 'hospital_app/add_appointment.html', context)


@login_required
def update_appointment_status(request, AppointmentID):
    if request.method == 'POST':
        appointment = get_object_or_404(Appointment, AppointmentID=AppointmentID)
        new_status = request.POST.get('status')
        
        if new_status in ['Scheduled', 'Completed', 'Cancelled']:
            appointment.status = new_status
            appointment.save()
            messages.success(request, f'Appointment status updated to {new_status}')
        else:
            messages.error(request, 'Invalid status')
    
    return redirect('appointment_detail', AppointmentID=AppointmentID)


@login_required
def billing_list(request):
    try:
        hospital_user = HospitalUser.objects.get(user=request.user)
        role = hospital_user.role
    except HospitalUser.DoesNotExist:
        messages.error(request, 'User profile not found')
        return redirect('login')
    
    bills = Billing.objects.select_related('appointment__patient', 'appointment__doctor').order_by('-billing_date')
    
    # Calculate paid bills count
    paid_count = bills.filter(payment_status='Paid').count()

    # Calculate Pending bills count
    pending_count = bills.filter(payment_status='Pending').count()

    # Calculate Total amount
    if bills.exists():
        # Filter paid bills first, then sum their amounts
        paid_bills = bills.filter(payment_status='Paid')
        total_amount = sum(int(bill.amount) for bill in paid_bills)
    else:
        total_amount = 0
    
    # Filter by payment status if provided
    status_filter = request.GET.get('status', '')
    if status_filter:
        bills = bills.filter(payment_status=status_filter)
    
    context = {
        'bills': bills,
        'status_filter': status_filter,
        'role': role,
        'paid_count': paid_count,
        'pending_count':pending_count,
        'total_amount': total_amount # Add this line
    }
    
    return render(request, 'hospital_app/billing_list.html', context)

@login_required
def update_payment_status(request, BillID):
    if request.method == 'POST':
        bill = get_object_or_404(Billing, BillID=BillID)
        new_status = request.POST.get('payment_status')
        payment_method = request.POST.get('payment_method')
        
        if new_status in ['Paid', 'Pending', 'Cancelled']:
            bill.payment_status = new_status
            if payment_method:
                bill.payment_method = payment_method
            bill.save()
            messages.success(request, f'Payment status updated to {new_status}')
        else:
            messages.error(request, 'Invalid payment status')
    
    return redirect('billing_list')


# API endpoints for AJAX calls
@login_required
def get_patient_data(request, PatientID):
    try:
        patient = Patient.objects.get(PatientID=PatientID)
        data = {
            'name': patient.name,
            'gender': patient.gender,
            'dob': patient.dob.strftime('%Y-%m-%d'),
            'contact': patient.contact,
            'blood_group': patient.blood_group,
        }
        return JsonResponse(data)
    except Patient.DoesNotExist:
        return JsonResponse({'error': 'Patient not found'}, status=404)


@login_required
def get_doctor_schedule(request, DoctorID, date):
    try:
        doctor = Doctor.objects.get(DoctorID=DoctorID)
        appointments = Appointment.objects.filter(
            doctor=doctor,
            appointment_date=date,
            status='Scheduled'
        ).values('appointment_time')
        
        times = [apt['appointment_time'].strftime('%H:%M') for apt in appointments]
        return JsonResponse({'scheduled_times': times})
    except Doctor.DoesNotExist:
        return JsonResponse({'error': 'Doctor not found'}, status=404)


@login_required
def add_patient(request):
    try:
        hospital_user = HospitalUser.objects.get(user=request.user)
        role = hospital_user.role
    except HospitalUser.DoesNotExist:
        messages.error(request, 'User profile not found')
        return redirect('login')
    
    if role not in ['Admin', 'Staff']:
        messages.error(request, 'You do not have permission to add patients')
        return redirect('patients_list')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        contact = request.POST.get('contact')
        blood_group = request.POST.get('blood_group')
        
        try:
            patient = Patient.objects.create(
                name=name,
                gender=gender,
                dob=dob,
                contact=contact,
                blood_group=blood_group
            )
            messages.success(request, f'Patient {patient.name} added successfully')
            return redirect('patient_detail', PatientID=patient.PatientID)
        except Exception as e:
            messages.error(request, f'Error adding patient: {str(e)}')
    
    return redirect('patients_list')


@login_required
def edit_patient(request, PatientID):
    try:
        hospital_user = HospitalUser.objects.get(user=request.user)
        role = hospital_user.role
    except HospitalUser.DoesNotExist:
        messages.error(request, 'User profile not found')
        return redirect('login')
    
    if role not in ['Admin', 'Staff']:
        messages.error(request, 'You do not have permission to edit patients')
        return redirect('patients_list')
    
    patient = get_object_or_404(Patient, PatientID=PatientID)
    
    if request.method == 'POST':
        patient.name = request.POST.get('name')
        patient.gender = request.POST.get('gender')
        patient.dob = request.POST.get('dob')
        patient.contact = request.POST.get('contact')
        patient.blood_group = request.POST.get('blood_group')
        
        try:
            patient.save()
            messages.success(request, f'Patient {patient.name} updated successfully')
            return redirect('patient_detail', PatientID=patient.PatientID)
        except Exception as e:
            messages.error(request, f'Error updating patient: {str(e)}')
    
    return redirect('patient_detail', PatientID=PatientID)


@login_required
def delete_patient(request, PatientID):
    try:
        hospital_user = HospitalUser.objects.get(user=request.user)
        role = hospital_user.role
    except HospitalUser.DoesNotExist:
        messages.error(request, 'User profile not found')
        return redirect('login')
    
    if role != 'Admin':
        messages.error(request, 'Only administrators can delete patients')
        return redirect('patients_list')
    
    patient = get_object_or_404(Patient, PatientID=PatientID)
    
    if request.method == 'POST':
        try:
            patient_name = patient.name
            patient.delete()
            messages.success(request, f'Patient {patient_name} deleted successfully')
        except Exception as e:
            messages.error(request, f'Error deleting patient: {str(e)}')
    
    return redirect('patients_list')


@login_required
def add_treatment(request, AppointmentID):
    try:
        hospital_user = HospitalUser.objects.get(user=request.user)
        role = hospital_user.role
    except HospitalUser.DoesNotExist:
        messages.error(request, 'User profile not found')
        return redirect('login')
    
    if role not in ['Admin', 'Doctor']:
        messages.error(request, 'You do not have permission to add treatments')
        return redirect('appointments_list')
    
    appointment = get_object_or_404(Appointment, AppointmentID=AppointmentID)
    
    # Check if doctor can only treat their own appointments
    if role == 'Doctor' and appointment.doctor != hospital_user.doctor:
        messages.error(request, 'You can only add treatments for your own appointments')
        return redirect('appointment_detail', AppointmentID=AppointmentID)
    
    if request.method == 'POST':
        diagnosis = request.POST.get('diagnosis')
        notes = request.POST.get('notes')
        
        try:
            treatment, created = Treatment.objects.get_or_create(
                appointment=appointment,
                defaults={
                    'diagnosis': diagnosis,
                    'notes': notes
                }
            )
            
            if not created:
                treatment.diagnosis = diagnosis
                treatment.notes = notes
                treatment.save()
            
            messages.success(request, 'Treatment added successfully')
            return redirect('appointment_detail', AppointmentID=AppointmentID)
        except Exception as e:
            messages.error(request, f'Error adding treatment: {str(e)}')
    
    return redirect('appointment_detail', AppointmentID=AppointmentID)
