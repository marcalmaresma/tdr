// Comprovar si hi ha hagut un error de DNI i mostrar missatge
window.addEventListener('DOMContentLoaded', () => {
    if (sessionStorage.getItem('dni_error') === 'true') {
        showAlert('DNI incorrecte. Si us plau, introdueix un DNI vàlid.', 'error');
        // Esborrar el camp DNI
        const dniInput = document.getElementById('dni');
        if (dniInput) {
            dniInput.value = '';
            dniInput.focus();
        }
        // Netejar el flag d'error
        sessionStorage.removeItem('dni_error');
    }
});

document.getElementById('voter-login-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const dni = document.getElementById('dni').value.trim().toUpperCase();
    const nom = document.getElementById('nom').value.trim();
    const codi_votacio = document.getElementById('codi_votacio').value.trim().toUpperCase();
    
    if (!dni || !nom || !codi_votacio) {
        showAlert('Si us plau, omple tots els camps', 'error');
        return;
    }
    
    // Validar DNI i codi de votació
    try {
        const validateResponse = await fetch('/api/voter/validate-login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                dni: dni,
                code: codi_votacio 
            })
        });
        
        const validateData = await validateResponse.json();
        
        if (!validateData.success) {
            // Mostrar error específic segons el tipus
            if (validateData.error === 'dni_invalid') {
                showAlert('DNI incorrecte', 'error');
                // Esborrar només el camp DNI
                document.getElementById('dni').value = '';
                document.getElementById('dni').focus();
            } else if (validateData.error === 'code_invalid') {
                showAlert('Codi de votació incorrecte', 'error');
                // Esborrar només el camp de codi
                document.getElementById('codi_votacio').value = '';
                document.getElementById('codi_votacio').focus();
            } else if (validateData.error === 'both_invalid') {
                showAlert('DNI i codi de votació incorrectes', 'error');
                // Esborrar ambdós camps
                document.getElementById('dni').value = '';
                document.getElementById('codi_votacio').value = '';
                document.getElementById('dni').focus();
            } else {
                showAlert(validateData.message || 'Error de validació', 'error');
            }
            return;
        }
        
        // Tot correcte, guardar dades a sessionStorage
        sessionStorage.setItem('voter_dni', dni);
        sessionStorage.setItem('voter_nom', nom);
        sessionStorage.setItem('voter_codi', codi_votacio);
        
        // Redirigir a la pàgina de votació
        window.location.href = `/voter/vote/${codi_votacio}`;
        
    } catch (error) {
        showAlert('Error de connexió', 'error');
    }
});

function showAlert(message, type) {
    const container = document.getElementById('alert-container');
    container.innerHTML = `<div class="alert alert-${type === 'success' ? 'success' : 'error'}">${message}</div>`;
}

