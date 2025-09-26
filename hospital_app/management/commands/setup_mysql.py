#!/usr/bin/env python
"""
Django management command to setup MySQL database
Run with: python manage.py setup_mysql
"""

from django.core.management.base import BaseCommand
from django.db import connection
import os

class Command(BaseCommand):
    help = 'Setup MySQL database with tables and sample data'

    def handle(self, *args, **options):
        self.stdout.write('Setting up MySQL database...')
        
        try:
            with connection.cursor() as cursor:
                # Create database
                self.stdout.write('Creating database PatientManagementDB...')
                cursor.execute("CREATE DATABASE IF NOT EXISTS PatientManagementDB")
                cursor.execute("USE PatientManagementDB")
                
                # Read and execute clean_hospital_schema.sql
                self.stdout.write('Creating tables from clean_hospital_schema.sql...')
                if os.path.exists('clean_hospital_schema.sql'):
                    with open('clean_hospital_schema.sql', 'r', encoding='utf-8') as file:
                        sql_content = file.read()
                        
                    # Split by semicolon and execute each statement
                    statements = sql_content.split(';')
                    for statement in statements:
                        statement = statement.strip()
                        if statement and not statement.startswith('--') and statement:
                            try:
                                cursor.execute(statement)
                            except Exception as e:
                                if "already exists" not in str(e) and "Duplicate entry" not in str(e):
                                    self.stdout.write(f"Warning: {e}")
                    
                    self.stdout.write('Tables created successfully!')
                else:
                    self.stdout.write('clean_hospital_schema.sql not found!')
                
                # Read and execute clean_sample_data.sql
                self.stdout.write('Loading sample data from clean_sample_data.sql...')
                if os.path.exists('clean_sample_data.sql'):
                    with open('clean_sample_data.sql', 'r', encoding='utf-8') as file:
                        sample_sql = file.read()
                        
                    # Split by semicolon and execute each statement
                    sample_statements = sample_sql.split(';')
                    for statement in sample_statements:
                        statement = statement.strip()
                        if statement and not statement.startswith('--') and statement:
                            try:
                                cursor.execute(statement)
                            except Exception as e:
                                if "already exists" not in str(e) and "Duplicate entry" not in str(e):
                                    self.stdout.write(f"Warning: {e}")
                    
                    self.stdout.write('Sample data loaded successfully!')
                else:
                    self.stdout.write('clean_sample_data.sql not found!')
                
                self.stdout.write(
                    self.style.SUCCESS('MySQL database setup completed!')
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error setting up MySQL: {e}')
            )
            self.stdout.write('Please ensure MySQL is running and accessible.')
