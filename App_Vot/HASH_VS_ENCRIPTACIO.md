# Per Què Hash i No Encriptació per a Contrasenyes?

## Problema amb RSA per Comparar Contrasenyes

### RSA-OAEP és No Determinístic

Quan encriptes amb RSA-OAEP (el mètode que utilitzem per DNIs/noms), cada encriptació dona un resultat diferent:

```python
from crypto_utils import encrypt_data

# Primera encriptació
result1 = encrypt_data("12345678")
print(result1)  # → bytes_A (exemple: b'\x8a\x3f...')

# Segona encriptació de la mateixa dada
result2 = encrypt_data("12345678")
print(result2)  # → bytes_B (exemple: b'\x7c\x1e...')

# NO SÓN IGUALS!
print(result1 == result2)  # → False
```

**Per què passa això?**
- RSA-OAEP afegeix padding aleatori (randomització)
- Això és bo per seguretat, però impedeix comparar directament
- Cada encriptació és diferent, fins i tot amb la mateixa entrada

### Per Tant, No Es Pot Fer Això:

❌ **Incorrecte:**
1. Guardar contrasenya encriptada a la BD
2. Encriptar la contrasenya introduïda al login
3. Comparar les dues ← **AIXÒ NO FUNCIONA!**

Resultat: Sempre serà diferent, fins i tot amb la contrasenya correcta.

## Solució: Hash SHA-256

### Hash És Determinístic

Un hash sempre dona el mateix resultat per la mateixa entrada:

```python
import hashlib

# Primera vegada
hash1 = hashlib.sha256("12345678".encode()).hexdigest()
print(hash1)  # → ef797c8118f02dfb649607dd5d3f8c7623048c9c063d532cc95c5ed7a898a64f

# Segona vegada
hash2 = hashlib.sha256("12345678".encode()).hexdigest()
print(hash2)  # → ef797c8118f02dfb649607dd5d3f8c7623048c9c063d532cc95c5ed7a898a64f

# SÓN IGUALS!
print(hash1 == hash2)  # → True
```

### Per Tant, Es Pot Fer Això:

✅ **Correcte:**
1. Guardar hash de la contrasenya a la BD: `ef797c81...`
2. Al login, generar hash de la contrasenya introduïda
3. Comparar els dos hash ← **AIXÒ SÍ FUNCIONA!**

### Avantatges del Hash per a Contrasenyes

1. **Determinístic**: Mateix input → mateix output
2. **Irreversible**: No es pot obtenir la contrasenya original del hash
3. **Ràpid**: Més ràpid que RSA
4. **Estàndard**: És el mètode utilitzat per tota la indústria

## Resum

- **Per DNIs/Noms de votants**: Utilitzem **RSA** perquè necessitem **desencriptar** les dades després
- **Per Contrasenyes**: Utilitzem **Hash** perquè només necessitem **verificar** si és correcta, no desencriptar-la

## Implementació Actual

```python
# Al crear l'admin (o actualitzar contrasenya):
contrasenya_hash = hashlib.sha256("12345678".encode()).hexdigest()
# Guardar contrasenya_hash a la BD

# Al login:
contrasenya_introduida = request.json.get('contrasenya')
hash_introduit = hashlib.sha256(contrasenya_introduida.encode()).hexdigest()

if hash_introduit == contrasenya_hash_bd:
    # Login correcte!
```

Aquest mètode és segur, eficient i és l'estàndard de la indústria.

