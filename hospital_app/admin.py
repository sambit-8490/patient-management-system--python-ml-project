from django.contrib import admin
from .models import Patient, Doctor, HospitalUser, Appointment, Treatment, Medication, Prescription, Billing


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('PatientID', 'name', 'gender', 'dob', 'contact', 'blood_group')
    list_filter = ('gender', 'blood_group')
    search_fields = ('name', 'PatientID', 'contact')
    ordering = ('-PatientID',)


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('DoctorID', 'name', 'specialization', 'contact')
    list_filter = ('specialization',)
    search_fields = ('name', 'specialization')
    ordering = ('-DoctorID',)


@admin.register(HospitalUser)
class HospitalUserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'user', 'role', 'doctor')
    list_filter = ('role',)
    search_fields = ('user__username', 'user__email')
    ordering = ('-user_id',)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('AppointmentID', 'patient', 'doctor', 'appointment_date', 'appointment_time', 'status')
    list_filter = ('status', 'appointment_date', 'doctor__specialization')
    search_fields = ('patient__name', 'doctor__name')
    ordering = ('-appointment_date', '-appointment_time')


@admin.register(Treatment)
class TreatmentAdmin(admin.ModelAdmin):
    list_display = ('TreatmentID', 'appointment', 'diagnosis')
    search_fields = ('appointment__patient__name', 'diagnosis')
    ordering = ('-TreatmentID',)


@admin.register(Medication)
class MedicationAdmin(admin.ModelAdmin):
    list_display = ('MedicationID', 'name', 'dosage', 'manufacturer')
    search_fields = ('name', 'manufacturer')
    ordering = ('name',)


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('PrescriptionID', 'treatment', 'medication', 'quantity', 'duration')
    search_fields = ('treatment__appointment__patient__name', 'medication__name')
    ordering = ('-PrescriptionID',)


@admin.register(Billing)
class BillingAdmin(admin.ModelAdmin):
    list_display = ('BillID', 'appointment', 'amount', 'payment_status', 'payment_method', 'billing_date')
    list_filter = ('payment_status', 'payment_method', 'billing_date')
    search_fields = ('appointment__patient__name', 'BillID')
    ordering = ('-billing_date',)





