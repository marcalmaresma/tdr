# Instruccions per Desencriptar Vots

Aquest document explica com utilitzar el programa `decrypt_votes.py` per desencriptar els noms i DNIs encriptats que s'han guardat a la base de dades.

## Prerequisits

1. **Clau privada RSA**: Necessites el fitxer `.pem` amb la clau privada RSA corresponent a la clau pública que s'utilitza per encriptar les dades.

2. **Dependències**: El programa utilitza les mateixes dependències que l'aplicació principal (ja especificades a `requirements.txt`):
   - cryptography
   - sqlite3 (ja inclòs amb Python)

## Ús del programa

### Opció 1: Execució interactiva

Simplement executa el programa i segueix les instruccions:

```bash
python3 decrypt_votes.py
```

El programa et demanarà:
1. La ruta al fitxer `.pem` amb la clau privada
2. Si vols mostrar els resultats per pantalla, exportar-los a CSV, o ambdues coses

### Opció 2: Amb arguments de línia de comandes

Pots passar la ruta de la clau com a argument:

```bash
python3 decrypt_votes.py /Users/marcal/Downloads/private_key.pem
```

O passar també l'opció directament:

```bash
python3 decrypt_votes.py /Users/marcal/Downloads/private_key.pem 1  # Mostrar per pantalla
python3 decrypt_votes.py /Users/marcal/Downloads/private_key.pem 2  # Exportar a CSV
python3 decrypt_votes.py /Users/marcal/Downloads/private_key.pem 3  # Ambdues
```

## Opcions disponibles

### 1. Mostrar vots desencriptats per pantalla

Aquesta opció desencripta tots els vots i els mostra per pantalla, agrupats per votació. Per cada vot mostra:
- ID del vot
- Nom del votant (desencriptat)
- DNI del votant (desencriptat)
- Opció votada
- Data i hora del vot

**Exemple de sortida:**

```
📊 VOTACIÓ: Eleccions a Delegat de Classe
   Codi: ABC123
   Total vots: 3
--------------------------------------------------------------------------------
   Vot #1 (ID: 1)
      👤 Nom:  Joan Garcia
      🆔 DNI:  12345678Z
      ✅ Opció: Candidat A
      📅 Data: 2025-12-12 10:30:45

   Vot #2 (ID: 2)
      👤 Nom:  Maria Lopez
      🆔 DNI:  87654321X
      ✅ Opció: Candidat B
      📅 Data: 2025-12-12 10:35:20
```

### 2. Exportar vots desencriptats a CSV

Aquesta opció crea un fitxer CSV amb tots els vots desencriptats. El fitxer es crea al mateix directori amb el nom `vots_desencriptats.csv`.

**Columnes del CSV:**
- ID Vot
- Votació
- Codi Votació
- Nom Votant
- DNI Votant
- Opció Votada
- Data Vot

Aquest fitxer es pot obrir amb Excel, LibreOffice Calc, o qualsevol altra eina de fulls de càlcul.

### 3. Ambdues opcions

Executa les dues opcions anteriors consecutivament: primer mostra els resultats per pantalla i després crea el fitxer CSV.

## Seguretat

⚠️ **IMPORTANT - Consideracions de seguretat:**

1. **Protecció de la clau privada**: La clau privada RSA és extremadament sensible. No la comparteixis mai i manté-la en un lloc segur.

2. **Protecció del fitxer CSV**: Si exportes els vots a CSV, recorda que aquest fitxer conté dades personals (noms i DNIs) en text pla. Assegura't de:
   - Esborrar-lo després d'utilitzar-lo
   - No compartir-lo per xarxes insegures
   - Encriptar-lo si necessites guardar-lo

3. **Ús responsable**: Aquest programa només s'hauria d'utilitzar quan sigui estrictament necessari verificar la integritat dels vots o per auditories autoritzades.

4. **Logs i traces**: El programa no guarda logs ni traces de l'execució, però assegura't que la teva terminal no guardi l'historial de comandes amb informació sensible.

## Resolució de problemes

### Error: "No s'ha trobat el fitxer"

Assegura't que la ruta al fitxer `.pem` és correcta. Pots utilitzar:
- Rutes absolutes: `/Users/usuari/Documents/clau_privada.pem`
- Rutes relatives: `./clau_privada.pem`
- Rutes amb ~: `~/Documents/clau_privada.pem`

### Error: "Error carregant la clau privada"

- Verifica que el fitxer és realment un fitxer `.pem` vàlid
- Si la clau privada està protegida amb contrasenya, hauràs de modificar el programa per proporcionar-la

### Error: "Error desencriptant"

Si apareix aquest error per alguns vots, pot ser perquè:
- Les dades s'han encriptat amb una clau pública diferent
- Les dades a la base de dades estan corrompudes
- La clau privada no correspon a la clau pública utilitzada per encriptar

### No s'han trobat vots

Si el programa indica que no hi ha vots:
- Verifica que la base de dades `votacions.db` existeix al mateix directori
- Comprova que realment hi ha vots registrats a l'aplicació

## Exemple complet d'ús

```bash
# 1. Navegar al directori de l'aplicació
cd /Users/marcal/Desktop/TDR/tdr/App_Vot/

# 2. Executar el programa
python3 decrypt_votes.py

# 3. Introduir la ruta de la clau quan es demani
📝 Introdueix la ruta al fitxer .pem amb la clau privada: /Users/marcal/Downloads/private_key.pem

# 4. Si la clau té contrasenya, introduir-la
🔒 La clau privada està protegida amb contrasenya
Introdueix la contrasenya de la clau privada: ********

# 5. Seleccionar opció
Opció (1/2/3): 3

# 6. El programa mostrarà els resultats i crearà el CSV
```

## Notes tècniques

- **Algoritme d'encriptació**: RSA amb OAEP (Optimal Asymmetric Encryption Padding)
- **Funció hash**: SHA-256
- **Mida de clau**: 2048 bits (segons la clau pública definida)
- **Base de dades**: SQLite 3
- **Encoding**: UTF-8 per tots els textos

## Manteniment del programa

Si necessites modificar el programa:
- El codi està ben comentat i documentat
- Les funcions són modulars i es poden reutilitzar
- Pots afegir més opcions d'exportació (JSON, Excel, etc.) modificant la funció corresponent

