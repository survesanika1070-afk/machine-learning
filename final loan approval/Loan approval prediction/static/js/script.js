// Main JavaScript file for Loan Approval System

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all tooltips
    initializeTooltips();
    
    // Initialize form validations
    initializeFormValidations();
    
    // Initialize auto-hide alerts
    initializeAlerts();
    
    // Initialize loading states
    initializeLoadingStates();
});

// Initialize Bootstrap tooltips
function initializeTooltips() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Form validation functions
function initializeFormValidations() {
    // Signup form validation
    const signupForm = document.getElementById('signupForm');
    if (signupForm) {
        signupForm.addEventListener('submit', validateSignupForm);
    }
    
    // Login form validation
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', validateLoginForm);
    }
    
    // Loan application form validation
    const loanForm = document.getElementById('loanForm');
    if (loanForm) {
        loanForm.addEventListener('submit', validateLoanForm);
        addRealtimeValidation(loanForm);
    }
}

function validateSignupForm(e) {
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm_password').value;
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    
    // Password validation
    if (password.length < 6) {
        showAlert('Password must be at least 6 characters long!', 'danger');
        e.preventDefault();
        return false;
    }
    
    if (password !== confirmPassword) {
        showAlert('Passwords do not match!', 'danger');
        e.preventDefault();
        return false;
    }
    
    // Username validation
    if (username.length < 3) {
        showAlert('Username must be at least 3 characters long!', 'danger');
        e.preventDefault();
        return false;
    }
    
    // Email validation
    if (!isValidEmail(email)) {
        showAlert('Please enter a valid email address!', 'danger');
        e.preventDefault();
        return false;
    }
    
    return true;
}

function validateLoginForm(e) {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    if (!username || !password) {
        showAlert('Please enter both username and password!', 'danger');
        e.preventDefault();
        return false;
    }
    
    return true;
}

function validateLoanForm(e) {
    const form = e.target;
    const formData = new FormData(form);
    
    // Get values
    const age = parseInt(formData.get('age'));
    const income = parseFloat(formData.get('income'));
    const creditHistory = parseFloat(formData.get('credit_history'));
    const loanAmount = parseFloat(formData.get('loan_amount'));
    const loanTerm = parseInt(formData.get('loan_term'));
    
    // Age validation
    if (age < 18 || age > 100) {
        showAlert('Age must be between 18 and 100!', 'danger');
        e.preventDefault();
        return false;
    }
    
    // Income validation
    if (income <= 0) {
        showAlert('Income must be greater than 0!', 'danger');
        e.preventDefault();
        return false;
    }
    
    // Credit history validation
    if (creditHistory < 0 || creditHistory > 1) {
        showAlert('Credit history must be between 0 and 1!', 'danger');
        e.preventDefault();
        return false;
    }
    
    // Loan amount validation
    if (loanAmount <= 0) {
        showAlert('Loan amount must be greater than 0!', 'danger');
        e.preventDefault();
        return false;
    }
    
    // Loan term validation
    if (loanTerm < 12 || loanTerm > 360) {
        showAlert('Loan term must be between 12 and 360 months!', 'danger');
        e.preventDefault();
        return false;
    }
    
    // Business logic validation
    if (loanAmount > income * 10) {
        showAlert('Loan amount cannot exceed 10 times your annual income!', 'warning');
        e.preventDefault();
        return false;
    }
    
    return true;
}

// Add real-time validation to loan form
function addRealtimeValidation(form) {
    const inputs = form.querySelectorAll('input, select');
    
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            validateField(this);
        });
        
        input.addEventListener('input', function() {
            this.classList.remove('is-invalid');
        });
    });
}

function validateField(field) {
    const value = field.value;
    let isValid = true;
    let message = '';
    
    switch(field.id) {
        case 'age':
            const age = parseInt(value);
            if (age < 18 || age > 100) {
                isValid = false;
                message = 'Age must be between 18 and 100';
            }
            break;
            
        case 'income':
            const income = parseFloat(value);
            if (income <= 0) {
                isValid = false;
                message = 'Income must be greater than 0';
            }
            break;
            
        case 'credit_history':
            const credit = parseFloat(value);
            if (credit < 0 || credit > 1) {
                isValid = false;
                message = 'Credit history must be between 0 and 1';
            }
            break;
            
        case 'loan_amount':
            const amount = parseFloat(value);
            if (amount <= 0) {
                isValid = false;
                message = 'Loan amount must be greater than 0';
            }
            break;
            
        case 'loan_term':
            const term = parseInt(value);
            if (term < 12 || term > 360) {
                isValid = false;
                message = 'Loan term must be between 12 and 360 months';
            }
            break;
    }
    
    if (!isValid) {
        field.classList.add('is-invalid');
        showFieldError(field, message);
    } else {
        field.classList.remove('is-invalid');
        removeFieldError(field);
    }
    
    return isValid;
}

function showFieldError(field, message) {
    removeFieldError(field);
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'invalid-feedback';
    errorDiv.textContent = message;
    
    field.parentNode.appendChild(errorDiv);
}

function removeFieldError(field) {
    const existingError = field.parentNode.querySelector('.invalid-feedback');
    if (existingError) {
        existingError.remove();
    }
}

// Alert functions
function initializeAlerts() {
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            if (alert.parentNode) {
                alert.style.transition = 'opacity 0.5s';
                alert.style.opacity = '0';
                setTimeout(() => alert.remove(), 500);
            }
        }, 5000);
    });
}

function showAlert(message, type = 'info') {
    const alertContainer = document.querySelector('.container') || document.body;
    
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    alertContainer.insertBefore(alertDiv, alertContainer.firstChild);
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.style.transition = 'opacity 0.5s';
            alertDiv.style.opacity = '0';
            setTimeout(() => alertDiv.remove(), 500);
        }
    }, 5000);
}

// Loading states
function initializeLoadingStates() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<span class="spinner"></span> Processing...';
                
                // Re-enable after 10 seconds (fallback)
                setTimeout(() => {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = originalText;
                }, 10000);
            }
        });
    });
}

// Utility functions
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

function formatPercentage(value) {
    return (value * 100).toFixed(1) + '%';
}

// Chart initialization (if needed for future enhancements)
function initializeCharts() {
    // Placeholder for future chart functionality
    console.log('Charts initialized');
}

// Export functions for use in other scripts
window.LoanAppUtils = {
    showAlert,
    formatCurrency,
    formatPercentage,
    isValidEmail
};
