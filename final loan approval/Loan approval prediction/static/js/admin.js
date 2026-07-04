// Admin Dashboard JavaScript

document.addEventListener('DOMContentLoaded', function() {
    initializeAdminDashboard();
});

function initializeAdminDashboard() {
    console.log('🚀 Admin Dashboard Initialized');
    
    // Initialize all admin features
    initializeTabSwitching();
    initializeSearchFunctionality();
    initializeTableSorting();
    initializeActionButtons();
    initializeRealTimeUpdates();
    initializeDataExport();
    initializeTooltips();
    initializeAnimations();
}

// Tab Switching Functionality
function initializeTabSwitching() {
    const tabButtons = document.querySelectorAll('[data-bs-toggle="tab"]');
    
    tabButtons.forEach(button => {
        button.addEventListener('shown.bs.tab', function(e) {
            const target = e.target.getAttribute('data-bs-target');
            console.log(`📊 Switched to tab: ${target}`);
            
            // Add animation to tab content
            const tabContent = document.querySelector(target);
            if (tabContent) {
                tabContent.classList.add('fade-in');
                setTimeout(() => tabContent.classList.remove('fade-in'), 500);
            }
        });
    });
}

// Search Functionality
function initializeSearchFunctionality() {
    const searchInputs = document.querySelectorAll('.search-input');
    
    searchInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            const searchTerm = e.target.value.toLowerCase();
            const tableId = e.target.getAttribute('data-table');
            const table = document.getElementById(tableId);
            
            if (table) {
                const rows = table.querySelectorAll('tbody tr');
                let visibleCount = 0;
                
                rows.forEach(row => {
                    const text = row.textContent.toLowerCase();
                    if (text.includes(searchTerm)) {
                        row.style.display = '';
                        visibleCount++;
                    } else {
                        row.style.display = 'none';
                    }
                });
                
                // Update search results count
                updateSearchResults(visibleCount, rows.length);
            }
        });
    });
}

function updateSearchResults(visible, total) {
    const resultsDiv = document.getElementById('search-results');
    if (resultsDiv) {
        resultsDiv.textContent = `Showing ${visible} of ${total} results`;
    }
}

// Table Sorting
function initializeTableSorting() {
    const sortableHeaders = document.querySelectorAll('.sortable');
    
    sortableHeaders.forEach(header => {
        header.addEventListener('click', function() {
            const table = this.closest('table');
            const tbody = table.querySelector('tbody');
            const rows = Array.from(tbody.querySelectorAll('tr'));
            const columnIndex = Array.from(this.parentNode.children).indexOf(this);
            const isAscending = !this.classList.contains('sort-asc');
            
            // Remove previous sort classes
            table.querySelectorAll('.sortable').forEach(h => {
                h.classList.remove('sort-asc', 'sort-desc');
            });
            
            // Add current sort class
            this.classList.add(isAscending ? 'sort-asc' : 'sort-desc');
            
            // Sort rows
            rows.sort((a, b) => {
                const aText = a.children[columnIndex].textContent.trim();
                const bText = b.children[columnIndex].textContent.trim();
                
                // Try to parse as number
                const aNum = parseFloat(aText.replace(/[^0-9.-]/g, ''));
                const bNum = parseFloat(bText.replace(/[^0-9.-]/g, ''));
                
                if (!isNaN(aNum) && !isNaN(bNum)) {
                    return isAscending ? aNum - bNum : bNum - aNum;
                }
                
                // Sort as text
                return isAscending ? 
                    aText.localeCompare(bText) : 
                    bText.localeCompare(aText);
            });
            
            // Reorder rows
            rows.forEach(row => tbody.appendChild(row));
        });
    });
}

