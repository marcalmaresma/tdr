import sqlite3
import os
import secrets
import string

DB_PATH = os.path.join(os.path.dirname(__file__), 'votacions.db')

def get_db():
    """Obtenir connexió a la base de dades"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    # Activar foreign keys per SQLite
    conn.execute('PRAGMA foreign_keys = ON')
    return conn

def init_db():
    """Inicialitzar la base de dades amb les taules necessàries"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Taula d'administradors
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS administradors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            compte TEXT UNIQUE NOT NULL,
            contrasenya TEXT NOT NULL
        )
    ''')
    
    # Taula de votacions
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS votacions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titol TEXT NOT NULL,
            descripcio TEXT,
            codi_votacio TEXT UNIQUE NOT NULL,
            data_creacio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            end_time TEXT,
            administrador_id INTEGER NOT NULL,
            FOREIGN KEY (administrador_id) REFERENCES administradors(id)
        )
    ''')

    # Afegir columna end_time si no existeix (compatibilitat amb bases de dades creades abans)
    cursor.execute("PRAGMA table_info(votacions)")
    columns = [row["name"] for row in cursor.fetchall()]
    if "end_time" not in columns:
        cursor.execute("ALTER TABLE votacions ADD COLUMN end_time TEXT")
    
    # Taula d'opcions
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS opcions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            votacio_id INTEGER NOT NULL,
            text_opcio TEXT NOT NULL,
            FOREIGN KEY (votacio_id) REFERENCES votacions(id) ON DELETE CASCADE
        )
    ''')
    
    # Taula de vots amb dades encriptades
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            votacio_id INTEGER NOT NULL,
            opcio_id INTEGER NOT NULL,
            dni_votant BLOB NOT NULL,
            nom_votant BLOB NOT NULL,
            dni_hash TEXT NOT NULL,
            data_vot TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (votacio_id) REFERENCES votacions(id) ON DELETE CASCADE,
            FOREIGN KEY (opcio_id) REFERENCES opcions(id) ON DELETE CASCADE
        )
    ''')
    
    # Crear índex únic per evitar que un DNI voti més d'una vegada a la mateixa votació
    cursor.execute('''
        CREATE UNIQUE INDEX IF NOT EXISTS idx_vot_unique 
        ON vots(votacio_id, dni_hash)
    ''')
    
    # Crear administrador per defecte si no existeix
    cursor.execute('SELECT * FROM administradors WHERE compte = ?', ('MarçalMaresma',))
    if not cursor.fetchone():
        cursor.execute('''
            INSERT INTO administradors (compte, contrasenya)
            VALUES (?, ?)
        ''', ('MarçalMaresma', '12345678'))
    
    conn.commit()
    conn.close()

def generate_votacio_code():
    """Generar un codi únic per a una votació"""
    while True:
        # Generar codi de 6 caràcters alfanumèrics
        code = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(6))
        
        # Verificar que no existeix
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM votacions WHERE codi_votacio = ?', (code,))
        if not cursor.fetchone():
            conn.close()
            return code
        conn.close()

if __name__ == '__main__':
    init_db()
    print("Base de dades inicialitzada correctament!")

