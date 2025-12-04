from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import sqlite3
from database import get_db, init_db, generate_votacio_code
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Clau secreta per a sessions

# Inicialitzar base de dades
init_db()

# ==================== RUTES HTML ====================

@app.route('/')
def index():
    """Pàgina principal - selecció de rol"""
    return render_template('index.html')

@app.route('/admin/login')
def admin_login_page():
    """Pàgina de login per administrador"""
    return render_template('admin_login.html')

@app.route('/admin/panel')
def admin_panel():
    """Panell d'administració"""
    if 'admin_id' not in session:
        return redirect(url_for('admin_login_page'))
    return render_template('admin_panel.html')

@app.route('/admin/polls/new')
def create_poll_page():
    """Pàgina per crear nova votació"""
    if 'admin_id' not in session:
        return redirect(url_for('admin_login_page'))
    return render_template('create_poll.html')

@app.route('/admin/polls/<int:poll_id>')
def poll_results_page(poll_id):
    """Pàgina per veure resultats d'una votació"""
    if 'admin_id' not in session:
        return redirect(url_for('admin_login_page'))
    return render_template('poll_results.html', poll_id=poll_id)

@app.route('/voter/login')
def voter_login_page():
    """Pàgina de login per votant"""
    return render_template('voter_login.html')

@app.route('/voter/vote/<code>')
def vote_page(code):
    """Pàgina per votar"""
    return render_template('vote.html', code=code)

# ==================== API ENDPOINTS ====================

@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    """Login d'administrador"""
    data = request.json
    compte = data.get('compte')
    contrasenya = data.get('contrasenya')
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id FROM administradors 
        WHERE compte = ? AND contrasenya = ?
    ''', (compte, contrasenya))
    
    admin = cursor.fetchone()
    conn.close()
    
    if admin:
        session['admin_id'] = admin['id']
        session['admin_compte'] = compte
        return jsonify({'success': True, 'message': 'Login correcte'})
    else:
        return jsonify({'success': False, 'message': 'Compte o contrasenya incorrectes'}), 401

@app.route('/api/admin/logout', methods=['POST'])
def admin_logout():
    """Logout d'administrador"""
    session.clear()
    return jsonify({'success': True})

@app.route('/api/admin/polls', methods=['GET'])
def get_admin_polls():
    """Obtenir totes les votacions de l'administrador"""
    if 'admin_id' not in session:
        return jsonify({'error': 'No autenticat'}), 401
    
    admin_id = session['admin_id']
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, titol, descripcio, codi_votacio, data_creacio
        FROM votacions
        WHERE administrador_id = ?
        ORDER BY data_creacio DESC
    ''', (admin_id,))
    
    polls = []
    for row in cursor.fetchall():
        polls.append({
            'id': row['id'],
            'titol': row['titol'],
            'descripcio': row['descripcio'],
            'codi_votacio': row['codi_votacio'],
            'data_creacio': row['data_creacio']
        })
    
    conn.close()
    return jsonify({'success': True, 'polls': polls})

@app.route('/api/admin/polls', methods=['POST'])
def create_poll():
    """Crear nova votació"""
    if 'admin_id' not in session:
        return jsonify({'error': 'No autenticat'}), 401
    
    data = request.json
    titol = data.get('titol')
    descripcio = data.get('descripcio', '')
    opcions = data.get('opcions', [])
    
    if not titol or not opcions:
        return jsonify({'error': 'Títol i opcions són obligatoris'}), 400
    
    admin_id = session['admin_id']
    codi_votacio = generate_votacio_code()
    
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        # Crear votació
        cursor.execute('''
            INSERT INTO votacions (titol, descripcio, codi_votacio, administrador_id)
            VALUES (?, ?, ?, ?)
        ''', (titol, descripcio, codi_votacio, admin_id))
        
        poll_id = cursor.lastrowid
        
        # Crear opcions
        for opcio_text in opcions:
            cursor.execute('''
                INSERT INTO opcions (votacio_id, text_opcio)
                VALUES (?, ?)
            ''', (poll_id, opcio_text))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'poll_id': poll_id,
            'codi_votacio': codi_votacio,
            'message': 'Votació creada correctament'
        })
    except Exception as e:
        conn.rollback()
        conn.close()
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/polls/<int:poll_id>', methods=['GET'])
def get_poll_details(poll_id):
    """Obtenir detalls d'una votació"""
    if 'admin_id' not in session:
        return jsonify({'error': 'No autenticat'}), 401
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Obtenir votació
    cursor.execute('''
        SELECT id, titol, descripcio, codi_votacio, data_creacio
        FROM votacions
        WHERE id = ? AND administrador_id = ?
    ''', (poll_id, session['admin_id']))
    
    poll = cursor.fetchone()
    if not poll:
        conn.close()
        return jsonify({'error': 'Votació no trobada'}), 404
    
    # Obtenir opcions
    cursor.execute('''
        SELECT id, text_opcio
        FROM opcions
        WHERE votacio_id = ?
    ''', (poll_id,))
    
    opcions = [{'id': row['id'], 'text': row['text_opcio']} for row in cursor.fetchall()]
    
    conn.close()
    
    return jsonify({
        'success': True,
        'poll': {
            'id': poll['id'],
            'titol': poll['titol'],
            'descripcio': poll['descripcio'],
            'codi_votacio': poll['codi_votacio'],
            'data_creacio': poll['data_creacio'],
            'opcions': opcions
        }
    })

