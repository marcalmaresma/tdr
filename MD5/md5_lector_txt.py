import hashlib

# Obrir els fitxers en mode lectura
with open("/Users/marcal/Desktop/TDR/tdr/MD5/fitxer1.txt", "r", encoding="utf-8") as f:
    text = f.read()
with open("/Users/marcal/Desktop/TDR/tdr/MD5/fitxer2.txt", "r", encoding="utf-8") as g:
    text2 = g.read()

# Crear objecte MD5
md5_obj = hashlib.md5()
md5_obj2 = hashlib.md5()


# Actualitzar amb el text (convertit a bytes)
md5_obj.update(text.encode('utf-8'))
md5_obj2.update(text2.encode('utf-8'))

# Obtenir el hash en hexadecimal
md5_hash = md5_obj.hexdigest()
md5_hash2 = md5_obj2.hexdigest()

print("1r Text original:", text)
print("MD5:", md5_hash)
print()

print("2n Text original:", text2)
print("MD5:", md5_hash2)
print()

#Comparar els codis hexadecimals obtinguts
if md5_hash == md5_hash2:
    print("MD5 coincidents")
else:
    print("MD5 no coincidents")