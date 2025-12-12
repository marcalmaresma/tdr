# 🚀 Guia Ràpida - Desencriptació de Vots

## Comandes per executar amb la teva configuració:

### 1️⃣ Verificar que la clau és correcta

```bash
cd /Users/marcal/Desktop/TDR/tdr/App_Vot/
python3 verify_key.py /Users/marcal/Downloads/private_key.pem
```

Quan et demani la contrasenya, introdueix-la (no es veurà mentre escrius per seguretat).

---

### 2️⃣ Desencriptar i veure els vots per pantalla

```bash
cd /Users/marcal/Desktop/TDR/tdr/App_Vot/
python3 decrypt_votes.py /Users/marcal/Downloads/private_key.pem 1
```

---

### 3️⃣ Desencriptar i exportar a CSV

```bash
cd /Users/marcal/Desktop/TDR/tdr/App_Vot/
python3 decrypt_votes.py /Users/marcal/Downloads/private_key.pem 2
```

Crearà el fitxer: `/Users/marcal/Desktop/TDR/tdr/App_Vot/vots_desencriptats.csv`

---

### 4️⃣ Fer ambdues coses (pantalla + CSV)

```bash
cd /Users/marcal/Desktop/TDR/tdr/App_Vot/
python3 decrypt_votes.py /Users/marcal/Downloads/private_key.pem 3
```

---

## 📝 Notes importants:

- ✅ La clau privada està protegida amb contrasenya
- ✅ El programa detectarà automàticament que té contrasenya i te la demanarà
- ⚠️ **LA CONTRASENYA NO ES VEU mentre l'escrius** - és per seguretat
  - Això vol dir que pots estar escrivint però no veuràs res a la pantalla
  - És COMPLETAMENT NORMAL
  - Escriu la contrasenya i prem Enter (encara que no vegis res)
- ✅ Utilitza `python3` (no `python`)

---

## 🔐 Seguretat:

⚠️ **Després d'utilitzar el CSV, esborra'l:**

```bash
rm /Users/marcal/Desktop/TDR/tdr/App_Vot/vots_desencriptats.csv
```

---

## ❓ Si tens problemes:

1. **"No s'ha trobat el fitxer"** → Verifica que la clau està a `/Users/marcal/Downloads/private_key.pem`
2. **"Contrasenya incorrecta"** → Torna-ho a intentar amb la contrasenya correcta
3. **"No coincideix"** → La clau privada no correspon a la clau pública de l'aplicació

Per més ajuda, consulta: `README_DESENCRIPTACIO.md`