@app.route('/api/admin/polls/<int:poll_id>', methods=['DELETE'])
def delete_poll(poll_id):
    """Eliminar una votació"""
    if 'admin_id' not in session:
        return jsonify({'error': 'No autenticat'}), 401
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Verificar que la votació pertany a l'admin
    cursor.execute('''
        SELECT id FROM votacions
        WHERE id = ? AND administrador_id = ?
    ''', (poll_id, session['admin_id']))
    
    if not cursor.fetchone():
        conn.close()
        return jsonify({'error': 'Votació no trobada'}), 404
    
    try:
        # Eliminar la votació (els vots i opcions s'eliminaran en cascada per les foreign keys)
        cursor.execute('DELETE FROM votacions WHERE id = ?', (poll_id,))
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Votació eliminada correctament'})
    except Exception as e:
        conn.rollback()
        conn.close()
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/polls/<int:poll_id>/results', methods=['GET'])
def get_poll_results(poll_id):
    """Obtenir resultats d'una votació"""
    if 'admin_id' not in session:
        return jsonify({'error': 'No autenticat'}), 401
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Verificar que la votació pertany a l'admin
    cursor.execute('''
        SELECT id FROM votacions
        WHERE id = ? AND administrador_id = ?
    ''', (poll_id, session['admin_id']))
    
    if not cursor.fetchone():
        conn.close()
        return jsonify({'error': 'Votació no trobada'}), 404
    
    # Obtenir totes les opcions de la votació
    cursor.execute('''
        SELECT id, text_opcio
        FROM opcions
        WHERE votacio_id = ?
        ORDER BY id
    ''', (poll_id,))
    
    opcions = cursor.fetchall()
    results = []
    
    # Per cada opció, comptar els vots
    for opcio in opcions:
        opcio_id = opcio['id']
        text_opcio = opcio['text_opcio']
        
        # Comptar vots per aquesta opció
        cursor.execute('''
            SELECT COUNT(*) as num_vots
            FROM vots
            WHERE opcio_id = ? AND votacio_id = ?
        ''', (opcio_id, poll_id))
        
        count_row = cursor.fetchone()
        num_vots = int(count_row['num_vots']) if count_row and count_row['num_vots'] is not None else 0
        
        results.append({
            'opcio_id': int(opcio_id),
            'text_opcio': str(text_opcio),
            'num_vots': num_vots
        })
    
    # Obtenir llista de vots individuals
    cursor.execute('''
        SELECT v.id, v.dni_votant, v.nom_votant, v.data_vot, o.text_opcio
        FROM vots v
        JOIN opcions o ON v.opcio_id = o.id
        WHERE v.votacio_id = ?
        ORDER BY v.data_vot DESC
    ''', (poll_id,))
    
    votes = []
    for row in cursor.fetchall():
        votes.append({
            'id': row['id'],
            'dni_votant': row['dni_votant'],
            'nom_votant': row['nom_votant'],
            'opcio': row['text_opcio'],
            'data_vot': row['data_vot']
        })
    
    conn.close()
    
    return jsonify({
        'success': True,
        'results': results,
        'votes': votes
    })

@app.route('/api/voter/verify', methods=['POST'])
def verify_votacio_code():
    """Verificar que un codi de votació existeix"""
    data = request.json
    code = data.get('code')
    
    if not code:
        return jsonify({'error': 'Codi requerit'}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM votacions WHERE codi_votacio = ?', (code,))
    
    poll = cursor.fetchone()
    conn.close()
    
    if poll:
        return jsonify({'success': True, 'exists': True})
    else:
        return jsonify({'success': True, 'exists': False})

@app.route('/api/voter/poll/<code>', methods=['GET'])
def get_poll_by_code(code):
    """Obtenir detalls d'una votació per codi"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, titol, descripcio, codi_votacio
        FROM votacions
        WHERE codi_votacio = ?
    ''', (code,))
    
    poll = cursor.fetchone()
    if not poll:
        conn.close()
        return jsonify({'error': 'Votació no trobada'}), 404
    
    # Obtenir opcions
    cursor.execute('''
        SELECT id, text_opcio
        FROM opcions
        WHERE votacio_id = ?
    ''', (poll['id'],))
    
    opcions = [{'id': row['id'], 'text': row['text_opcio']} for row in cursor.fetchall()]
    
    conn.close()
    
    return jsonify({
        'success': True,
        'poll': {
            'id': poll['id'],
            'titol': poll['titol'],
            'descripcio': poll['descripcio'],
            'codi_votacio': poll['codi_votacio'],
            'opcions': opcions
        }
    })

@app.route('/api/voter/vote', methods=['POST'])
def submit_vote():
    """Enviar un vot"""
    data = request.json
    codi_votacio = data.get('codi_votacio')
    dni_votant = data.get('dni_votant')
    nom_votant = data.get('nom_votant')
    opcio_id = data.get('opcio_id')
    
    if not all([codi_votacio, dni_votant, nom_votant, opcio_id]):
        return jsonify({'error': 'Falten dades'}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Obtenir ID de la votació
    cursor.execute('SELECT id FROM votacions WHERE codi_votacio = ?', (codi_votacio,))
    poll = cursor.fetchone()
    
    if not poll:
        conn.close()
        return jsonify({'error': 'Votació no trobada'}), 404
    
    poll_id = poll['id']
    
    # Verificar que l'opció pertany a la votació
    cursor.execute('''
        SELECT id FROM opcions
        WHERE id = ? AND votacio_id = ?
    ''', (opcio_id, poll_id))
    
    if not cursor.fetchone():
        conn.close()
        return jsonify({'error': 'Opció no vàlida'}), 400
    
    # Registrar el vot
    try:
        cursor.execute('''
            INSERT INTO vots (votacio_id, opcio_id, dni_votant, nom_votant)
            VALUES (?, ?, ?, ?)
        ''', (poll_id, opcio_id, dni_votant, nom_votant))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Vot registrat correctament'})
    except Exception as e:
        conn.rollback()
        conn.close()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

