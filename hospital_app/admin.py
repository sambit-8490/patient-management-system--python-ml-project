from django.contrib import admin
from .models import Patient, Doctor, HospitalUser, Appointment, Treatment, Medication, Prescription, Billing


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('patient_id', 'name', 'gender', 'dob', 'contact', 'blood_group')
    list_filter = ('gender', 'blood_group')
    search_fields = ('name', 'patient_id', 'contact')
    ordering = ('-patient_id',)


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('doctor_id', 'name', 'specialization', 'contact')
    list_filter = ('specialization',)
    search_fields = ('name', 'specialization')
    ordering = ('-doctor_id',)


@admin.register(HospitalUser)
class HospitalUserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'user', 'role', 'doctor')
    list_filter = ('role',)
    search_fields = ('user__username', 'user__email')
    ordering = ('-user_id',)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('appointment_id', 'patient', 'doctor', 'appointment_date', 'appointment_time', 'status')
    list_filter = ('status', 'appointment_date', 'doctor__specialization')
    search_fields = ('patient__name', 'doctor__name')
    ordering = ('-appointment_date', '-appointment_time')


@admin.register(Treatment)
class TreatmentAdmin(admin.ModelAdmin):
    list_display = ('treatment_id', 'appointment', 'diagnosis')
    search_fields = ('appointment__patient__name', 'diagnosis')
    ordering = ('-treatment_id',)


@admin.register(Medication)
class MedicationAdmin(admin.ModelAdmin):
    list_display = ('medication_id', 'name', 'dosage', 'manufacturer')
    search_fields = ('name', 'manufacturer')
    ordering = ('name',)


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('prescription_id', 'treatment', 'medication', 'quantity', 'duration')
    search_fields = ('treatment__appointment__patient__name', 'medication__name')
    ordering = ('-prescription_id',)


@admin.register(Billing)
class BillingAdmin(admin.ModelAdmin):
    list_display = ('bill_id', 'appointment', 'amount', 'payment_status', 'payment_method', 'billing_date')
    list_filter = ('payment_status', 'payment_method', 'billing_date')
    search_fields = ('appointment__patient__name', 'bill_id')
    ordering = ('-billing_date',)




