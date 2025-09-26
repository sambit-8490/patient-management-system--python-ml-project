// Main JavaScript for Patient Management System

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Form validation
    var forms = document.querySelectorAll('.needs-validation');
    Array.prototype.slice.call(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Search functionality
    var searchInputs = document.querySelectorAll('input[type="search"], input[name="search"]');
    searchInputs.forEach(function(input) {
        input.addEventListener('input', function() {
            var searchTerm = this.value.toLowerCase();
            var table = this.closest('.card').querySelector('table');
            if (table) {
                var rows = table.querySelectorAll('tbody tr');
                rows.forEach(function(row) {
                    var text = row.textContent.toLowerCase();
                    if (text.includes(searchTerm)) {
                        row.style.display = '';
                    } else {
                        row.style.display = 'none';
                    }
                });
            }
        });
    });

    // Date picker enhancements
    var dateInputs = document.querySelectorAll('input[type="date"]');
    dateInputs.forEach(function(input) {
        // Set max date to today for date of birth
        if (input.name === 'dob') {
            input.max = new Date().toISOString().split('T')[0];
        }
        
        // Set min date to today for appointment dates
        if (input.name === 'appointment_date') {
            input.min = new Date().toISOString().split('T')[0];
        }
    });

    // Time picker enhancements
    var timeInputs = document.querySelectorAll('input[type="time"]');
    timeInputs.forEach(function(input) {
        input.addEventListener('change', function() {
            validateTimeSlot(this);
        });
    });

    // Patient form auto-fill
    var patientSelect = document.getElementById('patient_id');
    if (patientSelect) {
        patientSelect.addEventListener('change', function() {
            var patientId = this.value;
            if (patientId) {
                fetchPatientData(patientId);
            }
        });
    }

    // Doctor schedule check
    var doctorSelect = document.getElementById('doctor_id');
    var dateInput = document.getElementById('appointment_date');
    if (doctorSelect && dateInput) {
        doctorSelect.addEventListener('change', function() {
            if (dateInput.value) {
                checkDoctorSchedule(this.value, dateInput.value);
            }
        });
        
        dateInput.addEventListener('change', function() {
            if (doctorSelect.value) {
                checkDoctorSchedule(doctorSelect.value, this.value);
            }
        });
    }

    // Status update confirmation
    var statusForms = document.querySelectorAll('form[action*="update-appointment-status"]');
    statusForms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            var statusSelect = this.querySelector('select[name="status"]');
            var currentStatus = statusSelect.dataset.currentStatus;
            var newStatus = statusSelect.value;
            
            if (currentStatus !== newStatus) {
                var confirmMessage = `Are you sure you want to change the status from "${currentStatus}" to "${newStatus}"?`;
                if (!confirm(confirmMessage)) {
                    e.preventDefault();
                }
            }
        });
    });

    // Payment status update confirmation
    var paymentForms = document.querySelectorAll('form[action*="update-payment"]');
    paymentForms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            var statusSelect = this.querySelector('select[name="payment_status"]');
            var currentStatus = statusSelect.dataset.currentStatus;
            var newStatus = statusSelect.value;
            
            if (currentStatus !== newStatus) {
                var confirmMessage = `Are you sure you want to change the payment status from "${currentStatus}" to "${newStatus}"?`;
                if (!confirm(confirmMessage)) {
                    e.preventDefault();
                }
            }
        });
    });

    // Table row click handlers
    var tableRows = document.querySelectorAll('table tbody tr[data-href]');
    tableRows.forEach(function(row) {
        row.addEventListener('click', function() {
            window.location.href = this.dataset.href;
        });
        
        row.style.cursor = 'pointer';
    });

    // Print functionality
    var printButtons = document.querySelectorAll('.btn-print');
    printButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            window.print();
        });
    });

    // Export functionality (placeholder)
    var exportButtons = document.querySelectorAll('.btn-export');
    exportButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            var format = this.dataset.format || 'csv';
            var table = this.closest('.card').querySelector('table');
            if (table) {
                exportTable(table, format);
            }
        });
    });
});

// Helper Functions

function fetchPatientData(patientId) {
    fetch(`/api/patient/${patientId}/`)
        .then(response => response.json())
        .then(data => {
            // Auto-fill patient details in forms
            var nameField = document.getElementById('patient_name');
            var genderField = document.getElementById('patient_gender');
            var dobField = document.getElementById('patient_dob');
            var contactField = document.getElementById('patient_contact');
            var bloodGroupField = document.getElementById('patient_blood_group');
            
            if (nameField) nameField.value = data.name || '';
            if (genderField) genderField.value = data.gender || '';
            if (dobField) dobField.value = data.dob || '';
            if (contactField) contactField.value = data.contact || '';
            if (bloodGroupField) bloodGroupField.value = data.blood_group || '';
        })
        .catch(error => {
            console.error('Error fetching patient data:', error);
        });
}

