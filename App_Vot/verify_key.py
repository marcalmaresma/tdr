#!/usr/bin/env python3
"""
Script per verificar que una clau privada .pem correspon a la clau pública
utilitzada per l'aplicació (hardcoded a crypto_utils.py)
"""

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from crypto_utils import PUBLIC_KEY_N, PUBLIC_KEY_E
import sys
import os
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


def verify_key_match(private_key):
    """
    Verificar que la clau privada correspon a la clau pública de l'aplicació
    
    Args:
        private_key: Clau privada RSA
        
    Returns:
        bool: True si coincideixen, False altrament
    """
    # Extreure la clau pública de la clau privada
    public_key = private_key.public_key()
    public_numbers = public_key.public_numbers()
    
    # Comparar amb els valors hardcoded
    n_match = (public_numbers.n == PUBLIC_KEY_N)
    e_match = (public_numbers.e == PUBLIC_KEY_E)
    
    return n_match and e_match, public_numbers


def main():
    """Funció principal"""
    print()
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║               VERIFICADOR DE CLAU PRIVADA                                    ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    
    # Demanar ruta de la clau privada
    if len(sys.argv) > 1:
        private_key_path = sys.argv[1]
    else:
        print("Aquest script verifica que una clau privada correspon a la clau pública")
        print("utilitzada per l'aplicació de votacions.")
        print()
        private_key_path = input("📝 Introdueix la ruta al fitxer .pem amb la clau privada: ").strip()
    
    if not private_key_path:
        print("❌ Error: Has de proporcionar una ruta al fitxer .pem")
        sys.exit(1)
    
    # Expandir ~ si és necessari
    private_key_path = os.path.expanduser(private_key_path)
    
    print()
    print("=" * 80)
    print(f"📂 Carregant clau privada des de: {private_key_path}")
    
    # Carregar la clau privada
    private_key = load_private_key(private_key_path)
    print("✅ Clau privada carregada correctament")
    print()
    
    # Verificar coincidència
    print("🔍 Verificant coincidència amb la clau pública de l'aplicació...")
    matches, public_numbers = verify_key_match(private_key)
    
    print()
    print("=" * 80)
    print("RESULTAT DE LA VERIFICACIÓ")
    print("=" * 80)
    print()
    
    if matches:
        print("✅ ¡COINCIDÈNCIA PERFECTA!")
        print()
        print("La clau privada proporcionada correspon exactament a la clau pública")
        print("utilitzada per l'aplicació. Pots utilitzar aquesta clau per desencriptar")
        print("tots els noms i DNIs de la base de dades.")
        print()
        print("📝 Per desencriptar els vots, executa:")
        print(f"   python3 decrypt_votes.py {private_key_path}")
    else:
        print("❌ NO COINCIDEIX")
        print()
        print("La clau privada proporcionada NO correspon a la clau pública utilitzada")
        print("per l'aplicació. No podràs desencriptar les dades amb aquesta clau.")
        print()
        print("Detalls:")
        print("-" * 80)
        print()
        print("Clau pública de l'aplicació (crypto_utils.py):")
        print(f"  Mòdul (n): {PUBLIC_KEY_N}")
        print(f"  Exponent (e): {PUBLIC_KEY_E}")
        print()
        print("Clau pública extreta de la clau privada proporcionada:")
        print(f"  Mòdul (n): {public_numbers.n}")
        print(f"  Exponent (e): {public_numbers.e}")
        print()
        print("Possibles solucions:")
        print("  1. Assegura't que estàs utilitzant la clau privada correcta")
        print("  2. Si has perdut la clau privada original, no podràs desencriptar les dades existents")
        print("  3. Si vols utilitzar aquesta clau, hauràs d'actualitzar crypto_utils.py")
        print("     amb els nous valors de PUBLIC_KEY_N i PUBLIC_KEY_E mostrats aquí dalt")
    
    print()
    print("=" * 80)
    print()


if __name__ == '__main__':
    main()

