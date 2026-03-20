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
- User profile management with HospitalUser model
- Automated demo user creation

### 🏥 **Patient Management**
- Patient registration and profile management
- Medical history tracking
- Contact information and blood group management
- Patient search and filtering
- Add/Edit/Delete patient functionality

### 📅 **Appointment System**
- Appointment scheduling and management
- Doctor availability checking
- Appointment status tracking (Scheduled, Completed, Cancelled)
- Time slot management
- Treatment documentation for appointments

### 💊 **Medical Records**
- Treatment documentation with diagnosis and notes
- Prescription management with medication details
- Medication tracking with dosage and manufacturer info
- Medical history per patient

### 💰 **Billing System**
- Bill generation and management
- Payment status tracking (Paid, Pending)
- Payment method recording (Card, Cash, UPI, Insurance)
- Financial reporting
- Billing constraints (only for completed appointments)

### 📊 **Analytics & Reporting**
- Dashboard with key metrics and charts
- Real-time statistics
- Export functionality
- Print-friendly reports

## Technology Stack

- **Backend**: Django 4.2.7
- **Database**: MySQL
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Charts**: Chart.js
- **Icons**: Font Awesome 6
- **Styling**: Custom CSS with medical-themed design

## Quick Start

### Option 1: Automated Setup (Recommended)

**For Windows:**
```bash
# Clone the repository
git clone <repository-url>
cd Patient-Management-System-1

# Run the automated setup script
run_server.bat
```

**For Linux/Mac:**
```bash
# Clone the repository
git clone <repository-url>
cd Patient-Management-System-1

# Make script executable and run
chmod +x run_server.sh
./run_server.sh
```

The automated script will:
- Create virtual environment
- Install dependencies
- Run database migrations
- Prompt for creating users via interactive `create_users.py`
- Load sample data
- Start development server

### Option 2: Manual Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### 1. Clone and Setup
```bash
git clone <repository-url>
cd Patient-Management-System-1

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Database Setup
```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Create users interactively (Admin/Doctor/Staff)
python create_users.py

# Load sample data
python manage.py load_sample_data
```

### 3. Start Server
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000` to access the application.

### 4. Quit Server
```bash
CTRL + C 
```

## Default Login Credentials

### User Credentials Pattern
- Username: normalized full name (letters/digits only, lowercase)
- Password: `<normalized_name>123`
- Example: "Dr. John Smith" -> username `drjohnsmith`, password `drjohnsmith123`

## Sample Data

The system comes with pre-loaded sample data including:
- **10 Patients** with complete profiles
- **8 Doctors** across different specializations
- **10 Appointments** (8 completed, 2 scheduled)
- **5 Treatments** with diagnoses
- **8 Medications** with dosage information
- **5 Prescriptions** linking treatments to medications
- **8 Billing Records** for completed appointments

## Project Structure

```
Patient-Management-System-1/
├── manage.py
├── requirements.txt
├── README.md
├── run_server.bat          # Windows setup script
├── run_server.sh           # Linux/Mac setup script
├── create_users.py         # Interactive user creation script
├── MYSQL_SETUP.md          # MySQL setup guide (optional)
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
│   ├── apps.py
│   └── management/
│       └── commands/
│           └── load_sample_data.py
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

## Key Features by Role

### Admin Features
- Complete system overview with statistics
- Manage all patients, doctors, and appointments
- Access billing and financial reports
- System administration and user management
- View comprehensive analytics dashboard

### Doctor Features
- View assigned patients and appointments
- Manage patient medical records and treatments
- Update appointment status
- Access treatment history and prescriptions
- Patient diagnosis and medication management

### Staff Features
- Schedule and manage appointments
- Handle patient registration and updates
- Process billing and payments
- Manage appointment logistics
- Add/edit/delete patient information

### Patient Features
- View personal medical records
- Check appointment history
- Access prescription information
- View billing details and payment status

## API Endpoints

- `GET /api/patient/<id>/` - Get patient data
- `GET /api/doctor/<id>/schedule/<date>/` - Get doctor schedule

## Database Configuration

### SQLite (Default)
No additional configuration required. Database file: `db.sqlite3`

### MySQL (Optional)
Update `patient_management/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'PatientManagementDB',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}
```

### MySQL Setup (Integrated)

1. Install MySQL Server 8.x and start the MySQL service.
   - Download from `https://dev.mysql.com/downloads/mysql/` or use XAMPP/WAMP.

