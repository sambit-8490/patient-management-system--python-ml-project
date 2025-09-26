# Patient Management System

A comprehensive Django-based Patient Management System with role-based access control for hospitals and medical facilities.

## Features

### 🏥 **Multi-Role Dashboard**
- **Admin Dashboard**: Complete system overview with statistics and charts
- **Doctor Dashboard**: Patient management and appointment scheduling
- **Staff Dashboard**: Appointment and billing management
- **Patient Portal**: Personal medical records and appointment history

### 👥 **User Management**
- Role-based authentication (Admin, Doctor, Staff, Patient)
- Secure login system with session management
- User profile management

### 🏥 **Patient Management**
- Patient registration and profile management
- Medical history tracking
- Contact information and blood group management
- Patient search and filtering

### 📅 **Appointment System**
- Appointment scheduling and management
- Doctor availability checking
- Appointment status tracking (Scheduled, Completed, Cancelled)
- Time slot management

### 💊 **Medical Records**
- Treatment documentation
- Diagnosis recording
- Prescription management
- Medication tracking

### 💰 **Billing System**
- Bill generation and management
- Payment status tracking
- Payment method recording
- Financial reporting

### 📊 **Analytics & Reporting**
- Dashboard with key metrics
- Chart visualizations
- Export functionality (CSV)
- Print-friendly reports

## Technology Stack

- **Backend**: Django 4.2.7
- **Database**: MySQL
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Charts**: Chart.js
- **Icons**: Font Awesome 6

## Installation & Setup

### Prerequisites
- Python 3.8+
- MySQL 5.7+
- pip (Python package manager)

### 1. Clone the Repository
```bash
git clone <repository-url>
cd Patient-Management-System-1
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup
1. Create MySQL database:
```sql
CREATE DATABASE PatientManagementDB;
```

2. Update database settings in `patient_management/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'PatientManagementDB',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

3. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser
```bash
python manage.py createsuperuser
```

### 6. Load Sample Data (Optional)
```bash
# Run the SQL script to create sample data
mysql -u your_username -p PatientManagementDB < HospitalManagementDB.sql
```

### 7. Run Development Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` to access the application.

## Default Login Credentials

### Demo Users (Create these in Django Admin)
- **Admin**: admin/admin123
- **Doctor**: doctor/doctor123  
- **Staff**: staff/staff123

## Project Structure

```
Patient-Management-System-1/
├── manage.py
├── requirements.txt
├── README.md
├── patient_management/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── hospital_app/
│   ├── __init__.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── apps.py
├── templates/
│   ├── base.html
│   └── hospital_app/
│       ├── login.html
│       ├── admin_dashboard.html
│       ├── doctor_dashboard.html
│       ├── staff_dashboard.html
│       ├── patients_list.html
│       ├── patient_detail.html
│       ├── appointments_list.html
│       ├── appointment_detail.html
│       ├── add_appointment.html
│       └── billing_list.html
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
└── HospitalManagementDB.sql
```

## Usage Guide

### Admin Features
- View complete system statistics
- Manage all patients, doctors, and appointments
- Access billing and financial reports
- System administration

### Doctor Features
- View assigned patients and appointments
- Manage patient medical records
- Update appointment status
- Access treatment history

### Staff Features
- Schedule and manage appointments
- Handle patient registration
- Process billing and payments
- Manage appointment logistics

### Patient Features
- View personal medical records
- Check appointment history
- Access prescription information
- View billing details

## API Endpoints

- `GET /api/patient/<id>/` - Get patient data
- `GET /api/doctor/<id>/schedule/<date>/` - Get doctor schedule

## Customization

### Adding New Roles
1. Update `ROLE_CHOICES` in `hospital_app/models.py`
2. Create corresponding dashboard template
3. Update view logic in `hospital_app/views.py`

### Styling
- Modify `static/css/style.css` for custom styling
- Update Bootstrap classes in templates
- Add custom JavaScript in `static/js/main.js`

### Database Schema
- Models are defined in `hospital_app/models.py`
- Run `python manage.py makemigrations` after changes
- Apply with `python manage.py migrate`

## Security Features

- CSRF protection on all forms
- User authentication and authorization
- Role-based access control
- SQL injection prevention
- XSS protection

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions, please contact the development team or create an issue in the repository.

## Future Enhancements

- [ ] Real-time notifications
- [ ] Mobile app integration
- [ ] Advanced reporting
- [ ] Email/SMS notifications
- [ ] Document management
- [ ] Integration with medical devices
- [ ] Multi-language support
- [ ] Advanced analytics dashboard