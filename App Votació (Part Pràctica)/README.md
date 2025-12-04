# Sistema de Votacions Web

Aplicació web per gestionar votacions amb dos rols: administrador i votant.

## Tecnologies Utilitzades

- **Back-end**: Python 3 amb Flask
- **Front-end**: HTML, CSS, JavaScript (vanilla)
- **Base de dades**: SQLite

## Requisits

- **Python 3.7 o superior** (recomanat Python 3.8+)
- pip (gestor de paquets de Python)

## Instal·lació

### 1. Instal·lar dependències

```bash
pip3 install flask
```

O utilitzant el fitxer `requirements.txt`:

```bash
pip3 install -r requirements.txt
```

### 2. Inicialitzar la base de dades

La base de dades s'inicialitza automàticament quan s'executa l'aplicació per primera vegada. Si vols inicialitzar-la manualment:

```bash
python3 database.py
```

## Executar l'Aplicació

```bash
python3 app.py
```

L'aplicació estarà disponible a: `http://localhost:5000`

## Funcionalitats

### Administrador

**Credencials per defecte:**
- Compte: `MarçalMaresma`
- Contrasenya: `12345678`

**Funcions disponibles:**
1. **Login**: Accedir al panell d'administració amb compte i contrasenya
2. **Crear Votació**: Crear noves votacions amb títol, descripció i múltiples opcions
3. **Veure Resultats**: Consultar els resultats de les votacions creates, incloent:
   - Recompte de vots per opció
   - Percentatges
   - Llista detallada de tots els vots individuals
4. **Codi de Votació**: Cada votació té un codi únic que s'ha de compartir amb els votants

### Votant

**Funcions disponibles:**
1. **Accés**: Introduir DNI, nom i codi de votació per accedir
2. **Votar**: Seleccionar una opció i enviar el vot
3. **No validació DNI**: El sistema no valida el format del DNI (com sol·licitat)

## Estructura del Projecte

```
App Votació (Part Pràctica)/
├── app.py                 # Aplicació Flask principal
├── database.py            # Configuració de la base de dades
├── requirements.txt       # Dependències Python
├── votacions.db           # Base de dades SQLite (generada automàticament)
├── static/
│   ├── css/
│   │   └── style.css      # Estils CSS
│   └── js/
│       ├── admin_login.js
│       ├── admin_panel.js
│       ├── create_poll.js
│       ├── poll_results.js
│       ├── voter_login.js
│       └── vote.js
└── templates/
    ├── index.html         # Pàgina principal
    ├── admin_login.html   # Login administrador
    ├── admin_panel.html   # Panell d'administració
    ├── create_poll.html   # Crear votació
    ├── poll_results.html  # Resultats
    ├── voter_login.html   # Login votant
    └── vote.html          # Pàgina de votació
```

## Base de Dades

### Taules

- **administradors**: Emmagatzema les credencials dels administradors
- **votacions**: Informació de les votacions (títol, descripció, codi, etc.)
- **opcions**: Opcions disponibles per a cada votació
- **vots**: Registre de tots els vots emesos (DNI, nom, opció escollida, data)

## Notes Importants

- **No s'encripten els vots**: Els vots s'emmagatzemen en text pla a la base de dades
- **No hi ha validació de DNI**: El sistema accepta qualsevol text com a DNI
- **Múltiples vots**: El sistema permet que la mateixa persona voti múltiples vegades (no hi ha restricció implementada)
- **Codi de votació**: Es genera automàticament i és únic per cada votació

## Desenvolupament

Per executar en mode desenvolupament:

```bash
python3 app.py
```

L'aplicació s'executarà en mode debug, permetent veure errors detallats i recarregar automàticament quan hi ha canvis.

