# Sistema Blockchain per a Verificació d'Integritat

## ✅ Problema Resolt

Amb el sistema anterior (només MD5), algú amb accés a la base de dades podria:
1. ❌ Modificar un vot
2. ❌ Recalcular el MD5
3. ❌ Actualitzar el MD5 a la BD
4. ❌ El vot semblaria correcte ☹️

Amb el **sistema blockchain**, això és **gairebé impossible** perquè cada vot està enllaçat amb el vot anterior.

## Com Funciona

### 1. Cadena de Hash (Blockchain)

Cada vot conté:
- **Dades pròpies**: votació, opció, DNI hash, timestamp
- **MD5**: Hash de les dades pròpies
- **Hash anterior**: Hash del vot anterior
- **Hash de bloc**: Hash que combina tot (inclou hash anterior)

```
Vot 1:  hash_anterior = "000...000" (genesis)
        hash_bloc = SHA256(dades_vot_1 + md5_1 + "000...000")

Vot 2:  hash_anterior = hash_bloc_vot_1
        hash_bloc = SHA256(dades_vot_2 + md5_2 + hash_bloc_vot_1)

Vot 3:  hash_anterior = hash_bloc_vot_2
        hash_bloc = SHA256(dades_vot_3 + md5_3 + hash_bloc_vot_2)
```

### 2. Exemple Visual

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   Vot 1     │      │   Vot 2     │      │   Vot 3     │
│─────────────│      │─────────────│      │─────────────│
│ Opció: A    │      │ Opció: B    │      │ Opció: C    │
│ DNI: abc... │      │ DNI: def... │      │ DNI: ghi... │
│ MD5: a3f2...│      │ MD5: b4e3...│      │ MD5: c5d4...│
│ Hash Ant: 0 │──┐   │ Hash Ant: x │──┐   │ Hash Ant: y │
│ Hash Bloc: x│  └──▶│ Hash Bloc: y│  └──▶│ Hash Bloc: z│
└─────────────┘      └─────────────┘      └─────────────┘
```

### 3. Verificació Triple

Quan es carreguen els resultats, cada vot es verifica amb **3 checks**:

#### Check 1: MD5 de Dades
```python
vot_data = f"{votacio_id}:{opcio_id}:{dni_hash}:{data_vot}"
md5_calculat = hashlib.md5(vot_data.encode()).hexdigest()
md5_valid = (md5_calculat == md5_guardat)
```

#### Check 2: Cadena de Hash
```python
# El hash_anterior del vot actual ha de coincidir amb
# el hash_bloc del vot anterior
cadena_valid = (hash_anterior_guardat == hash_anterior_esperat)
```

#### Check 3: Hash de Bloc
```python
bloc_data = f"{vot_data}:{md5}:{hash_anterior}"
hash_bloc_calculat = hashlib.sha256(bloc_data.encode()).hexdigest()
bloc_valid = (hash_bloc_calculat == hash_bloc_guardat)
```

**Vot íntegre només si els 3 checks passen!**

## Per Què És Gairebé Impossible d'Alterar

### Escenari: Algú Intenta Modificar el Vot 2

```
ABANS:
Vot 1 → Vot 2 (Opció: B) → Vot 3
        hash: xyz123

INTENT DE MODIFICACIÓ:
Vot 1 → Vot 2 (Opció: C) → Vot 3
        hash: abc456 ❌    hash_anterior: xyz123 ❌ TRENCADA!
