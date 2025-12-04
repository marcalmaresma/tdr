async function loadPolls() {
    try {
        const response = await fetch('/api/admin/polls');
        const data = await response.json();
        
        if (data.success) {
            displayPolls(data.polls);
        } else {
            showAlert('Error carregant votacions', 'error');
        }
    } catch (error) {
        showAlert('Error de connexió', 'error');
    }
}

function displayPolls(polls) {
    const container = document.getElementById('polls-container');
    
    if (polls.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <p>No tens cap votació creada encara.</p>
                <p>Crea la teva primera votació!</p>
            </div>
        `;
        return;
    }
    
    container.innerHTML = '<ul class="poll-list"></ul>';
    const list = container.querySelector('ul');
    
    polls.forEach(poll => {
        const item = document.createElement('li');
        item.className = 'poll-item';
        item.innerHTML = `
            <h3>${escapeHtml(poll.titol)}</h3>
            ${poll.descripcio ? `<p>${escapeHtml(poll.descripcio)}</p>` : ''}
            <div class="code">Codi: ${escapeHtml(poll.codi_votacio)}</div>
            <div class="poll-actions">
                <button onclick="viewResults(${poll.id})" class="btn btn-primary">
                    Veure Resultats
                </button>
                <button onclick="deletePoll(${poll.id}, '${escapeHtml(poll.titol)}')" class="btn btn-danger">
                    🗑️ Eliminar
                </button>
            </div>
        `;
        list.appendChild(item);
    });
}

function viewResults(pollId) {
    window.location.href = `/admin/polls/${pollId}`;
}

async function deletePoll(pollId, pollTitle) {
    if (!confirm(`Estàs segur que vols eliminar la votació "${pollTitle}"?\n\nAquesta acció no es pot desfer i s'eliminaran tots els vots associats.`)) {
        return;
    }
    
    try {
        const response = await fetch(`/api/admin/polls/${pollId}`, {
            method: 'DELETE'
        });
        
        const data = await response.json();
        
        if (data.success) {
            showAlert('Votació eliminada correctament', 'success');
            // Recarregar la llista de votacions
            setTimeout(() => {
                loadPolls();
            }, 1000);
        } else {
            showAlert(data.error || 'Error eliminant la votació', 'error');
        }
    } catch (error) {
        showAlert('Error de connexió', 'error');
    }
}

async function logout() {
    try {
        await fetch('/api/admin/logout', { method: 'POST' });
        window.location.href = '/';
    } catch (error) {
        window.location.href = '/';
    }
}

function showAlert(message, type) {
    const container = document.getElementById('alert-container');
    container.innerHTML = `<div class="alert alert-${type === 'success' ? 'success' : 'error'}">${message}</div>`;
    setTimeout(() => {
        container.innerHTML = '';
    }, 5000);
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Carregar votacions quan es carrega la pàgina
loadPolls();

