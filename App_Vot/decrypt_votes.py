#!/usr/bin/env python3
"""
Programa per desencriptar noms i DNIs encriptats de la base de dades de votacions
Utilitza la clau privada RSA per desencriptar les dades
"""

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
import sqlite3
import os
import sys
import getpass


def load_private_key(pem_file_path):
    """
    Carregar la clau privada des d'un fitxer .pem
    
    Args:
        pem_file_path (str): Ruta al fitxer .pem amb la clau privada
        
    Returns:
        private_key: Objecte de clau privada RSA
    """
    try:
        with open(pem_file_path, 'rb') as key_file:
            key_data = key_file.read()
        
        # Intentar carregar sense contrasenya primer
        try:
            private_key = serialization.load_pem_private_key(
                key_data,
                password=None,
                backend=default_backend()
            )
            return private_key
        except TypeError:
            # La clau necessita contrasenya
            print()
            print("🔒 La clau privada està protegida amb contrasenya")
            print()
            print("⚠️  IMPORTANT: Quan escriguis la contrasenya NO es veurà a la pantalla.")
            print("   Això és normal per seguretat. Escriu-la i prem Enter.")
            print()
            
            password = getpass.getpass("Introdueix la contrasenya: ")
            
            if not password:
                print("❌ Error: No s'ha introduït cap contrasenya")
                sys.exit(1)
            
            try:
                private_key = serialization.load_pem_private_key(
                    key_data,
                    password=password.encode('utf-8'),
                    backend=default_backend()
                )
                print("✅ Contrasenya correcta!")
                return private_key
            except ValueError:
                print("❌ Error: Contrasenya incorrecta")
                sys.exit(1)
                
    except FileNotFoundError:
        print(f"❌ Error: No s'ha trobat el fitxer {pem_file_path}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error carregant la clau privada: {e}")
        sys.exit(1)


def decrypt_data(private_key, ciphertext):
    """
    Desencriptar dades amb la clau privada RSA
    
    Args:
        private_key: Clau privada RSA
        ciphertext (bytes): Dades encriptades
        
    Returns:
        str: Text desencriptat
    """
    if not ciphertext or not isinstance(ciphertext, bytes):
        return "[No disponible]"
    
    try:
        plaintext_bytes = private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return plaintext_bytes.decode('utf-8')
    except Exception as e:
        return f"[Error desencriptant: {str(e)}]"


def get_db_path():
    """Obtenir el path de la base de dades"""
    return os.path.join(os.path.dirname(__file__), 'votacions.db')


def decrypt_all_votes(private_key_path):
    """
    Desencriptar tots els vots de la base de dades
    
    Args:
        private_key_path (str): Ruta al fitxer .pem amb la clau privada
    """
    print("=" * 80)
    print("DESENCRIPTACIÓ DE VOTS DE LA BASE DE DADES")
    print("=" * 80)
    print()
    
    # Carregar clau privada
    print(f"📂 Carregant clau privada des de: {private_key_path}")
    private_key = load_private_key(private_key_path)
    print("✅ Clau privada carregada correctament")
    print()
    
    # Connectar a la base de dades
    db_path = get_db_path()
    print(f"📂 Connectant a la base de dades: {db_path}")
    
    if not os.path.exists(db_path):
        print(f"❌ Error: No s'ha trobat la base de dades en {db_path}")
        sys.exit(1)
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    print("✅ Connectat a la base de dades")
    print()
    
    # Obtenir tots els vots
    cursor.execute('''
        SELECT 
            v.id,
            v.votacio_id,
            v.opcio_id,
            v.dni_votant,
            v.nom_votant,
            v.data_vot,
            vot.titol as votacio_titol,
            vot.codi_votacio,
            o.text_opcio
        FROM vots v
        JOIN votacions vot ON v.votacio_id = vot.id
        JOIN opcions o ON v.opcio_id = o.id
        ORDER BY v.votacio_id, v.data_vot
    ''')
    
    vots = cursor.fetchall()
    
    if not vots:
        print("ℹ️  No s'han trobat vots a la base de dades")
        conn.close()
        return
    
    print(f"🔍 S'han trobat {len(vots)} vots. Desencriptant...")
    print()
    print("=" * 80)
    
    # Agrupar per votació
    votacions_dict = {}
    for vot in vots:
        votacio_id = vot['votacio_id']
        if votacio_id not in votacions_dict:
            votacions_dict[votacio_id] = {
                'titol': vot['votacio_titol'],
                'codi': vot['codi_votacio'],
                'vots': []
            }
        
        # Desencriptar DNI i nom
        dni_desencriptat = decrypt_data(private_key, vot['dni_votant'])
        nom_desencriptat = decrypt_data(private_key, vot['nom_votant'])
        
        votacions_dict[votacio_id]['vots'].append({
            'id': vot['id'],
            'dni': dni_desencriptat,
            'nom': nom_desencriptat,
            'opcio': vot['text_opcio'],
            'data': vot['data_vot']
        })
    
    # Mostrar resultats agrupats per votació
    for votacio_id, votacio_info in votacions_dict.items():
        print()
        print(f"📊 VOTACIÓ: {votacio_info['titol']}")
        print(f"   Codi: {votacio_info['codi']}")
        print(f"   Total vots: {len(votacio_info['vots'])}")
        print("-" * 80)
        
        for i, vot in enumerate(votacio_info['vots'], 1):
            print(f"   Vot #{i} (ID: {vot['id']})")
            print(f"      👤 Nom:  {vot['nom']}")
            print(f"      🆔 DNI:  {vot['dni']}")
            print(f"      ✅ Opció: {vot['opcio']}")
            print(f"      📅 Data: {vot['data']}")
            print()
    
    print("=" * 80)
    print(f"✅ Desencriptació completada. Total de vots processats: {len(vots)}")
    
    conn.close()


