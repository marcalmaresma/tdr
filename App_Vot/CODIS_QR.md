# Codis QR per a Votacions

## 📱 Funcionalitat Implementada

El sistema ara genera automàticament **codis QR** per a cada votació que et permeten compartir l'accés de forma ràpida i còmoda.

---

## 🎯 Com Funciona

### 1. **Al Panell d'Administració**

Quan crees una votació, al panell d'administració veuràs:
- El **codi alfanumèric** tradicional (ex: `A3B5C7`)
- Un **codi QR** al costat

```
┌─────────────────────────────────────┐
│  Títol: Votació President          │
│  Descripció: Elecció anual          │
│                                     │
│  Codi: A3B5C7     ┌───────────┐   │
│  Termini: ...     │  ▓▓░░▓▓   │   │
│                   │  ░░▓▓░░   │   │
│                   │  ▓▓▓▓▓▓   │   │
│                   └───────────┘   │
│                Escaneja per votar  │
└─────────────────────────────────────┘
```

### 2. **Escanejant el QR**

Quan algú escaneja el codi QR amb el seu mòbil:

1. **Es redirigeix automàticament** a: `https://www.sistemavot.cat/voter/login?code=A3B5C7`
2. El **codi de votació ja està omplert** automàticament
3. El votant només ha d'introduir el seu **DNI i nom**
4. Pot votar immediatament

### 3. **Avantatges**

✅ **Més ràpid**: No cal escriure el codi manualment  
✅ **Sense errors**: Evita errors de transcripció  
✅ **Més còmode**: Escaneja i vota en segons  
✅ **Accessible**: Funciona amb qualsevol càmera de mòbil  

---

## 🔧 Detalls Tècnics

### Endpoint de l'API

```
GET /api/qr/<codi_votacio>
```

Retorna una imatge PNG del codi QR.

### URL Codificada al QR

```
https://www.sistemavot.cat/voter/login?code=<CODI>
```

### Llibreries Utilitzades

- **qrcode** (Python): Generació de codis QR
- **Pillow**: Processament d'imatges

### Mida del QR

- **Desktop**: 150x150 px
- **Mòbil**: 120x120 px (responsive)

---

## 📋 Ús Recomanat

### Per a l'Administrador:

1. Crea la votació al panell d'admin
2. Comparteix el **codi QR**:
   - Projecta-lo en una pantalla
   - Envia'l per correu/WhatsApp
   - Imprimeix-lo en cartells
3. Els votants escanegen i voten

### Per al Votant:

1. Escaneja el codi QR amb la càmera del mòbil
2. S'obre automàticament el navegador
3. Introdueix DNI i nom
4. Vota!

---

## 🎨 Personalització

Si vols canviar l'estil del QR, modifica els paràmetres a `app.py`:

```python
qr = qrcode.QRCode(
    version=1,  # Mida del QR (1-40)
    error_correction=qrcode.constants.ERROR_CORRECT_L,  # Nivell de correcció d'errors
    box_size=10,  # Mida de cada quadrat
    border=4,  # Marge exterior
)
```

### Nivells de Correcció d'Errors:

- `ERROR_CORRECT_L`: ~7% (més ràpid)
- `ERROR_CORRECT_M`: ~15%
- `ERROR_CORRECT_Q`: ~25%
- `ERROR_CORRECT_H`: ~30% (més robust)

---

## 🚀 Millores Futures (Opcionals)

- [ ] Botó per **descarregar** el QR com a imatge
- [ ] **Personalitzar colors** del QR
- [ ] Afegir **logo** al centre del QR
- [ ] Generar **PDF** amb el QR i les instruccions
- [ ] **Estadístiques** de quants vots venen per QR vs. manual

---

## ✅ Testat amb:

- iPhone (iOS 16+)
- Android (11+)
- Aplicacions natives de càmera
- Google Lens
- Aplicacions de lectura de QR

---

**Data d'implementació**: Desembre 2025  
**Autor**: Sistema de Votacions - TDR Marçal Maresma Roig

