function addOption() {
    const container = document.getElementById('options-container');
    const optionCount = container.children.length;
    
    const optionDiv = document.createElement('div');
    optionDiv.className = 'option-item';
    optionDiv.innerHTML = `
        <input type="text" class="option-input" placeholder="Opció ${optionCount + 1}" required>
        <button type="button" class="btn btn-danger" onclick="removeOption(this)">Eliminar</button>
    `;
    
    container.appendChild(optionDiv);
    updateRemoveButtons();
}

function removeOption(button) {
    const container = document.getElementById('options-container');
    if (container.children.length > 1) {
        button.parentElement.remove();
        updateRemoveButtons();
    }
}

function updateRemoveButtons() {
    const container = document.getElementById('options-container');
    const options = container.querySelectorAll('.option-item');
    
    options.forEach((option, index) => {
        const removeBtn = option.querySelector('.btn-danger');
        if (options.length === 1) {
            removeBtn.style.display = 'none';
        } else {
            removeBtn.style.display = 'block';
        }
    });
}

document.getElementById('create-poll-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const titol = document.getElementById('titol').value.trim();
    const descripcio = document.getElementById('descripcio').value.trim();
    
    const optionInputs = document.querySelectorAll('.option-input');
    const opcions = Array.from(optionInputs)
        .map(input => input.value.trim())
        .filter(text => text.length > 0);
    
    if (opcions.length < 2) {
        showAlert('Cal afegir almenys 2 opcions', 'error');
        return;
    }
    
    try {
        const response = await fetch('/api/admin/polls', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                titol,
                descripcio,
                opcions
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showAlert(`Votació creada! Codi: ${data.codi_votacio}`, 'success');
            setTimeout(() => {
                window.location.href = '/admin/panel';
            }, 2000);
        } else {
            showAlert(data.error || 'Error creant la votació', 'error');
        }
    } catch (error) {
        showAlert('Error de connexió', 'error');
    }
});

function showAlert(message, type) {
    const container = document.getElementById('alert-container');
    container.innerHTML = `<div class="alert alert-${type === 'success' ? 'success' : 'error'}">${message}</div>`;
}

