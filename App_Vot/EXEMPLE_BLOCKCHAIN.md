# Exemple Pràctic: Com Funciona el Blockchain

## Escenari: 3 Vots en una Votació

### 📊 Vots Registrats

```
Votant 1: DNI 12345678Z vota Opció A a les 10:00
Votant 2: DNI 87654321X vota Opció B a les 10:15
Votant 3: DNI 11111111H vota Opció A a les 10:30
```

## 🔗 Cadena de Hash (Simplificat)

```
┌────────────────────────────────────────────────────┐
│                    Vot 1                           │
│────────────────────────────────────────────────────│
│ Votació: 1                                         │
│ Opció: A (id=1)                                    │
│ DNI Hash: a3f2c8d9...                              │
│ Timestamp: 2025-12-15T10:00:00                     │
│                                                    │
│ MD5 (dades): 7e8f9a1b2c3d4e5f...                  │
│ Hash Anterior: 0000000000000000... (genesis)      │
│ Hash Bloc: x1y2z3a4b5c6d7e8...  ◄───────┐         │
└────────────────────────────────────────────────────┘
                                           │
                                           │
┌────────────────────────────────────────────────────┐
│                    Vot 2                 │         │
│──────────────────────────────────────────│─────────┘
│ Votació: 1                               │
│ Opció: B (id=2)                          │
│ DNI Hash: b4e3d2c1...                    │
│ Timestamp: 2025-12-15T10:15:00           │
│                                          │
│ MD5 (dades): 8f9g0h1i2j3k4l5m...        │
│ Hash Anterior: x1y2z3a4b5c6d7e8... ◄────┘ (vot 1)
│ Hash Bloc: m6n7o8p9q0r1s2t3...  ◄───────┐
└────────────────────────────────────────────────────┘
                                           │
                                           │
┌────────────────────────────────────────────────────┐
│                    Vot 3                 │         │
│──────────────────────────────────────────│─────────┘
│ Votació: 1                               │
│ Opció: A (id=1)                          │
│ DNI Hash: c5d4e3f2...                    │
│ Timestamp: 2025-12-15T10:30:00           │
│                                          │
│ MD5 (dades): 9g0h1i2j3k4l5m6n...        │
│ Hash Anterior: m6n7o8p9q0r1s2t3... ◄────┘ (vot 2)
│ Hash Bloc: u4v5w6x7y8z9a0b1...
└────────────────────────────────────────────────────┘
```

## 🚨 Intent d'Alteració: Modificar el Vot 2

### Atac: Canviar Vot 2 d'Opció B → Opció C

```
ABANS:
Vot 1 → Vot 2 (Opció B) → Vot 3
        Hash Bloc: m6n7o8...

DESPRÉS (modificació):
Vot 1 → Vot 2 (Opció C) → Vot 3
        Hash Bloc: p9q8r7... ❌
                              ↓
                    Hash Anterior: m6n7o8... ❌
                    ⚠️ NO COINCIDEIX!
```

### Què Detecta el Sistema

```
✅ Vot 1: Verificat
   - MD5 correcte ✓
   - Hash anterior correcte ✓ (genesis)
   - Hash bloc correcte ✓

❌ Vot 2: ALTERAT
   - MD5 correcte ✓ (recalculat per l'atacant)
   - Hash anterior correcte ✓ (apunta a Vot 1)
   - Hash bloc ❌ DIFERENT DEL GUARDAT

❌ Vot 3: ALTERAT
   - MD5 correcte ✓
   - Hash anterior ❌ NO COINCIDEIX (apunta a hash antic del Vot 2)
   - Hash bloc ❌ INCORRECTE
```

### Resultat a la Interfície

```
⚠️ ALERTA CRÍTICA: S'han detectat vots alterats!
Vots verificats: 1 | Vots alterats: 2 | Total: 3
🔗 CADENA DE HASH TRENCADA - Alteració detectada!
⚠️ Els resultats NO són fiables. El sistema ha estat compromès.
```

## 🔐 Per Què És Segur

### Per Ocultar l'Alteració, l'Atacant Hauria de:

1. **Modificar Vot 2:**
   - Canviar `opcio_id` de 2 a 3
   - Recalcular `md5_hash`
   - Recalcular `hash_bloc` → nou hash: `p9q8r7...`

2. **Actualitzar Vot 3:**
   - Canviar `hash_anterior` de `m6n7o8...` a `p9q8r7...`
   - Recalcular `hash_bloc` → nou hash: `x1y2z3...`

3. **Actualitzar Vot 4** (si existeix):
   - Canviar `hash_anterior`
   - Recalcular `hash_bloc`

4. **... i així TOTS els vots posteriors**

### Per una Votació amb 100 vots:

- Modificar 1 vot = **recalcular 99 registres**
- Extremadament sospitós
- Fàcil d'auditar (timestamps de modificació de BD)

## 📊 Comparació: Abans vs Després

### Abans (només MD5)

```
Atacant:
1. Modifica Vot 2 (Opció B → C)
2. Recalcula MD5 del Vot 2
3. Actualitza MD5 a la BD

Resultat: ✅ Vot sembla correcte ☹️
```

### Després (Blockchain)

```
Atacant:
1. Modifica Vot 2 (Opció B → C)
2. Recalcula MD5 del Vot 2
3. Recalcula hash_bloc del Vot 2
4. PROBLEMA: Vot 3 ja no enllaça correctament!

Resultat: ❌ 2 vots surten com alterats
          🔗 Cadena trencada detectada
```

## ✅ Conclusions

El sistema blockchain:
- ✅ **Enllaça** tots els vots en una cadena
- ✅ **Detecta** qualsevol modificació
- ✅ **Mostra** exactament quins vots estan alterats
- ✅ **Fa extremadament difícil** modificar sense ser detectat
- ✅ **Proporciona confiança** que els resultats són legítims

És com un **segell de seguretat**: si algú l'obre, es veu immediatament. 🔒

