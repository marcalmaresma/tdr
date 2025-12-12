#!/usr/bin/env python3
"""
Script per generar un parell de claus RSA (pública i privada)
Aquest script genera la clau privada que correspon a la clau pública 
hardcoded a crypto_utils.py
"""

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import os


def generate_keypair(key_size=2048):
    """
    Generar un parell de claus RSA
    
    Args:
        key_size (int): Mida de la clau en bits (2048 o 4096 recomanat)
        
    Returns:
        tuple: (private_key, public_key)
    """
    print(f"🔐 Generant parell de claus RSA de {key_size} bits...")
    
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
        backend=default_backend()
    )
    
    public_key = private_key.public_key()
    
    print("✅ Claus generades correctament")
    return private_key, public_key


def save_private_key(private_key, filename='private_key.pem'):
    """
    Guardar la clau privada a un fitxer .pem
    
    Args:
        private_key: Clau privada RSA
        filename (str): Nom del fitxer de sortida
    """
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    filepath = os.path.join(os.path.dirname(__file__), filename)
    with open(filepath, 'wb') as f:
        f.write(pem)
    
    # Establir permisos restrictius (només lectura per l'usuari)
    os.chmod(filepath, 0o600)
    
    print(f"💾 Clau privada guardada a: {filepath}")
    print(f"   Permisos establerts: 600 (només lectura per l'usuari)")


def save_public_key(public_key, filename='public_key.pem'):
    """
    Guardar la clau pública a un fitxer .pem
    
    Args:
        public_key: Clau pública RSA
        filename (str): Nom del fitxer de sortida
    """
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    filepath = os.path.join(os.path.dirname(__file__), filename)
    with open(filepath, 'wb') as f:
        f.write(pem)
    
    print(f"💾 Clau pública guardada a: {filepath}")


def display_public_key_components(public_key):
    """
    Mostrar els components de la clau pública (n i e) per actualitzar crypto_utils.py
    
    Args:
        public_key: Clau pública RSA
    """
    public_numbers = public_key.public_numbers()
    
    print()
    print("=" * 80)
    print("COMPONENTS DE LA CLAU PÚBLICA")
    print("=" * 80)
    print()
    print("⚠️  Si vols utilitzar aquesta clau a l'aplicació, hauràs d'actualitzar")
    print("   els valors de PUBLIC_KEY_N i PUBLIC_KEY_E a crypto_utils.py:")
    print()
    print("PUBLIC_KEY_N = " + str(public_numbers.n))
    print()
    print("PUBLIC_KEY_E = " + str(public_numbers.e))
    print()
    print("=" * 80)


def main():
    """Funció principal"""
    print()
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║               GENERADOR DE PARELLS DE CLAUS RSA                             ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    
    print("⚠️  AVÍS IMPORTANT:")
    print()
    print("Aquest script genera un NOU parell de claus RSA. Si ja tens dades encriptades")
    print("amb la clau pública actual de l'aplicació, NO podràs desencriptar-les amb")
    print("aquesta nova clau privada.")
    print()
    print("Aquest script és útil si:")
    print("  1. Estàs configurant l'aplicació per primera vegada")
    print("  2. Vols generar noves claus i començar de zero")
    print("  3. Has perdut la clau privada i vols regenerar-ho tot")
    print()
    
    resposta = input("Vols continuar? (s/n): ").strip().lower()
    
    if resposta != 's':
        print("\n❌ Operació cancel·lada")
        return
    
    print()
    
    # Generar claus
    private_key, public_key = generate_keypair(key_size=2048)
    
    print()
    
    # Guardar claus
    save_private_key(private_key, 'private_key.pem')
    save_public_key(public_key, 'public_key.pem')
    
    print()
    
    # Mostrar components
    display_public_key_components(public_key)
    
    print()
    print("✅ Procés completat!")
    print()
    print("📝 PRÒXIMS PASSOS:")
    print("   1. Copia els valors de PUBLIC_KEY_N i PUBLIC_KEY_E mostrats anteriorment")
    print("   2. Actualitza'ls al fitxer crypto_utils.py")
    print("   3. Guarda la clau privada (private_key.pem) en un lloc segur")
    print("   4. Pots esborrar la clau pública (public_key.pem) ja que està a crypto_utils.py")
    print()
    print("⚠️  SEGURETAT:")
    print("   - NO comparteixis MAI la clau privada (private_key.pem)")
    print("   - Fes còpies de seguretat de la clau privada")
    print("   - Considera encriptar la clau privada amb una contrasenya")
    print()


if __name__ == '__main__':
    main()

