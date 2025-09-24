text = input("Introdueix el text a encriptar (sense accents): ")
desplaçament = int(input("Introdueix el desplaçament (nombre enter):"))
abecedarim = "abcdefghijklmnopqrstuvwxyz"
abecedari = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
position = 0
text_encriptat = ""
for i in text:
    if i == " ":
        text_encriptat += " "
    elif i.islower():
        for z in abecedarim:
            if i != z:
                position += 1
            else:
                text_encriptat += abecedarim[(position + desplaçament) % 26]
                position = 0
                break
    elif i.isupper():
        for z in abecedari:
            if i != z:
                position += 1
            else:
                text_encriptat += abecedari[(position + desplaçament) % 26]
                position = 0
                break
    else:
        text_encriptat += i
print("Text encriptat:", text_encriptat)