```

**Què passa:**
1. Modifiques el Vot 2 (Opció B → C)
2. Recalcules el MD5 del Vot 2
3. Recalcules el hash_bloc del Vot 2 → **CANVIA** (ara és `abc456` en lloc de `xyz123`)
4. ⚠️ **PROBLEMA**: El Vot 3 té `hash_anterior = xyz123`
5. El Vot 3 **no coincideix** amb el nou hash del Vot 2
6. **CADENA TRENCADA** → Detecció immediata! 🚨

### Per Ocultar l'Alteració, Caldria:

1. Modificar el Vot 2
2. Recalcular el seu hash_bloc
3. Modificar el hash_anterior del Vot 3
4. Recalcular el hash_bloc del Vot 3
5. Modificar el hash_anterior del Vot 4
6. Recalcular el hash_bloc del Vot 4
7. ... **TOTS ELS VOTS POSTERIORS**

Això és:
- ⏰ **Molt laboriós** (especialment amb molts vots)
- 🔍 **Altament detectable** (cal modificar desenes/centenars de registres)
- 🧠 **Requereix coneixement profund** de l'algoritme

## Avantatges

### ✅ Immutabilitat Pràctica
No és **matemàticament impossible** alterar, però és **extremadament difícil** sense deixar rastre.

### ✅ Detecció Múltiple
- Si modifiques 1 vot → **2 vots** mostraran error (el modificat + el següent)
- Si modifiques sense actualitzar cadena → **Tots els posteriors** fallen

### ✅ Audit Trail
La cadena mostra l'ordre exacte en què es van emetre els vots.

### ✅ Transparent
L'usuari veu immediatament si hi ha problemes:
- **✓ Cadena intacta**: Tot correcte
- **🔗 CADENA TRENCADA**: Alteració detectada

## Limitacions

### ⚠️ Protecció NO és Absoluta

Si algú:
1. Té accés complet a la BD
2. Coneix l'algoritme exacte
3. Té temps i paciència

Podria recalcular **tota la cadena**. Però:
- És **molt més difícil** que simplement canviar un vot
- Requereix **modificar desenes/centenars de registres**
- És **altament sospitós** (molts registres canviats)

### ✅ Protecció És Molt Alta

Per a la majoria de casos:
- ✅ Protegeix contra errors i corrupcions
- ✅ Protegeix contra modificacions no autoritzades casuales
- ✅ Fa **extremadament difícil** alterar sense ser detectat
- ✅ Proporciona **alta confiança** en la integritat dels resultats

## Estructura de la Base de Dades

### Taula `vots` (amb blockchain)

```sql
CREATE TABLE vots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    votacio_id INTEGER NOT NULL,
    opcio_id INTEGER NOT NULL,
    dni_votant BLOB NOT NULL,
    nom_votant BLOB NOT NULL,
    dni_hash TEXT NOT NULL,
    data_vot TIMESTAMP,
    md5_hash TEXT NOT NULL,           -- Hash de les dades del vot
    hash_anterior TEXT NOT NULL,      -- Hash del vot anterior (blockchain)
    hash_bloc TEXT NOT NULL,          -- Hash d'aquest bloc (inclou hash_anterior)
    ...
)
```

## Visualització a la Interfície

### Banner de Verificació

**Tots els vots correctes:**
```
✓ Verificació Blockchain: Tots els vots són íntegres
X de X vots verificats correctament.
✓ Cadena de hash intacta · ✓ Cap vot alterat
```

**Vots alterats detectats:**
```
⚠️ ALERTA CRÍTICA: S'han detectat vots alterats!
Vots verificats: X | Vots alterats: Y | Total: Z
🔗 CADENA DE HASH TRENCADA - Alteració detectada!
⚠️ Els resultats NO són fiables. El sistema ha estat compromès.
```

## Comparació: MD5 vs Blockchain

| Aspecte | MD5 Sol | MD5 + Blockchain |
|---------|---------|------------------|
| Detecta corrupció | ✅ | ✅ |
| Detecta modificació simple | ✅ | ✅ |
| Protegeix contra modificació + recàlcul | ❌ | ✅ |
| Mostra ordre cronològic | ❌ | ✅ |
| Dificultat d'alterar | Baixa | Molt Alta |
| Overhead computacional | Baix | Mitjà |

## Conclusions

Aquest sistema proporciona:
- 🔒 **Seguretat molt alta** contra alteracions
- 🔍 **Detecció immediata** de manipulacions
- 📊 **Confiança** en la integritat dels resultats
- 🚨 **Alertes clares** quan hi ha problemes

És una implementació **blockchain simplificada** però **altament efectiva** per garantir que els resultats de les votacions són legítims i no han estat manipulats.

---

**Nota tècnica**: Aquest és un sistema "blockchain-like" simplificat. No inclou conceptes com proof-of-work, nodes distribuïts o consensos, que són característics de blockchains públics com Bitcoin. Però utilitza el principi fonamental: **cadena de hash enllaçats** per crear immutabilitat pràctica.

