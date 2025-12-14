# Opcions per Protegir la Contrasenya de l'Admin

## Problema amb RSA per a Contrasenyes

RSA amb OAEP (que utilitzem per DNIs i noms) **NO funciona per comparar contrasenyes** perquè:
- És **no determinístic**: encriptar "12345678" dues vegades dona resultats diferents
- No es poden comparar directament

## Opció 1: Hash SHA-256 (Recomanat) ✓

Utilitzar hash en lloc d'encriptació. Un hash:
- És **determinístic**: mateix input → mateix output
- És **irreversible**: no es pot obtenir la contrasenya original
- És el mètode estàndard per emmagatzemar contrasenyes

**Implementació:**

1. Guardar a la BD el hash de la contrasenya
2. Quan l'admin fa login, hashear la contrasenya introduïda
3. Comparar els dos hash

**Avantatges:**
- Funciona correctament
- Més ràpid que RSA
- Estàndard de la indústria

## Opció 2: Encriptació Simètrica (AES)

Utilitzar AES per encriptar la contrasenya amb una clau secreta.

**Desavantatges:**
- Necessites guardar la clau secreta al servidor (menys segur que hash)
- Més complex

## Opció 3: No Hashear/Encriptar (Actual)

Mantenir la contrasenya en text pla (com està ara).

**Desavantatges:**
- Menys segur si algú accedeix a la base de dades

## Recomanació

Utilitzar **Hash SHA-256** per a la contrasenya de l'admin. És el mètode més segur i estàndard.

Vols que implementi aquesta opció?

