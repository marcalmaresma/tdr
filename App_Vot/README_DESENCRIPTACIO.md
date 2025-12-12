# Eines de Desencriptació - Sistema de Votació

Aquest conjunt d'eines permet gestionar les claus RSA i desencriptar els noms i DNIs encriptats que es guarden a la base de dades del sistema de votació.

## 📋 Índex

1. [Resum de les eines disponibles](#resum-de-les-eines-disponibles)
2. [Flux de treball recomanat](#flux-de-treball-recomanat)
3. [Guia ràpida d'ús](#guia-ràpida-dús)
4. [Seguretat i bones pràctiques](#seguretat-i-bones-pràctiques)

---

## Resum de les eines disponibles

### 1. 🔐 `verify_key.py` - Verificador de clau privada

**Propòsit:** Verificar que una clau privada correspon a la clau pública utilitzada per l'aplicació.

**Ús:**
```bash
python3 verify_key.py /Users/marcal/Downloads/private_key.pem
```

**Quan utilitzar-lo:**
- Abans de desencriptar, per assegurar-te que tens la clau correcta
- Per verificar que una clau de backup és la correcta
- Per comprovar que una clau privada correspon amb la clau pública hardcoded

**Sortida:**
- ✅ Confirmació si la clau coincideix
- ❌ Informació detallada si no coincideix
- Mostra els valors de n i e per comparació

---

### 2. 🔓 `decrypt_votes.py` - Desencriptador de vots

**Propòsit:** Desencriptar tots els noms i DNIs de la base de dades utilitzant la clau privada.

**Ús:**
```bash
python3 decrypt_votes.py /Users/marcal/Downloads/private_key.pem [opció]
```

**Opcions:**
- **1**: Mostrar vots desencriptats per pantalla
- **2**: Exportar vots desencriptats a CSV
- **3**: Ambdues opcions

**Quan utilitzar-lo:**
- Per auditar els vots d'una votació
- Per verificar la identitat dels votants
- Per exportar dades per a anàlisi

**Sortida:**
- Visualització formatada dels vots per pantalla
- Fitxer `vots_desencriptats.csv` amb totes les dades

📖 Més detalls: Consulta [DESENCRIPTACIO_INSTRUCCIONS.md](DESENCRIPTACIO_INSTRUCCIONS.md)

---

### 3. 🔑 `generate_keypair.py` - Generador de parells de claus

**Propòsit:** Generar un nou parell de claus RSA (pública i privada).

**Ús:**
```bash
python3 generate_keypair.py
```

**⚠️ AVÍS IMPORTANT:** Aquest script genera NOVES claus. Si ja tens dades encriptades, NO podràs desencriptar-les amb aquestes noves claus.

**Quan utilitzar-lo:**
- Quan configures l'aplicació per primera vegada
- Si vols començar amb claus noves (perdràs accés a dades antigues)
- Per generar claus de prova en entorns de desenvolupament

**Sortida:**
- Fitxer `private_key.pem` - Clau privada (GUARDAR EN LLOC SEGUR)
- Fitxer `public_key.pem` - Clau pública
- Valors de PUBLIC_KEY_N i PUBLIC_KEY_E per actualitzar `crypto_utils.py`

---

## Flux de treball recomanat

### Escenari 1: Tens la clau privada i vols desencriptar vots

```bash
# Pas 1: Verificar que tens la clau correcta
python3 verify_key.py /Users/marcal/Downloads/private_key.pem

# Pas 2: Si la verificació és correcta, desencriptar
python3 decrypt_votes.py /Users/marcal/Downloads/private_key.pem 3
```

### Escenari 2: Configuració inicial de l'aplicació

```bash
# Pas 1: Generar noves claus
python3 generate_keypair.py

# Pas 2: Actualitzar crypto_utils.py amb els valors mostrats

# Pas 3: Guardar private_key.pem en un lloc segur

# Pas 4: Opcional - Verificar la clau
python3 verify_key.py /Users/marcal/Downloads/private_key.pem
```

### Escenari 3: Has perdut la clau privada

❌ **Malauradament, si has perdut la clau privada original, NO hi ha forma de recuperar les dades encriptades.**

Opcions:
1. Buscar còpies de seguretat de la clau privada
2. Si no la trobes, hauràs de generar noves claus i començar de zero
3. Les dades antigues quedaran permanentment encriptades

---

## Guia ràpida d'ús

### Desencriptar i veure resultats per pantalla

```bash
python3 decrypt_votes.py /Users/marcal/Downloads/private_key.pem 1
```

### Desencriptar i exportar a CSV

```bash
python3 decrypt_votes.py /Users/marcal/Downloads/private_key.pem 2
```

### Verificar una clau abans de desencriptar

```bash
python3 verify_key.py /Users/marcal/Downloads/private_key.pem && python3 decrypt_votes.py /Users/marcal/Downloads/private_key.pem 1
```

---

## Seguretat i bones pràctiques

### 🔒 Protecció de la clau privada

1. **Mai comparteixis la clau privada**: És l'únic mecanisme per desencriptar les dades
2. **Fes còpies de seguretat**: Guarda la clau en múltiples llocs segurs
3. **Utilitza permisos restrictius**: 
   ```bash
   chmod 600 private_key.pem
   ```
4. **Considera l'encriptació amb contrasenya**: Protegeix la clau amb una contrasenya addicional

### 🗑️ Gestió de fitxers desencriptats

1. **Esborra el CSV després d'utilitzar-lo**:
   ```bash
   rm vots_desencriptats.csv
   ```

2. **No el comparteixis per xarxes insegures**: Conté dades personals

3. **Si necessites guardar-lo, encripta'l**:
   ```bash
   # Exemple amb GPG
   gpg -c vots_desencriptats.csv
   rm vots_desencriptats.csv
   ```

### 📋 Auditoria i registres

- Els scripts NO guarden logs de les operacions
- Assegura't que el teu terminal no guarda l'historial amb informació sensible
- Utilitza aquests scripts només quan sigui estrictament necessari

### ⚖️ Compliment legal

- Aquestes eines s'han de fer servir només per auditories autoritzades
- Assegura't de complir amb la legislació de protecció de dades (GDPR/LOPD)
- Documenta l'ús de les eines per a auditories

---

## Resolució de problemes comuns

### "No s'ha trobat el fitxer"
→ Verifica la ruta al fitxer .pem. Utilitza rutes absolutes o relatives correctes.

### "Error carregant la clau privada"
→ Assegura't que el fitxer és un .pem vàlid. Si està protegit amb contrasenya, hauràs de modificar el codi.

### "NO COINCIDEIX" (verify_key.py)
→ La clau privada no correspon a la clau pública de l'aplicació. Busca la clau correcta o actualitza crypto_utils.py.

### "Error desencriptant"
→ Algunes dades no es poden desencriptar. Possibles causes:
- Clau privada incorrecta
- Dades corrompudes a la base de dades
- Dades encriptades amb una clau diferent

### "No s'han trobat vots"
→ La base de dades està buida o no existeix. Verifica que `votacions.db` existeix i conté vots.

---

## Informació tècnica

### Especificacions de l'encriptació

- **Algoritme**: RSA 2048 bits
- **Padding**: OAEP (Optimal Asymmetric Encryption Padding)
- **Funció hash**: SHA-256
- **MGF**: MGF1 amb SHA-256
- **Base de dades**: SQLite 3
- **Encoding de text**: UTF-8

### Estructura de la base de dades

Taula `vots`:
- `id`: INTEGER (PRIMARY KEY)
- `votacio_id`: INTEGER (FOREIGN KEY)
- `opcio_id`: INTEGER (FOREIGN KEY)
- `dni_votant`: BLOB (encriptat amb RSA)
- `nom_votant`: BLOB (encriptat amb RSA)
- `data_vot`: TIMESTAMP

### Dependències

Totes les dependències estan especificades a `requirements.txt`:
- `cryptography` - Per a operacions criptogràfiques
- `Flask` - Framework web
- Altres dependències de l'aplicació principal

---

## Contacte i suport

Per a més informació sobre el sistema de votació, consulta:
- [README.md](README.md) - Documentació principal de l'aplicació
- [ENCRIPTACIO.md](ENCRIPTACIO.md) - Detalls sobre el sistema d'encriptació
- [PLA.md](PLA.md) - Pla de desenvolupament del projecte

---

**Versió:** 1.0  
**Data:** Desembre 2025  
**Autor:** Sistema de Votació TDR

