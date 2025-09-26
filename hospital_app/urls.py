from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.dashboard, name='home'),
    
    # Patients
    path('patients/', views.patients_list, name='patients_list'),
    path('patients/<int:PatientID>/', views.patient_detail, name='patient_detail'),
    path('patients/add/', views.add_patient, name='add_patient'),
    path('patients/<int:PatientID>/edit/', views.edit_patient, name='edit_patient'),
    path('patients/<int:PatientID>/delete/', views.delete_patient, name='delete_patient'),
    
    # Appointments
    path('appointments/', views.appointments_list, name='appointments_list'),
    path('appointments/<int:AppointmentID>/', views.appointment_detail, name='appointment_detail'),
    path('appointments/add/', views.add_appointment, name='add_appointment'),
    path('appointments/<int:AppointmentID>/update-status/', views.update_appointment_status, name='update_appointment_status'),
    
    # Treatments
    path('appointments/<int:AppointmentID>/treatment/', views.add_treatment, name='add_treatment'),
    
    # Billing
    path('billing/', views.billing_list, name='billing_list'),
    path('billing/<int:BillID>/update-payment/', views.update_payment_status, name='update_payment_status'),
    
    # API endpoints
    path('api/patient/<int:PatientID>/', views.get_patient_data, name='get_patient_data'),
    path('api/doctor/<int:DoctorID>/schedule/<str:date>/', views.get_doctor_schedule, name='get_doctor_schedule'),
]

