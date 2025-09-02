import hashlib

def calcula_md5(filepath):
    with open(filepath, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

fitxer1 = "fitxer1.txt"
fitxer2 = "fitxer2.txt"

md5_1 = calcula_md5(fitxer1)
md5_2 = calcula_md5(fitxer2)

print(f"MD5 de {fitxer1}: {md5_1}")
print(f"MD5 de {fitxer2}: {md5_2}")

if md5_1 == md5_2:
    print("Els fitxers són iguals (MD5 coincidents).")
else:
    print("Els fitxers són diferents (MD5 no coincideixen).")