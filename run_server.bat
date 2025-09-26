

@echo off
echo Starting Patient Management System...
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Install requirements
echo Installing requirements...
pip install -r requirements.txt

REM Check MySQL connection
echo Checking MySQL database connection...
python -c "import mysql.connector; mysql.connector.connect(host='localhost', user='root', password='14680', database='PatientManagementDB')" 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Cannot connect to MySQL database!
    echo Please ensure MySQL is running and the database 'PatientManagementDB' exists.
    echo You can create the database using the clean_hospital_schema.sql file.
    pause
    exit /b 1
)

REM Run migrations
echo Running database migrations...
python manage.py makemigrations
python manage.py migrate

REM Setup MySQL database schema
echo Setting up MySQL database schema...
python manage.py setup_mysql

REM Create superuser if it doesn't exist
echo Creating superuser (if not exists)...
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin123')"

REM Create demo users with HospitalUser profiles
echo Creating demo users...
python create_demo_users.py

REM Load sample data
echo Loading sample data...
python manage.py load_sample_data

REM Start server
echo Starting Django development server...
echo.
echo Server will be available at: http://127.0.0.1:8000
echo Press Ctrl+C to stop the server
echo.
python manage.py runserver




