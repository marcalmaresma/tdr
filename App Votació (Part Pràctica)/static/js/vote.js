let pollData = null;
let dniVotant = null;
let nomVotant = null;

async function loadPoll() {
    try {
        const response = await fetch(`/api/voter/poll/${votacioCode}`);
        const data = await response.json();
        
        if (data.success) {
            pollData = data.poll;
            dniVotant = sessionStorage.getItem('voter_dni');
            nomVotant = sessionStorage.getItem('voter_nom');
            
            if (!dniVotant || !nomVotant) {
                showAlert('Dades de votant no trobades. Si us plau, accedeix des del formulari.', 'error');
                setTimeout(() => {
                    window.location.href = '/voter/login';
                }, 2000);
                return;
            }
            
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
    `;
    
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
            showAlert(data.error || 'Error registrant el vot', 'error');
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

// Carregar votació quan es carrega la pàgina
loadPoll();

