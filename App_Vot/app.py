from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import sqlite3
from database import get_db, init_db, generate_votacio_code
from datetime import datetime
import os
import hashlib
from crypto_utils import encrypt_dni, encrypt_nom

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
    
    # Obtenir l'admin per compte
    cursor.execute('SELECT id, contrasenya FROM administradors WHERE compte = ?', (compte,))
    admin = cursor.fetchone()
    
    if not admin:
        conn.close()
        return jsonify({'success': False, 'message': 'Compte o contrasenya incorrectes'}), 401
    
    contrasenya_bd = admin['contrasenya']
    
    # Generar hash SHA-256 de la contrasenya introduïda
    contrasenya_hash = hashlib.sha256(contrasenya.encode('utf-8')).hexdigest()
    
    print(f"DEBUG Login:")
    print(f"  Compte: {compte}")
    print(f"  Contrasenya introduïda: {contrasenya}")
    print(f"  Hash generat: {contrasenya_hash}")
    print(f"  Hash a la BD: {contrasenya_bd}")
    print(f"  Coincideixen? {contrasenya_hash == contrasenya_bd}")
    
    # Comparar el hash generat amb el de la BD
    if contrasenya_hash == contrasenya_bd:
        session['admin_id'] = admin['id']
        session['admin_compte'] = compte
        conn.close()
        return jsonify({'success': True, 'message': 'Login correcte'})
    
    conn.close()
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
        SELECT id, titol, descripcio, codi_votacio, data_creacio, end_time
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
            'data_creacio': row['data_creacio'],
            'end_time': row['end_time']
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
    end_time = data.get('end_time')  # ISO string o buit
    
    if not titol or not opcions:
        return jsonify({'error': 'Títol i opcions són obligatoris'}), 400
    
    admin_id = session['admin_id']
    codi_votacio = generate_votacio_code()
    
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        # Crear votació
        cursor.execute('''
            INSERT INTO votacions (titol, descripcio, codi_votacio, end_time, administrador_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (titol, descripcio, codi_votacio, end_time, admin_id))
        
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
            'end_time': end_time,
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
        SELECT id, titol, descripcio, codi_votacio, data_creacio, end_time
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
            'end_time': poll['end_time'],
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
        # Les dades estan encriptades, mostrem indicador
        dni_encrypted = row['dni_votant']
        nom_encrypted = row['nom_votant']
        
        # Mostrar hash o representació de les dades encriptades
        import hashlib
        dni_display = f"[Encriptat - {hashlib.sha256(dni_encrypted).hexdigest()[:8]}]" if isinstance(dni_encrypted, bytes) else dni_encrypted
        nom_display = f"[Encriptat - {hashlib.sha256(nom_encrypted).hexdigest()[:8]}]" if isinstance(nom_encrypted, bytes) else nom_encrypted
        
        votes.append({
            'id': row['id'],
            'dni_votant': dni_display,
            'nom_votant': nom_display,
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

@app.route('/api/voter/validate-login', methods=['POST'])
def validate_voter_login():
    """Validar DNI i codi de votació del votant"""
    data = request.json
    dni = data.get('dni', '').strip().upper()
    codi_votacio = data.get('code', '').upper()
    
    # Validar que les dades existeixen
    if not dni or not codi_votacio:
        return jsonify({
            'success': False,
            'error': 'missing_data',
            'message': 'Falten dades'
        }), 400
    
    # Validar DNI
    dni_valid = False
    
    dnilet = "TRWAGMYFPDXBNJZSQVHLCKE"                  #Assigno les lletres amb la posició concordant amb el nombre que els hi toqui
    if len(dni) != 9:                                   #Els dnis consten de 9 caràcters, 8 nombres i 1 lletra, per tant si el dni introduit conté un nombre diferent a 9 de caràcters és incorrecte
        dni_valid = False
    else:
        try:
            if dnilet[int(dni[0:8])%23] == dni[8].upper():       #Calculo la lletra que obtenim del nombre i si coincideix amb la que s'ha introduit és correcte
                dni_valid = True
            else:                                         #Si en canvi no coincideix mostro la lletra que correspon al nombre
                dni_valid = False
        except (ValueError, IndexError):
            dni_valid = False
    # Exemple del teu codi:
    # a = dni
    # dni_letters = "TRWAGMYFPDXBNJZSQVHLCKE"
    # if len(a) == 9:
    #     try:
    #         if dni_letters[int(a[0:8])%23] == a[8]:
    #             dni_valid = True
    #     except (ValueError, IndexError):
    #         dni_valid = False
    
    # ============================================
    
    # Validar codi de votació
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM votacions WHERE codi_votacio = ?', (codi_votacio,))
    code_valid = cursor.fetchone() is not None
    conn.close()
    
    # Determinar l'error específic
    if not dni_valid and not code_valid:
        return jsonify({
            'success': False,
            'error': 'both_invalid',
            'message': 'DNI i codi de votació incorrectes'
        }), 400
    elif not dni_valid:
        return jsonify({
            'success': False,
            'error': 'dni_invalid',
            'message': 'DNI incorrecte'
        }), 400
    elif not code_valid:
        return jsonify({
            'success': False,
            'error': 'code_invalid',
            'message': 'Codi de votació incorrecte'
        }), 400
    
    # Tot correcte
    return jsonify({
        'success': True,
        'message': 'Validació correcta'
    })

@app.route('/api/voter/poll/<code>', methods=['GET'])
def get_poll_by_code(code):
    """Obtenir detalls d'una votació per codi"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, titol, descripcio, codi_votacio, end_time
        FROM votacions
        WHERE codi_votacio = ?
    ''', (code,))
    
    poll = cursor.fetchone()
    if not poll:
        conn.close()
        return jsonify({'error': 'Votació no trobada'}), 404
    
    # Comprovar si la votació ha acabat
    is_expired = False
    end_time = poll['end_time']
    if end_time:
        try:
            end_dt = datetime.fromisoformat(end_time)
            if datetime.now() > end_dt:
                is_expired = True
        except:
            pass
    
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
            'end_time': poll['end_time'],
            'is_expired': is_expired,
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
    
    dni_TF = False
    
    # Validar DNI amb el teu codi
    if dni_votant:
        a = dni_votant
        dni = "TRWAGMYFPDXBNJZSQVHLCKE"                  #Assigno les lletres amb la posició concordant amb el nombre que els hi toqui
        if len(a) != 9:                                   #Els dnis consten de 9 caràcters, 8 nombres i 1 lletra, per tant si el dni introduit conté un nombre diferent a 9 de caràcters és incorrecte
            dni_TF = False
        else:
            try:
                if dni[int(a[0:8])%23] == a[8].upper():       #Calculo la lletra que obtenim del nombre i si coincideix amb la que s'ha introduit és correcte
                    dni_TF = True
                else:                                         #Si en canvi no coincideix mostro la lletra que correspon al nombre
                    dni_TF = False
            except (ValueError, IndexError):
                dni_TF = False
    else:
        dni_TF = False

    # Validar DNI - si és incorrecte, retornar error
    if dni_TF == False:
        return jsonify({'error': 'DNI incorrecte', 'success': False}), 400

    if not all([codi_votacio, dni_votant, nom_votant, opcio_id]):
        return jsonify({'error': 'Falten dades'}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Obtenir ID de la votació i el seu termini
    cursor.execute('SELECT id, end_time FROM votacions WHERE codi_votacio = ?', (codi_votacio,))
    poll = cursor.fetchone()
    
    if not poll:
        conn.close()
        return jsonify({'error': 'Votació no trobada'}), 404
    
    poll_id = poll['id']
    end_time = poll['end_time']

    # Si hi ha termini i ja ha passat, no permetre votar
    if end_time:
        try:
            end_dt = datetime.fromisoformat(end_time)
            if datetime.now() > end_dt:
                conn.close()
                return jsonify({'error': 'La votació ja ha finalitzat'}), 400
        except Exception:
            # Si el format és invàlid, permetre però avisar d'error de dades
            conn.close()
            return jsonify({'error': 'Error amb el termini de la votació'}), 400
    
    # Verificar que l'opció pertany a la votació
    cursor.execute('''
        SELECT id FROM opcions
        WHERE id = ? AND votacio_id = ?
    ''', (opcio_id, poll_id))
    
    if not cursor.fetchone():
        conn.close()
        return jsonify({'error': 'Opció no vàlida'}), 400
    
    # Encriptar DNI i nom abans de guardar
    try:
        dni_encrypted = encrypt_dni(dni_votant)
        nom_encrypted = encrypt_nom(nom_votant)
    except Exception as e:
        conn.close()
        return jsonify({'error': f'Error encriptant dades: {str(e)}'}), 500
    
    # Registrar el vot amb dades encriptades
    try:
        cursor.execute('''
            INSERT INTO vots (votacio_id, opcio_id, dni_votant, nom_votant)
            VALUES (?, ?, ?, ?)
        ''', (poll_id, opcio_id, dni_encrypted, nom_encrypted))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Vot registrat correctament'})
    except Exception as e:
        conn.rollback()
        conn.close()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

