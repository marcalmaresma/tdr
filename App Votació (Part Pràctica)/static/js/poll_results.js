async function loadPollDetails() {
    try {
        const response = await fetch(`/api/admin/polls/${pollId}`);
        const data = await response.json();
        
        if (data.success) {
            displayPollInfo(data.poll);
            loadResults();
        } else {
            showAlert('Error carregant la votació', 'error');
        }
    } catch (error) {
        showAlert('Error de connexió', 'error');
    }
}

function displayPollInfo(poll) {
    const container = document.getElementById('poll-info');
    container.innerHTML = `
        <h2>${escapeHtml(poll.titol)}</h2>
        ${poll.descripcio ? `<p>${escapeHtml(poll.descripcio)}</p>` : ''}
        <div class="code" style="margin: 15px 0;">Codi de Votació: ${escapeHtml(poll.codi_votacio)}</div>
    `;
}

async function loadResults() {
    try {
        const response = await fetch(`/api/admin/polls/${pollId}/results`);
        const data = await response.json();
        
        if (data.success) {
            displayResults(data.results);
            displayVotes(data.votes);
        } else {
            showAlert('Error carregant resultats', 'error');
        }
    } catch (error) {
        showAlert('Error de connexió', 'error');
    }
}

function displayResults(results) {
    const container = document.getElementById('results-container');
    
    if (results.length === 0) {
        container.innerHTML = '<p>Encara no hi ha resultats.</p>';
        return;
    }
    
    const totalVots = results.reduce((sum, r) => sum + r.num_vots, 0);
    
    let html = '<h2>Recompte de Vots</h2>';
    html += '<table class="results-table">';
    html += '<thead><tr><th>Opció</th><th>Vots</th><th>Percentatge</th></tr></thead>';
    html += '<tbody>';
    
    results.forEach(result => {
        const percentatge = totalVots > 0 ? ((result.num_vots / totalVots) * 100).toFixed(1) : 0;
        html += `
            <tr>
                <td>${escapeHtml(result.text_opcio)}</td>
                <td>${result.num_vots}</td>
                <td>${percentatge}%</td>
            </tr>
        `;
    });
    
    html += '</tbody></table>';
    html += `<p><strong>Total de vots: ${totalVots}</strong></p>`;
    
    container.innerHTML = html;
}

function displayVotes(votes) {
    const container = document.getElementById('votes-container');
    
    if (votes.length === 0) {
        container.innerHTML = '<div class="votes-list"><h2>Vots Individuals</h2><p>Encara no hi ha vots.</p></div>';
        return;
    }
    
    let html = '<div class="votes-list"><h2>Vots Individuals</h2>';
    
    votes.forEach(vote => {
        html += `
            <div class="vote-item">
                <strong>${escapeHtml(vote.nom_votant)}</strong> (DNI: ${escapeHtml(vote.dni_votant)})<br>
                Vot: ${escapeHtml(vote.opcio)}<br>
                <small>Data: ${vote.data_vot}</small>
            </div>
        `;
    });
    
    html += '</div>';
    container.innerHTML = html;
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

// Carregar dades quan es carrega la pàgina
loadPollDetails();