2. Create the database (from MySQL shell or Workbench):
   ```sql
   CREATE DATABASE PatientManagementDB;
   ```

3. (Optional) Import schema and sample data via the combined script:
   ```bash
   # From the project root
   mysql -u root -p -h localhost -P 3306 PatientManagementDB < combined_schema_and_data.sql
   ```

4. Configure Django to use MySQL (see snippet above) and then apply migrations:
   ```bash
   python manage.py migrate
   # If tables already exist, you can reconcile with
   python manage.py migrate --fake-initial
   ```

5. Create users:
   ```bash
   python manage.py createsuperuser
   python create_users.py   # Admin/Doctor/Staff interactively
   ```



   
Using docker create admin,user:

docker exec -it django_app python create_users.py





Troubleshooting:
- Access denied: verify credentials and MySQL is running.
- `mysql` not found: add MySQL bin to PATH or run from MySQL Shell.
- Database already exists: safe to ignore; proceed with migrations and `--fake-initial` if needed.

## Management Commands

### Load Sample Data
```bash
python manage.py load_sample_data
```

### Create Users (Interactive)
```bash
python create_users.py
```

## Customization

### Adding New Roles
1. Update `ROLE_CHOICES` in `hospital_app/models.py`
2. Create corresponding dashboard template
3. Update view logic in `hospital_app/views.py`
4. Add URL patterns in `hospital_app/urls.py`

### Styling
- Modify `static/css/style.css` for custom styling
- Update Bootstrap classes in templates
- Add custom JavaScript in `static/js/main.js`
- Login page features medical-themed green design

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
- Secure session management

## Troubleshooting

### Common Issues

1. **Login Issues**: Run `python create_users.py` to create users
2. **No Data**: Run `python manage.py load_sample_data` to load sample data
3. **Database Errors**: Run `python manage.py migrate` to apply migrations
4. **Permission Errors**: Ensure proper role assignments in HospitalUser model

### Reset Database
```bash
# Delete database file (SQLite)
rm db.sqlite3

# Recreate and migrate
python manage.py migrate

# Create users and load data
python create_users.py
python manage.py load_sample_data
```

## Getting Started (New Users)

1. Install prerequisites: Python 3.9+, Git, and MySQL 8.x (optional; SQLite works by default).
2. Clone and enter the project directory:
   - `git clone <repository-url>`
   - `cd Patient-Management-System-1`
3. Create and activate a virtual environment, then install dependencies:
   - Windows: `python -m venv venv && .\\venv\\Scripts\\activate && pip install -r requirements.txt`
   - macOS/Linux: `python -m venv venv && source venv/bin/activate && pip install -r requirements.txt`
4. Database:
   - SQLite (default): no setup required.
   - MySQL: update `patient_management/settings.py` credentials or follow `MYSQL_SETUP.md`.
5. Initialize the DB: `python manage.py migrate`.
6. Create users:
   - Superuser: `python manage.py createsuperuser`.
   - Additional Admin/Doctor/Staff: `python create_users.py` (username derived from name; password `<normalized_name>123`).
7. Optional sample data: `python manage.py load_sample_data`.
8. Start the server: `python manage.py runserver` and open `http://127.0.0.1:8000`.

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
- [ ] MySQL integration with proper authentication
- [ ] Docker containerization
- [ ] Automated testing suite
