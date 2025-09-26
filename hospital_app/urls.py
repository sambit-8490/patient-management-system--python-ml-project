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
    path('patients/<int:patient_id>/', views.patient_detail, name='patient_detail'),
    path('patients/add/', views.add_patient, name='add_patient'),
    path('patients/<int:patient_id>/edit/', views.edit_patient, name='edit_patient'),
    path('patients/<int:patient_id>/delete/', views.delete_patient, name='delete_patient'),
    
    # Appointments
    path('appointments/', views.appointments_list, name='appointments_list'),
    path('appointments/<int:appointment_id>/', views.appointment_detail, name='appointment_detail'),
    path('appointments/add/', views.add_appointment, name='add_appointment'),
    path('appointments/<int:appointment_id>/update-status/', views.update_appointment_status, name='update_appointment_status'),
    
    # Treatments
    path('appointments/<int:appointment_id>/treatment/', views.add_treatment, name='add_treatment'),
    
    # Billing
    path('billing/', views.billing_list, name='billing_list'),
    path('billing/<int:bill_id>/update-payment/', views.update_payment_status, name='update_payment_status'),
    
    # API endpoints
    path('api/patient/<int:patient_id>/', views.get_patient_data, name='get_patient_data'),
    path('api/doctor/<int:doctor_id>/schedule/<str:date>/', views.get_doctor_schedule, name='get_doctor_schedule'),
]

