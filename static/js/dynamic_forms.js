// Function to toggle fields based on device type selection
function toggleDeviceFields() {
    const deviceTypeSelect = document.querySelector('#id_device_type');
    if (!deviceTypeSelect) return;
    
    const selectedOption = deviceTypeSelect.options[deviceTypeSelect.selectedIndex];
    const isDesktop = selectedOption.text.toLowerCase().includes('desktop');
    
    // Toggle component fields visibility
    const componentFields = document.getElementById('component-fields');
    if (componentFields) {
        componentFields.style.display = isDesktop ? 'block' : 'none';
    }
    
    // Toggle component fields requirement
    const lcdComponent = document.querySelector('#id_lcd_component');
    const cpuComponent = document.querySelector('#id_cpu_component');
    
    if (lcdComponent && cpuComponent) {
        lcdComponent.required = isDesktop;
        cpuComponent.required = isDesktop;
    }
}

// Function to toggle closure date based on status
function toggleClosureDate() {
    const statusSelect = document.querySelector('#id_status');
    const closureDateField = document.querySelector('#id_closure_date');
    const closureRemarksField = document.querySelector('#id_closure_remarks');
    
    if (statusSelect && closureDateField && closureRemarksField) {
        const isResolved = statusSelect.value === 'RESOLVED';
        
        closureDateField.disabled = !isResolved;
        if (isResolved && !closureDateField.value) {
            const today = new Date().toISOString().split('T')[0];
            closureDateField.value = today;
        }
        
        closureRemarksField.required = isResolved;
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    // Device type fields
    toggleDeviceFields();
    const deviceTypeSelect = document.querySelector('#id_device_type');
    if (deviceTypeSelect) {
        deviceTypeSelect.addEventListener('change', toggleDeviceFields);
    }
    
    // Vendor escalation status
    toggleClosureDate();
    const statusSelect = document.querySelector('#id_status');
    if (statusSelect) {
        statusSelect.addEventListener('change', toggleClosureDate);
    }
    
    // Form validation for biometric authentication
    const biometricForm = document.querySelector('#biometric-form');
    if (biometricForm) {
        biometricForm.addEventListener('submit', function(e) {
            const biometricInput = document.querySelector('#id_biometric_data');
            const passwordInput = document.querySelector('#id_password');
            
            if (!biometricInput.files.length && !passwordInput.value) {
                e.preventDefault();
                alert('Please provide either biometric data or password for authentication');
            }
        });
    }
});

// Refresh attachments list after upload
function refreshAttachments() {
    const container = document.querySelector('.attachments-container');
    if (container) {
        fetch(window.location.href)
            .then(response => response.text())
            .then(html => {
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');
                const newContent = doc.querySelector('.attachments-container');
                if (newContent) {
                    container.innerHTML = newContent.innerHTML;
                }
            });
    }
}

// Call this after successful upload in your upload script
