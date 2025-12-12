# Encriptació RSA dels Vots

## Introducció

L'aplicació ara encripta els noms i DNIs dels votants utilitzant encriptació RSA amb una clau pública. Només qui tingui la clau privada pot desencriptar aquestes dades.

## Clau Pública Utilitzada

**Mòdul (n):**
```
22821840466491519043138118189621618411966956019422356753561154144339890974210629236261596261721520650816282460591705614210423489852719963342382152580215180657348296861369295753044659285940816677815879724369215024697590660829301358560583836904678707523115569403326077212133327938026166984559861101486679958974088126681381443781348662936898858374902722376939997058711955537864995262984240378423839242869879781035035496586235134494304908997333844002821477222348594076576361278099610636985152790084944054734801744606237298325373501317504629256107544868965456054277892538519412065464953249166054185812648403328256656153699
```

**Exponent públic (e):**
```
65537
```

## Implementació

### Fitxers Modificats

1. **`crypto_utils.py`** (NOU)
   - Conté les funcions d'encriptació
   - `encrypt_dni(dni)` - Encripta un DNI
   - `encrypt_nom(nom)` - Encripta un nom
   - `get_public_key()` - Crea l'objecte de clau pública RSA

2. **`database.py`**
   - Canviats els camps `dni_votant` i `nom_votant` de TEXT a BLOB
   - Ara emmagatzemen dades binàries encriptades

3. **`app.py`**
   - Importa les funcions d'encriptació
   - Encripta DNI i nom abans de guardar-los a la base de dades
   - En veure resultats, mostra un hash de les dades encriptades

4. **`requirements.txt`**
   - Afegida dependència: `cryptography==41.0.7`

## Com Funciona

### Encriptació (en votar)

1. L'usuari introdueix el seu DNI i nom
2. El DNI es valida
3. Abans de guardar a la base de dades:
   ```python
   dni_encrypted = encrypt_dni(dni_votant)
   nom_encrypted = encrypt_nom(nom_votant)
   ```
4. Les dades encriptades (bytes) es guarden com a BLOB

### Visualització (resultats)

- A la pàgina de resultats, es mostra un hash SHA256 de les dades encriptades
- Format: `[Encriptat - 1a2b3c4d]`
- Això permet veure que hi ha dades però sense revelar-les

### Desencriptació (amb clau privada)

Per desencriptar les dades (només qui tingui la clau privada):

```python
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes

# Carregar clau privada
with open("private_key.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(f.read(), password=None)

# Obtenir dades encriptades de la BD
import sqlite3
conn = sqlite3.connect("votacions.db")
cursor = conn.cursor()
cursor.execute("SELECT dni_votant, nom_votant FROM vots WHERE id = ?", (vot_id,))
row = cursor.fetchone()

dni_encrypted = row[0]
nom_encrypted = row[1]

# Desencriptar
dni_plaintext = private_key.decrypt(
    dni_encrypted,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

nom_plaintext = private_key.decrypt(
    nom_encrypted,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

print(f"DNI: {dni_plaintext.decode('utf-8')}")
print(f"Nom: {nom_plaintext.decode('utf-8')}")
```

## Seguretat

- **RSA-OAEP**: S'utilitza el padding OAEP (Optimal Asymmetric Encryption Padding) amb SHA-256
- **Clau de 2048+ bits**: La clau és prou llarga per garantir la seguretat
- **Només lectura**: Les dades encriptades només es poden llegir amb la clau privada
- **No reversible**: Sense la clau privada, és matemàticament impossible desencriptar les dades

## Migració de Dades Antigues

Si ja tenies vots a la base de dades abans d'implementar l'encriptació:
- Els vots antics tenen DNIs i noms en text pla (TEXT)
- Els nous vots tenen dades encriptades (BLOB)
- Es recomana eliminar vots antics o re-crear la base de dades

Per re-crear la base de dades:
```bash
rm votacions.db
python3 database.py
```

## Llibreries Necessàries

Instal·lar amb:
```bash
pip3 install cryptography==41.0.7
```

