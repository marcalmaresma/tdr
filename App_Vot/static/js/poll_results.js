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
    const endTimeHtml = poll.end_time ? `<p><strong>Termini:</strong> ${formatDateTime(poll.end_time)}</p>` : '';
    container.innerHTML = `
        <h2>${escapeHtml(poll.titol)}</h2>
        ${poll.descripcio ? `<p>${escapeHtml(poll.descripcio)}</p>` : ''}
        ${endTimeHtml}
        <div class="code" style="margin: 15px 0;">Codi de Votació: ${escapeHtml(poll.codi_votacio)}</div>
        <div id="verification-status" style="margin-top: 15px;"></div>
    `;
}

function displayVerification(verificacio) {
    const container = document.getElementById('verification-status');
    
    if (!verificacio || verificacio.total_vots === 0) {
        container.innerHTML = '';
        return;
    }
    
    const { total_vots, vots_verificats, vots_alterats, integritat_completa, cadena_trencada } = verificacio;
    
    if (integritat_completa) {
        container.innerHTML = `
            <div class="alert alert-success" style="background: #d4edda; color: #155724; border: 1px solid #c3e6cb; padding: 15px; border-radius: 5px;">
                <strong>✓ Verificació Blockchain: Tots els vots són íntegres</strong><br>
                <small>${vots_verificats} de ${total_vots} vots verificats correctament.</small><br>
                <small>✓ Cadena de hash intacta · ✓ Cap vot alterat</small>
            </div>
        `;
    } else {
        const cadenaMsg = cadena_trencada ? '<br><small style="color: #dc3545;">🔗 CADENA DE HASH TRENCADA - Alteració detectada!</small>' : '';
        container.innerHTML = `
            <div class="alert alert-error" style="background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; padding: 15px; border-radius: 5px;">
                <strong>⚠️ ALERTA CRÍTICA: S'han detectat vots alterats!</strong><br>
                <small>Vots verificats: ${vots_verificats} | Vots alterats: ${vots_alterats} | Total: ${total_vots}</small>
                ${cadenaMsg}
                <br><small style="font-weight: bold;">⚠️ Els resultats NO són fiables. El sistema ha estat compromès.</small>
            </div>
        `;
    }
}

async function loadResults() {
    try {
        const response = await fetch(`/api/admin/polls/${pollId}/results`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.success) {
            // Assegurar que results i votes són arrays
            const results = Array.isArray(data.results) ? data.results : [];
            const votes = Array.isArray(data.votes) ? data.votes : [];
            const verificacio = data.verificacio || null;
            
            console.log('Resultats rebuts:', results);
            console.log('Nombre de resultats:', results.length);
            console.log('Verificació:', verificacio);
            
            displayVerification(verificacio);
            displayResults(results);
            displayVotes(votes);
        } else {
            showAlert('Error carregant resultats: ' + (data.error || 'Desconegut'), 'error');
        }
    } catch (error) {
        console.error('Error carregant resultats:', error);
        showAlert('Error de connexió: ' + error.message, 'error');
    }
}

function displayResults(results) {
    const container = document.getElementById('results-container');
    
    // Assegurar que results és un array
    if (!Array.isArray(results)) {
        container.innerHTML = '<h2>Recompte de Vots</h2><p class="alert alert-error">Error: Dades de resultats no vàlides.</p>';
        return;
    }
    
    if (results.length === 0) {
        container.innerHTML = '<h2>Recompte de Vots</h2><p>Encara no hi ha opcions configurades per a aquesta votació.</p>';
        return;
    }
    
    // Assegurar-nos que num_vots és un número
    const totalVots = results.reduce((sum, r) => {
        const vots = parseInt(r.num_vots) || 0;
        return sum + vots;
    }, 0);
    
    let html = '<h2>Recompte de Vots</h2>';
    html += '<table class="results-table">';
    html += '<thead><tr><th>Opció</th><th>Vots</th><th>Percentatge</th></tr></thead>';
    html += '<tbody>';
    
    // Iterar sobre cada resultat i crear una fila
    for (let i = 0; i < results.length; i++) {
        const result = results[i];
        if (!result) continue;
        
        const numVots = parseInt(result.num_vots) || 0;
        const textOpcio = result.text_opcio || 'Opció sense nom';
        const percentatge = totalVots > 0 ? ((numVots / totalVots) * 100).toFixed(1) : '0.0';
        
        html += `
            <tr>
                <td>${escapeHtml(textOpcio)}</td>
                <td>${numVots}</td>
                <td>${percentatge}%</td>
            </tr>
        `;
    }
    
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
    html += '<table class="results-table">';
    html += '<thead><tr><th>Nom</th><th>DNI</th><th>Vot</th><th>Data</th><th>Estat</th></tr></thead>';
    html += '<tbody>';
    
    votes.forEach(vote => {
        const verificatIcon = vote.verificat ? 
            '<span style="color: #28a745; font-weight: bold;">✓ Verificat</span>' : 
            '<span style="color: #dc3545; font-weight: bold;">⚠️ Alterat</span>';
        
        html += `
            <tr style="${vote.verificat ? '' : 'background-color: #fff3cd;'}">
                <td><strong>${escapeHtml(vote.nom_votant)}</strong></td>
                <td>${escapeHtml(vote.dni_votant)}</td>
                <td>${escapeHtml(vote.opcio)}</td>
                <td><small>${formatDateTime(vote.data_vot)}</small></td>
                <td>${verificatIcon}</td>
            </tr>
        `;
    });
    
    html += '</tbody></table>';
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

// Carregar dades quan es carrega la pàgina
loadPollDetails();