function checkDoctorSchedule(doctorId, date) {
    fetch(`/api/doctor/${doctorId}/schedule/${date}/`)
        .then(response => response.json())
        .then(data => {
            var timeInput = document.getElementById('appointment_time');
            if (timeInput && data.scheduled_times) {
                // Disable already scheduled times
                var options = timeInput.querySelectorAll('option');
                options.forEach(function(option) {
                    if (data.scheduled_times.includes(option.value)) {
                        option.disabled = true;
                        option.textContent += ' (Booked)';
                    } else {
                        option.disabled = false;
                    }
                });
            }
        })
        .catch(error => {
            console.error('Error checking doctor schedule:', error);
        });
}

function validateTimeSlot(timeInput) {
    var selectedTime = timeInput.value;
    var dateInput = document.getElementById('appointment_date');
    var doctorSelect = document.getElementById('doctor_id');
    
    if (selectedTime && dateInput && doctorSelect) {
        // Check if the selected time slot is available
        checkDoctorSchedule(doctorSelect.value, dateInput.value);
    }
}

function exportTable(table, format) {
    var data = [];
    var headers = [];
    
    // Get headers
    var headerRow = table.querySelector('thead tr');
    if (headerRow) {
        var headerCells = headerRow.querySelectorAll('th');
        headers = Array.from(headerCells).map(cell => cell.textContent.trim());
    }
    
    // Get data rows
    var rows = table.querySelectorAll('tbody tr');
    rows.forEach(function(row) {
        var cells = row.querySelectorAll('td');
        var rowData = Array.from(cells).map(cell => cell.textContent.trim());
        data.push(rowData);
    });
    
    if (format === 'csv') {
        exportToCSV(headers, data);
    } else if (format === 'excel') {
        exportToExcel(headers, data);
    }
}

function exportToCSV(headers, data) {
    var csvContent = headers.join(',') + '\n';
    data.forEach(function(row) {
        csvContent += row.join(',') + '\n';
    });
    
    var blob = new Blob([csvContent], { type: 'text/csv' });
    var url = window.URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = url;
    a.download = 'export.csv';
    a.click();
    window.URL.revokeObjectURL(url);
}

function exportToExcel(headers, data) {
    // This would require a library like SheetJS
    console.log('Excel export not implemented. Use CSV export instead.');
}

// Utility Functions

function showNotification(message, type = 'info') {
    var alertClass = 'alert-' + type;
    var alertHtml = `
        <div class="alert ${alertClass} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    var container = document.querySelector('.container-fluid');
    if (container) {
        container.insertAdjacentHTML('afterbegin', alertHtml);
        
        // Auto-hide after 5 seconds
        setTimeout(function() {
            var alert = container.querySelector('.alert');
            if (alert) {
                var bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }
        }, 5000);
    }
}

function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

function formatDate(dateString) {
    var date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

function formatTime(timeString) {
    var time = new Date('2000-01-01T' + timeString);
    return time.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        hour12: true
    });
}

// Chart.js helper functions
function createDoughnutChart(canvasId, data, options = {}) {
    var ctx = document.getElementById(canvasId).getContext('2d');
    var defaultOptions = {
        type: 'doughnut',
        data: data,
        options: {
            maintainAspectRatio: false,
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    };
    
    var chartOptions = Object.assign({}, defaultOptions, options);
    return new Chart(ctx, chartOptions);
}

function createBarChart(canvasId, data, options = {}) {
    var ctx = document.getElementById(canvasId).getContext('2d');
    var defaultOptions = {
        type: 'bar',
        data: data,
        options: {
            maintainAspectRatio: false,
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    };
    
    var chartOptions = Object.assign({}, defaultOptions, options);
    return new Chart(ctx, chartOptions);
}

// Search and filter functions
function filterTable(tableId, searchTerm, columnIndex = -1) {
    var table = document.getElementById(tableId);
    if (!table) return;
    
    var rows = table.querySelectorAll('tbody tr');
    var term = searchTerm.toLowerCase();
    
    rows.forEach(function(row) {
        var cells = row.querySelectorAll('td');
        var shouldShow = false;
        
        if (columnIndex === -1) {
            // Search all columns
            cells.forEach(function(cell) {
                if (cell.textContent.toLowerCase().includes(term)) {
                    shouldShow = true;
                }
            });
        } else {
            // Search specific column
            if (cells[columnIndex] && cells[columnIndex].textContent.toLowerCase().includes(term)) {
                shouldShow = true;
            }
        }
        
        row.style.display = shouldShow ? '' : 'none';
    });
}

// Real-time updates (WebSocket placeholder)
function initializeRealTimeUpdates() {
    // This would be implemented with WebSockets or Server-Sent Events
    // for real-time updates of appointments, notifications, etc.
    console.log('Real-time updates not implemented yet.');
}

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeRealTimeUpdates();
});





