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
    
    const dni = document.getElementById('dni').value.trim();
    const nom = document.getElementById('nom').value.trim();
    const codi_votacio = document.getElementById('codi_votacio').value.trim().toUpperCase();
    
    if (!dni || !nom || !codi_votacio) {
        showAlert('Si us plau, omple tots els camps', 'error');
        return;
    }
    
    // Verificar que el codi existeix
    try {
        const verifyResponse = await fetch('/api/voter/verify', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ code: codi_votacio })
        });
        
        const verifyData = await verifyResponse.json();
        
        if (!verifyData.exists) {
            showAlert('Codi de votació no vàlid', 'error');
            return;
        }
        
        // Guardar dades a sessionStorage per usar-les després
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