// Action Buttons
function initializeActionButtons() {
    // View buttons
    document.querySelectorAll('.btn-view').forEach(button => {
        button.addEventListener('click', function() {
            const userId = this.getAttribute('data-user-id');
            const applicationId = this.getAttribute('data-application-id');
            
            if (userId) {
                viewUserDetails(userId);
            } else if (applicationId) {
                viewApplicationDetails(applicationId);
            }
        });
    });
    
    // Edit buttons
    document.querySelectorAll('.btn-edit').forEach(button => {
        button.addEventListener('click', function() {
            const id = this.getAttribute('data-id');
            const type = this.getAttribute('data-type');
            
            if (type === 'user') {
                editUser(id);
            } else if (type === 'application') {
                editApplication(id);
            }
        });
    });
    
    // Delete buttons
    document.querySelectorAll('.btn-delete').forEach(button => {
        button.addEventListener('click', function() {
            const id = this.getAttribute('data-id');
            const type = this.getAttribute('data-type');
            
            confirmDelete(id, type);
        });
    });
}

// View User Details
function viewUserDetails(userId) {
    console.log(`👤 Viewing user details for ID: ${userId}`);
    
    // Show loading
    showLoadingModal();
    
    // Simulate API call
    setTimeout(() => {
        hideLoadingModal();
        showUserModal(userId);
    }, 500);
}

function showUserModal(userId) {
    const modal = document.createElement('div');
    modal.className = 'modal fade';
    modal.innerHTML = `
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">User Details</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <div class="text-center">
                        <div class="spinner-border text-primary" role="status">
                            <span class="visually-hidden">Loading...</span>
                        </div>
                        <p class="mt-2">Loading user details...</p>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    const bsModal = new bootstrap.Modal(modal);
    bsModal.show();
    
    // Remove modal from DOM after hidden
    modal.addEventListener('hidden.bs.modal', () => {
        document.body.removeChild(modal);
    });
}

// View Application Details
function viewApplicationDetails(applicationId) {
    console.log(`📋 Viewing application details for ID: ${applicationId}`);
    
    // Show loading
    showLoadingModal();
    
    // Simulate API call
    setTimeout(() => {
        hideLoadingModal();
        showApplicationModal(applicationId);
    }, 500);
}

function showApplicationModal(applicationId) {
    const modal = document.createElement('div');
    modal.className = 'modal fade';
    modal.innerHTML = `
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Application Details</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <div class="text-center">
                        <div class="spinner-border text-primary" role="status">
                            <span class="visually-hidden">Loading...</span>
                        </div>
                        <p class="mt-2">Loading application details...</p>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    const bsModal = new bootstrap.Modal(modal);
    bsModal.show();
    
    // Remove modal from DOM after hidden
    modal.addEventListener('hidden.bs.modal', () => {
        document.body.removeChild(modal);
    });
}

// Edit Functions
function editUser(userId) {
    console.log(`✏️ Editing user: ${userId}`);
    showNotification('Edit functionality coming soon!', 'info');
}

function editApplication(applicationId) {
    console.log(`✏️ Editing application: ${applicationId}`);
    showNotification('Edit functionality coming soon!', 'info');
}

