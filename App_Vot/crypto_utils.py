"""
Utilitats per encriptar noms i DNIs amb clau pública RSA
"""
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend

# Clau pública (mòdul n)
PUBLIC_KEY_N = 26370146660610931097416887361945484749774297537711981404246798088393922975920704619223956269940997975956730546193789585595060900566486616734617372353639963271425401489527775521992629222135118034864035953451353120892033536023885586781108151905608417641129197118764456166619376415126427321371689167172121177909056389714977641485462134584592922317216438896791843425565811901871782335414564507389087710709508326991864402467885781312247680609162350838222652648422940087809089974942412108460287742241799926415171552800351436957513904982379588048679696308210418066217909206531880946438195625966772790693383523958978940927959

# Exponent públic estàndard
PUBLIC_KEY_E = 65537

def get_public_key():
    """
    Crear l'objecte de clau pública RSA a partir del mòdul i l'exponent
    """
    public_numbers = rsa.RSAPublicNumbers(
        e=PUBLIC_KEY_E,
        n=PUBLIC_KEY_N
    )
    public_key = public_numbers.public_key(default_backend())
    return public_key

def encrypt_data(plaintext):
    """
    Encriptar dades amb la clau pública RSA
    
    Args:
        plaintext (str): Text a encriptar
        
    Returns:
        bytes: Dades encriptades
    """
    if not plaintext:
        return None
    
    public_key = get_public_key()
    
    # Convertir el text a bytes
    plaintext_bytes = plaintext.encode('utf-8')
    
    # Encriptar amb RSA OAEP
    ciphertext = public_key.encrypt(
        plaintext_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    
    return ciphertext

def encrypt_dni(dni):
    """
    Encriptar un DNI
    
    Args:
        dni (str): DNI a encriptar
        
    Returns:
        bytes: DNI encriptat
    """
    return encrypt_data(dni)

def encrypt_nom(nom):
    """
    Encriptar un nom
    
    Args:
        nom (str): Nom a encriptar
        
    Returns:
        bytes: Nom encriptat
    """
    return encrypt_data(nom)

