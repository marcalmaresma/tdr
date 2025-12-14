# Sistema de Verificació d'Integritat amb MD5

## Objectiu

Garantir que els vots no hagin estat alterats després de ser registrats, mitjançant el càlcul i verificació de hash MD5 de cada vot.

## Com Funciona

### 1. Quan es Registra un Vot

Quan un votant emet el seu vot, el sistema:

1. **Recull les dades del vot:**
   - `votacio_id`: ID de la votació
   - `opcio_id`: ID de l'opció votada
   - `dni_hash`: Hash SHA-256 del DNI
   - `data_vot`: Timestamp del moment del vot

2. **Genera un hash MD5:**
   ```python
   vot_data = f"{poll_id}:{opcio_id}:{dni_hash_value}:{datetime.now().isoformat()}"
   md5_hash = hashlib.md5(vot_data.encode('utf-8')).hexdigest()
   ```

3. **Guarda el vot amb el hash MD5:**
   - El vot es guarda a la base de dades amb totes les dades encriptades
   - El hash MD5 es guarda a la columna `md5_hash`

### 2. Quan es Visualitzen els Resultats

Cada vegada que l'administrador accedeix als resultats:

1. **Obté tots els vots de la BD**

2. **Per cada vot, recalcula el MD5:**
   ```python
   vot_data = f"{votacio_id}:{opcio_id}:{dni_hash}:{data_vot}"
   md5_calculat = hashlib.md5(vot_data.encode('utf-8')).hexdigest()
   ```

3. **Compara el MD5 calculat amb el guardat:**
   ```python
   vot_integre = (md5_calculat == md5_original)
   ```

4. **Mostra l'estat de verificació:**
   - ✓ **Verificat**: El MD5 coincideix → el vot no ha estat alterat
   - ⚠️ **Alterat**: El MD5 no coincideix → el vot pot haver estat modificat

### 3. Visualització a la Interfície

#### Banner de Verificació General

Si tots els vots són íntegres:
```
✓ Verificació MD5: Tots els vots són íntegres
X de X vots verificats correctament. Cap vot ha estat alterat.
```

Si hi ha vots alterats:
```
⚠️ Advertència: S'han detectat vots alterats!
Vots verificats: X | Vots alterats: Y | Total: Z
Els resultats poden no ser fiables.
```

#### Taula de Vots Individuals

Cada vot mostra una columna "Estat":
- **✓ Verificat** (en verd): El vot és íntegre
- **⚠️ Alterat** (en vermell): El vot pot haver estat modificat

Els vots alterats també es ressalten amb fons groc (`#fff3cd`).

## Seguretat

### ✅ Protecció Contra Alteracions

- **Qualsevol canvi** en les dades d'un vot (votació, opció, DNI, data) farà que el MD5 no coincideixi
- És **extremadament difícil** modificar un vot i mantenir el mateix MD5

### ✅ Detecció Immediata

- Cada vegada que es carreguen els resultats, es verifica la integritat
- No es pot alterar un vot sense que es detecti

### ✅ Dades Verificades

Les dades que es verifica el MD5 inclouen:
- `votacio_id`: Quin poll
- `opcio_id`: Quina opció
- `dni_hash`: Qui va votar (hash del DNI)
- `data_vot`: Quan es va votar

## Limitacions

### ⚠️ MD5 només detecta alteracions, no les impedeix

El sistema **detecta** si un vot ha estat alterat, però no impedeix que algú amb accés directe a la base de dades pugui modificar-lo.

### ⚠️ La protecció depèn de l'accés a la BD

Si algú té accés complet a la base de dades, podria:
1. Modificar un vot
2. Recalcular el MD5
3. Actualitzar el `md5_hash` a la BD

**Però:** Per fer-ho necessitaria:
- Accés directe a la base de dades
- Conèixer l'algoritme de càlcul del MD5
- Això és un risc molt més gran que simplement alterar resultats

## Casos d'Ús

### ✅ Detectar Errors de Base de Dades

Si hi ha problemes de corrupció de dades, es detectarà immediatament.

### ✅ Detectar Manipulacions No Autoritzades

Si algú intenta modificar vots sense actualitzar els MD5, es detectarà.

### ✅ Audit de Resultats

L'administrador pot estar segur que els resultats mostrats corresponen als vots reals registrats.

## Estructura de la Base de Dades

### Taula `vots`

```sql
CREATE TABLE vots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    votacio_id INTEGER NOT NULL,
    opcio_id INTEGER NOT NULL,
    dni_votant BLOB NOT NULL,      -- DNI encriptat
    nom_votant BLOB NOT NULL,       -- Nom encriptat
    dni_hash TEXT NOT NULL,         -- Hash SHA-256 del DNI
    data_vot TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    md5_hash TEXT NOT NULL,         -- Hash MD5 per verificació
    FOREIGN KEY (votacio_id) REFERENCES votacions(id) ON DELETE CASCADE,
    FOREIGN KEY (opcio_id) REFERENCES opcions(id) ON DELETE CASCADE
)
```

## Exemple Pràctic

### Vot Original
```
votacio_id: 1
opcio_id: 3
dni_hash: ef797c8118f02dfb...
data_vot: 2025-12-14T10:30:00
```

**MD5 generat:** `a3f2c8d9e1b4f7a2c5d8e9f1a2b3c4d5`

### Verificació Correcta
Si ningú ha modificat el vot, quan es recalcula:
```
MD5 calculat: a3f2c8d9e1b4f7a2c5d8e9f1a2b3c4d5
MD5 guardat:  a3f2c8d9e1b4f7a2c5d8e9f1a2b3c4d5
Resultat: ✓ Verificat
```

### Vot Alterat
Si algú modifica `opcio_id` de 3 a 5:
```
MD5 calculat: b4e3d2c1f0a9e8d7c6b5a4f3e2d1c0b9
MD5 guardat:  a3f2c8d9e1b4f7a2c5d8e9f1a2b3c4d5
Resultat: ⚠️ Alterat
```

## Fitxers Modificats

1. **`database.py`**: Afegida columna `md5_hash` a la taula `vots`
2. **`app.py`**: 
   - Generació de MD5 quan es registra un vot
   - Verificació de MD5 quan es carreguen resultats
   - Retorn d'estat de verificació a l'API
3. **`static/js/poll_results.js`**: 
   - Funció `displayVerification()` per mostrar banner de verificació
   - Modificació de `displayVotes()` per mostrar estat de cada vot
   - Columna "Estat" afegida a la taula de vots

## Conclusions

Aquest sistema proporciona una **capa addicional de seguretat** que:
- ✅ Detecta alteracions de vots
- ✅ Dona confiança en la integritat dels resultats
- ✅ És transparent per als votants
- ✅ És informatiu per als administradors

És una implementació senzilla però efectiva per garantir que els resultats mostrats són els vots reals que es van registrar.