// Delete Confirmation
function confirmDelete(id, type) {
    const modal = document.createElement('div');
    modal.className = 'modal fade';
    modal.innerHTML = `
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Confirm Delete</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <p>Are you sure you want to delete this ${type}? This action cannot be undone.</p>
                    <div class="alert alert-warning">
                        <strong>Warning:</strong> This will permanently delete the ${type} and all associated data.
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                    <button type="button" class="btn btn-danger" onclick="deleteItem('${id}', '${type}')">Delete</button>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    const bsModal = new bootstrap.Modal(modal);
    bsModal.show();
    
    // Remove modal from DOM after hidden
    modal.addEventListener('hidden.bs.modal', () => {
        document.body.removeChild(modal);
    });
}

function deleteItem(id, type) {
    console.log(`🗑️ Deleting ${type}: ${id}`);
    
    // Simulate deletion
    setTimeout(() => {
        showNotification(`${type} deleted successfully!`, 'success');
        
        // Close modal
        const modal = document.querySelector('.modal.show');
        if (modal) {
            bootstrap.Modal.getInstance(modal).hide();
        }
        
        // Refresh data
        refreshTableData(type);
    }, 1000);
}

// Real-time Updates
function initializeRealTimeUpdates() {
    // Simulate real-time updates every 30 seconds
    setInterval(() => {
        updateStats();
        console.log('📊 Stats updated');
    }, 30000);
}

function updateStats() {
    // Update stats cards with animation
    const statCards = document.querySelectorAll('.stats-card h3');
    statCards.forEach(card => {
        const currentValue = parseInt(card.textContent);
        const change = Math.floor(Math.random() * 5) - 2; // Random change between -2 and 2
        const newValue = Math.max(0, currentValue + change);
        
        // Animate the change
        animateValue(card, currentValue, newValue, 1000);
    });
}

function animateValue(element, start, end, duration) {
    const range = end - start;
    const increment = range / (duration / 16);
    let current = start;
    
    const timer = setInterval(() => {
        current += increment;
        if ((increment > 0 && current >= end) || (increment < 0 && current <= end)) {
            element.textContent = end;
            clearInterval(timer);
        } else {
            element.textContent = Math.round(current);
        }
    }, 16);
}

// Data Export
function initializeDataExport() {
    const exportButtons = document.querySelectorAll('.btn-export');
    
    exportButtons.forEach(button => {
        button.addEventListener('click', function() {
            const format = this.getAttribute('data-format');
            const table = this.getAttribute('data-table');
            
            exportTableData(table, format);
        });
    });
}

function exportTableData(tableId, format) {
    console.log(`📤 Exporting ${tableId} as ${format}`);
    
    const table = document.getElementById(tableId);
    if (!table) {
        showNotification('Table not found!', 'error');
        return;
    }
    
    if (format === 'csv') {
        exportToCSV(table);
    } else if (format === 'excel') {
        showNotification('Excel export coming soon!', 'info');
    } else if (format === 'pdf') {
        showNotification('PDF export coming soon!', 'info');
    }
}

function exportToCSV(table) {
    const rows = table.querySelectorAll('tr');
    let csv = [];
    
    // Add headers
    const headers = Array.from(rows[0].querySelectorAll('th')).map(th => th.textContent);
    csv.push(headers.join(','));
    
    // Add data rows
    for (let i = 1; i < rows.length; i++) {
        const row = rows[i];
        const cells = Array.from(row.querySelectorAll('td')).map(td => td.textContent);
        csv.push(cells.join(','));
    }
    
    // Download CSV
    const csvContent = csv.join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'admin_data.csv';
    a.click();
    window.URL.revokeObjectURL(url);
    
    showNotification('Data exported successfully!', 'success');
}

// Tooltips
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Animations
function initializeAnimations() {
    // Add fade-in animation to cards
    const cards = document.querySelectorAll('.stats-card, .admin-table-container');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            card.style.transition = 'all 0.5s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
}

// Utility Functions
function showLoadingModal() {
    const modal = document.createElement('div');
    modal.className = 'modal fade';
    modal.id = 'loadingModal';
    modal.innerHTML = `
        <div class="modal-dialog modal-sm">
            <div class="modal-content">
                <div class="modal-body text-center py-4">
                    <div class="spinner-border text-primary" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    <p class="mt-2 mb-0">Processing...</p>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    const bsModal = new bootstrap.Modal(modal, { backdrop: 'static', keyboard: false });
    bsModal.show();
}

function hideLoadingModal() {
    const modal = document.getElementById('loadingModal');
    if (modal) {
        bootstrap.Modal.getInstance(modal).hide();
        setTimeout(() => document.body.removeChild(modal), 500);
    }
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.style.opacity = '0';
            setTimeout(() => {
                if (notification.parentNode) {
                    document.body.removeChild(notification);
                }
            }, 500);
        }
    }, 5000);
}

function refreshTableData(type) {
    console.log(`🔄 Refreshing ${type} table data...`);
    // This would typically make an API call to refresh the data
    showNotification('Data refreshed!', 'success');
}

// Global functions for HTML onclick handlers
window.viewUserDetails = viewUserDetails;
window.viewApplicationDetails = viewApplicationDetails;
window.editUser = editUser;
window.editApplication = editApplication;
window.deleteItem = deleteItem;
window.exportTableData = exportTableData;

console.log('🎯 Admin JavaScript loaded successfully!');
