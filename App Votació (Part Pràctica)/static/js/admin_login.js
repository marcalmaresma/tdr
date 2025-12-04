document.getElementById('login-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const compte = document.getElementById('compte').value;
    const contrasenya = document.getElementById('contrasenya').value;
    
    try {
        const response = await fetch('/api/admin/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ compte, contrasenya })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showAlert('Login correcte! Redirigint...', 'success');
            setTimeout(() => {
                window.location.href = '/admin/panel';
            }, 1000);
        } else {
            showAlert(data.message || 'Error en el login', 'error');
        }
    } catch (error) {
        showAlert('Error de connexió', 'error');
    }
});

function showAlert(message, type) {
    const container = document.getElementById('alert-container');
    container.innerHTML = `<div class="alert alert-${type === 'success' ? 'success' : 'error'}">${message}</div>`;
}

