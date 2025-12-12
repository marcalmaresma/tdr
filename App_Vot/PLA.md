# Pla d'Implementació - Aplicació Web de Votacions

## 1. Arquitectura General

### Tecnologies
- **Back-end**: Python amb Flask
- **Front-end**: HTML, CSS, JavaScript (vanilla)
- **Base de dades**: SQLite

### Estructura de Fitxers
```
App Votació (Part Pràctica)/
├── app.py                 # Aplicació Flask principal
├── database.py            # Configuració i inicialització de la base de dades
├── static/
│   ├── css/
│   │   └── style.css      # Estils CSS
│   └── js/
│       └── main.js        # JavaScript principal
├── templates/
│   ├── index.html         # Pàgina principal (selecció de rol)
│   ├── admin_login.html   # Login administrador
│   ├── admin_panel.html   # Panell d'administració
│   ├── create_poll.html   # Crear nova votació
│   ├── poll_results.html  # Veure resultats d'una votació
│   ├── voter_login.html   # Login votant (DNI + nom + codi)
│   └── vote.html          # Pàgina de votació
└── votacions.db           # Base de dades SQLite (generada automàticament)
```

## 2. Base de Dades

### Taules

#### `administradors`
- `id` (INTEGER PRIMARY KEY)
- `compte` (TEXT UNIQUE)
- `contrasenya` (TEXT)

#### `votacions`
- `id` (INTEGER PRIMARY KEY)
- `titol` (TEXT)
- `descripcio` (TEXT)
- `codi_votacio` (TEXT UNIQUE) - Generat automàticament
- `data_creacio` (TIMESTAMP)
- `administrador_id` (INTEGER, FOREIGN KEY)

#### `opcions`
- `id` (INTEGER PRIMARY KEY)
- `votacio_id` (INTEGER, FOREIGN KEY)
- `text_opcio` (TEXT)

#### `vots`
- `id` (INTEGER PRIMARY KEY)
- `votacio_id` (INTEGER, FOREIGN KEY)
- `opcio_id` (INTEGER, FOREIGN KEY)
- `dni_votant` (TEXT)
- `nom_votant` (TEXT)
- `data_vot` (TIMESTAMP)

## 3. Funcionalitats Back-end (Flask)

### Endpoints API

#### Autenticació
- `POST /api/admin/login` - Login administrador
- `POST /api/admin/logout` - Logout administrador

#### Votacions (Administrador)
- `GET /api/admin/polls` - Llista totes les votacions de l'admin
- `POST /api/admin/polls` - Crear nova votació
- `GET /api/admin/polls/<poll_id>` - Detalls d'una votació
- `GET /api/admin/polls/<poll_id>/results` - Resultats d'una votació

#### Votacions (Votant)
- `POST /api/voter/verify` - Verificar codi de votació
- `GET /api/voter/poll/<code>` - Obtenir detalls de la votació per codi
- `POST /api/voter/vote` - Enviar vot

### Rutes HTML
- `GET /` - Pàgina principal
- `GET /admin/login` - Formulari login admin
- `GET /admin/panel` - Panell administració
- `GET /admin/polls/new` - Crear votació
- `GET /admin/polls/<poll_id>` - Veure resultats
- `GET /voter/login` - Formulari login votant
- `GET /voter/vote/<code>` - Pàgina de votació

## 4. Funcionalitats Front-end

### Pàgina Principal (`index.html`)
- Botons per seleccionar rol (Administrador / Votant)

### Login Administrador (`admin_login.html`)
- Formulari: compte i contrasenya
- Validació client-side
- Redirecció al panell si correcte

### Panell Administració (`admin_panel.html`)
- Llista de votacions creades
- Botó per crear nova votació
- Botó per veure resultats de cada votació
- Mostra codi de votació per cada votació

### Crear Votació (`create_poll.html`)
- Formulari: títol, descripció
- Afegir/eliminar opcions dinàmicament
- Generació automàtica de codi de votació

### Resultats Votació (`poll_results.html`)
- Títol i descripció de la votació
- Taula amb recompte de vots per opció
- Llista de vots individuals (DNI, nom, opció escollida)

### Login Votant (`voter_login.html`)
- Formulari: DNI, nom, codi de votació
- Verificació del codi
- Redirecció a la pàgina de votació

### Pàgina de Votació (`vote.html`)
- Mostra títol i descripció
- Llista d'opcions (radio buttons o botons)
- Botó per enviar vot
- Prevenció de votació múltiple (opcional, per simplificar no ho implementem)

## 5. Seguretat i Validacions

### Administrador
- Contrasenya hardcoded: "12345678" per compte "MarçalMaresma"
- Sessions amb Flask sessions
- Verificació de sessió en rutes protegides

### Votant
- No validació DNI (com sol·licitat)
- Verificació que el codi de votació existeix
- Permet múltiples vots (no hi ha restricció explícita)

## 6. Generació de Codi de Votació

- Format: Alphanumèric aleatori (ex: "ABC123", "XYZ789")
- Longitud: 6-8 caràcters
- Únic a la base de dades

## 7. Estils CSS

- Disseny modern i net
- Responsive design
- Colors diferenciats per rols
- Formularis ben estructurats

## 8. Implementació

### Ordre d'Implementació
1. Base de dades i models
2. Back-end Flask (endpoints API)
3. Templates HTML bàsics
4. JavaScript per interactivitat
5. Estils CSS
6. Proves i ajustos

