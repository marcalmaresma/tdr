let pollData = null;
let dniVotant = null;
let nomVotant = null;

async function loadPoll() {
    try {
        dniVotant = sessionStorage.getItem('voter_dni');
        nomVotant = sessionStorage.getItem('voter_nom');
        
        if (!dniVotant || !nomVotant) {
            showAlert('Dades de votant no trobades. Si us plau, accedeix des del formulari.', 'error');
            setTimeout(() => {
                window.location.href = '/voter/login';
            }, 2000);
            return;
        }
        
        // Enviar DNI com a query parameter per comprovar si ja ha votat
        const response = await fetch(`/api/voter/poll/${votacioCode}?dni=${encodeURIComponent(dniVotant)}`);
        const data = await response.json();
        
        if (data.success) {
            pollData = data.poll;
            displayPoll();
        } else {
            showAlert('Votació no trobada', 'error');
        }
    } catch (error) {
        showAlert('Error de connexió', 'error');
    }
}

function displayPoll() {
    const infoContainer = document.getElementById('poll-info');
    const formContainer = document.getElementById('vote-form-container');
    
    infoContainer.innerHTML = `
        <h2>${escapeHtml(pollData.titol)}</h2>
        ${pollData.descripcio ? `<p>${escapeHtml(pollData.descripcio)}</p>` : ''}
        ${pollData.end_time ? `<p style="color: #666;"><strong>Termini:</strong> ${formatDateTime(pollData.end_time)}</p>` : ''}
    `;
    
    // Comprovar si ja ha votat
    if (pollData.has_voted) {
        formContainer.innerHTML = `
            <div class="alert alert-error" style="margin-top: 20px;">
                <strong>Ja has votat!</strong><br>
                Aquest DNI ja ha emès el seu vot en aquesta votació. No pots tornar a votar.
            </div>
            <div style="margin-top: 30px;">
                <h3 style="color: #555; margin-bottom: 15px;">Opcions de la votació:</h3>
                <div class="radio-options">
                    ${pollData.opcions.map(opcio => `
                        <div class="radio-option" style="background: #f0f0f0; cursor: default; opacity: 0.7;">
                            <input type="radio" disabled>
                            <label style="cursor: default;">${escapeHtml(opcio.text)}</label>
                        </div>
                    `).join('')}
                </div>
            </div>
            <button onclick="window.location.href='/'" class="btn btn-primary btn-block" style="margin-top: 30px;">
                Tornar a l'Inici
            </button>
        `;
        return;
    }
    
    // Comprovar si la votació ha acabat
    if (pollData.is_expired) {
        formContainer.innerHTML = `
            <div class="alert alert-error" style="margin-top: 20px;">
                <strong>Votació finalitzada</strong><br>
                El termini per votar en aquesta votació ja ha acabat.
            </div>
            <div style="margin-top: 30px;">
                <h3 style="color: #555; margin-bottom: 15px;">Opcions de la votació:</h3>
                <div class="radio-options">
                    ${pollData.opcions.map(opcio => `
                        <div class="radio-option" style="background: #f0f0f0; cursor: default; opacity: 0.7;">
                            <input type="radio" disabled>
                            <label style="cursor: default;">${escapeHtml(opcio.text)}</label>
                        </div>
                    `).join('')}
                </div>
            </div>
            <button onclick="window.location.href='/'" class="btn btn-primary btn-block" style="margin-top: 30px;">
                Tornar a l'Inici
            </button>
        `;
        return;
    }
    
    // Si la votació està activa, mostrar formulari normal
    let formHtml = '<form id="vote-form">';
    formHtml += '<div class="radio-options">';
    
    pollData.opcions.forEach((opcio, index) => {
        formHtml += `
            <div class="radio-option">
                <input type="radio" id="opcio_${opcio.id}" name="opcio" value="${opcio.id}" required>
                <label for="opcio_${opcio.id}">${escapeHtml(opcio.text)}</label>
            </div>
        `;
    });
    
    formHtml += '</div>';
    formHtml += '<button type="submit" class="btn btn-primary btn-block">Enviar Vot</button>';
    formHtml += '</form>';
    
    formContainer.innerHTML = formHtml;
    
    // Afegir event listener al formulari
    document.getElementById('vote-form').addEventListener('submit', handleVote);
}

async function handleVote(e) {
    e.preventDefault();
    
    const opcioId = document.querySelector('input[name="opcio"]:checked')?.value;
    
    if (!opcioId) {
        showAlert('Si us plau, selecciona una opció', 'error');
        return;
    }
    
    try {
        const response = await fetch('/api/voter/vote', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                codi_votacio: votacioCode,
                dni_votant: dniVotant,
                nom_votant: nomVotant,
                opcio_id: parseInt(opcioId)
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showAlert('Vot registrat correctament! Gràcies per participar.', 'success');
            document.getElementById('vote-form').style.display = 'none';
            
            // Netejar sessionStorage
            sessionStorage.removeItem('voter_dni');
            sessionStorage.removeItem('voter_nom');
            sessionStorage.removeItem('voter_codi');
            
            setTimeout(() => {
                window.location.href = '/';
            }, 3000);
        } else {
            // Si l'error és de DNI incorrecte, netejar sessionStorage i redirigir al login
            if (data.error && data.error.includes('DNI incorrecte')) {
                showAlert('DNI incorrecte. Si us plau, introdueix un DNI vàlid.', 'error');
                // Marcar que hi ha hagut un error de DNI
                sessionStorage.setItem('dni_error', 'true');
                sessionStorage.removeItem('voter_dni');
                sessionStorage.removeItem('voter_nom');
                sessionStorage.removeItem('voter_codi');
                setTimeout(() => {
                    window.location.href = '/voter/login';
                }, 2000);
            } else if (data.error && data.error.includes('ja ha votat')) {
                // Si el DNI ja ha votat en aquesta votació
                showAlert('Aquest DNI ja ha votat en aquesta votació', 'error');
                sessionStorage.removeItem('voter_dni');
                sessionStorage.removeItem('voter_nom');
                sessionStorage.removeItem('voter_codi');
                setTimeout(() => {
                    window.location.href = '/';
                }, 3000);
            } else {
                showAlert(data.error || 'Error registrant el vot', 'error');
            }
        }
    } catch (error) {
        showAlert('Error de connexió', 'error');
    }
}

function showAlert(message, type) {
    const container = document.getElementById('alert-container');
    container.innerHTML = `<div class="alert alert-${type === 'success' ? 'success' : 'error'}">${message}</div>`;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatDateTime(isoString) {
    if (!isoString) return '';
    try {
        const normalized = isoString.replace(' ', 'T');
        const d = new Date(normalized);
        if (isNaN(d)) return isoString;
        const dd = String(d.getDate()).padStart(2, '0');
        const mm = String(d.getMonth() + 1).padStart(2, '0');
        const yyyy = d.getFullYear();
        const hh = String(d.getHours()).padStart(2, '0');
        const min = String(d.getMinutes()).padStart(2, '0');
        return `${dd}-${mm}-${yyyy}, ${hh}:${min}`;
    } catch (e) {
        return isoString;
    }
}

// Carregar votació quan es carrega la pàgina
loadPoll();