def export_to_csv(private_key_path, output_file='vots_desencriptats.csv'):
    """
    Desencriptar i exportar tots els vots a un fitxer CSV
    
    Args:
        private_key_path (str): Ruta al fitxer .pem amb la clau privada
        output_file (str): Nom del fitxer CSV de sortida
    """
    print("=" * 80)
    print("EXPORTACIÓ DE VOTS DESENCRIPTATS A CSV")
    print("=" * 80)
    print()
    
    # Carregar clau privada
    print(f"📂 Carregant clau privada des de: {private_key_path}")
    private_key = load_private_key(private_key_path)
    print("✅ Clau privada carregada correctament")
    print()
    
    # Connectar a la base de dades
    db_path = get_db_path()
    print(f"📂 Connectant a la base de dades: {db_path}")
    
    if not os.path.exists(db_path):
        print(f"❌ Error: No s'ha trobat la base de dades en {db_path}")
        sys.exit(1)
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    print("✅ Connectat a la base de dades")
    print()
    
    # Obtenir tots els vots
    cursor.execute('''
        SELECT 
            v.id,
            v.votacio_id,
            v.dni_votant,
            v.nom_votant,
            v.data_vot,
            vot.titol as votacio_titol,
            vot.codi_votacio,
            o.text_opcio
        FROM vots v
        JOIN votacions vot ON v.votacio_id = vot.id
        JOIN opcions o ON v.opcio_id = o.id
        ORDER BY v.votacio_id, v.data_vot
    ''')
    
    vots = cursor.fetchall()
    
    if not vots:
        print("ℹ️  No s'han trobat vots a la base de dades")
        conn.close()
        return
    
    print(f"🔍 S'han trobat {len(vots)} vots. Desencriptant i exportant...")
    
    # Crear fitxer CSV
    import csv
    output_path = os.path.join(os.path.dirname(__file__), output_file)
    
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        # Capçalera
        writer.writerow(['ID Vot', 'Votació', 'Codi Votació', 'Nom Votant', 'DNI Votant', 'Opció Votada', 'Data Vot'])
        
        # Dades
        for vot in vots:
            dni_desencriptat = decrypt_data(private_key, vot['dni_votant'])
            nom_desencriptat = decrypt_data(private_key, vot['nom_votant'])
            
            writer.writerow([
                vot['id'],
                vot['votacio_titol'],
                vot['codi_votacio'],
                nom_desencriptat,
                dni_desencriptat,
                vot['text_opcio'],
                vot['data_vot']
            ])
    
    conn.close()
    
    print(f"✅ Fitxer CSV creat: {output_path}")
    print(f"   Total de vots exportats: {len(vots)}")
    print()


def main():
    """Funció principal del programa"""
    print()
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║            PROGRAMA DE DESENCRIPTACIÓ DE VOTS - SISTEMA DE VOTACIÓ          ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    
    # Demanar ruta de la clau privada
    if len(sys.argv) > 1:
        # Si es passa com a argument
        private_key_path = sys.argv[1]
    else:
        # Demanar interactivament
        print("Per desencriptar els vots necessites la clau privada RSA (.pem)")
        print()
        private_key_path = input("📝 Introdueix la ruta al fitxer .pem amb la clau privada: ").strip()
    
    if not private_key_path:
        print("❌ Error: Has de proporcionar una ruta al fitxer .pem")
        sys.exit(1)
    
    # Expandir ~ si és necessari
    private_key_path = os.path.expanduser(private_key_path)
    
    print()
    print("Selecciona una opció:")
    print("  1. Mostrar vots desencriptats per pantalla")
    print("  2. Exportar vots desencriptats a CSV")
    print("  3. Fer ambdues coses")
    print()
    
    if len(sys.argv) > 2:
        opcio = sys.argv[2]
    else:
        opcio = input("Opció (1/2/3): ").strip()
    
    print()
    
    if opcio == '1':
        decrypt_all_votes(private_key_path)
    elif opcio == '2':
        export_to_csv(private_key_path)
    elif opcio == '3':
        decrypt_all_votes(private_key_path)
        print()
        export_to_csv(private_key_path)
    else:
        print("❌ Opció no vàlida")
        sys.exit(1)
    
    print()
    print("=" * 80)
    print("✅ Procés finalitzat correctament")
    print("=" * 80)
    print()


if __name__ == '__main__':
    main()

