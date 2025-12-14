# Protecció Contra Vots Duplicats

## Funcionalitat

El sistema ara impedeix que un mateix DNI pugui votar més d'una vegada a la mateixa votació.

## Com Funciona

### 1. Hash del DNI

Quan un votant vota, el sistema:
1. **Encripta** el DNI amb RSA per a la privacitat (no es pot desencriptar sense la clau privada)
2. **Genera un hash SHA-256** del DNI en text pla per poder comprovar duplicats

```python
# Encriptar per a privacitat
dni_encrypted = encrypt_dni(dni_votant)  # RSA-OAEP

# Hash per a comprovació de duplicats
dni_hash = hash_dni(dni_votant)  # SHA-256
```

### 2. Base de Dades

La taula `vots` té:
- `dni_votant` (BLOB): DNI encriptat amb RSA
- `dni_hash` (TEXT): Hash SHA-256 del DNI
- **Índex únic** sobre `(votacio_id, dni_hash)`: Garanteix que no puguin haver-hi dos vots amb el mateix hash de DNI a la mateixa votació

```sql
CREATE UNIQUE INDEX idx_vot_unique 
ON vots(votacio_id, dni_hash)
```

### 3. Comprovació Abans de Votar

Abans de registrar un vot, el backend:
1. Genera el hash del DNI
2. Comprova si ja existeix un vot amb aquest hash per aquesta votació
3. Si existeix, retorna error: **"Aquest DNI ja ha votat en aquesta votació"**
4. Si no existeix, permet el vot

```python
# Comprovar si ja ha votat
cursor.execute('''
    SELECT id FROM vots
    WHERE votacio_id = ? AND dni_hash = ?
''', (poll_id, dni_hash_value))

if cursor.fetchone():
    return jsonify({'error': 'Aquest DNI ja ha votat en aquesta votació'})
```

## Seguretat i Privacitat

### ✅ Privacitat Garantida
- El DNI real està **encriptat amb RSA** i només es pot desencriptar amb la clau privada
- El hash SHA-256 **no es pot invertir** per obtenir el DNI original

### ✅ Protecció Contra Duplicats
- L'índex únic a nivell de base de dades **garanteix** que no es puguin inserir duplicats
- Fins i tot si hi ha un error al codi, la BD ho impedeix

### ✅ Diferents Votacions
- Un DNI pot votar a **diferents votacions**
- Només s'impedeix votar **més d'una vegada a la mateixa votació**

## Missatges d'Error

### Frontend (`vote.js`)

Quan un DNI intenta votar per segona vegada:
1. Mostra: **"Aquest DNI ja ha votat en aquesta votació"**
2. Neteja el sessionStorage
3. Redirigeix a la pàgina principal després de 3 segons

### Backend (`app.py`)

Retorna:
```json
{
  "error": "Aquest DNI ja ha votat en aquesta votació",
  "success": false
}
```

## Exemple de Flux

### Primera Vegada (Vot Permès)

1. Votant introdueix DNI `12345678Z` i vota per l'opció A
2. Sistema genera:
   - `dni_encrypted`: `b'\x8a\x3f...'` (encriptat)
   - `dni_hash`: `ef797c8118f02dfb...` (hash)
3. Insereix vot a la BD amb ambdues dades
4. ✅ **Vot registrat correctament**

### Segona Vegada (Vot Bloquejat)

1. El mateix votant intenta votar de nou amb DNI `12345678Z`
2. Sistema genera el mateix `dni_hash`: `ef797c8118f02dfb...`
3. Comprova la BD i **troba un vot amb aquest hash**
4. ❌ **Error: "Aquest DNI ja ha votat en aquesta votació"**

## Migració

Si ja tenies vots a la base de dades abans d'aquesta actualització:
- Els vots antics **han estat esborrats** perquè no tenien `dni_hash`
- A partir d'ara, tots els vots nous inclouran el `dni_hash`

## Fitxers Modificats

1. **`crypto_utils.py`**: Afegida funció `hash_dni()`
2. **`database.py`**: 
   - Afegida columna `dni_hash` a la taula `vots`
   - Creat índex únic `idx_vot_unique`
3. **`app.py`**: 
   - Importat `hash_dni`
   - Comprovació de duplicats abans de votar
   - Inserció del `dni_hash` juntament amb el vot
4. **`static/js/vote.js`**: Afegit missatge d'error específic per vots duplicats

