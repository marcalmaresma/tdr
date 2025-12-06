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
            body: JSON.stringify({ code: codi_votacio, dni: dni })
        });
        
        const verifyData = await verifyResponse.json();
        console.log(verifyData);
        if (!verifyData.exists) {
            if (verifyData.error == 'Codi de votació no trobat i DNI incorrecte') {
                showAlert('Codi de votació no trobat i DNI incorrecte. Si us plau, introdueix un codi de votació vàlid i un DNI vàlid.', 'error');
                return;
            }
            if (verifyData.error == 'DNI incorrecte') {
                showAlert('DNI incorrecte. Si us plau, introdueix un DNI vàlid.', 'error');
                return;
            }
            if (verifyData.error == 'Codi de votació no trobat') {
                showAlert('Codi de votació no trobat. Si us plau, introdueix un codi de votació vàlid.', 'error');
                return;
            }
            showAlert(verifyData.error, 'error');
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

