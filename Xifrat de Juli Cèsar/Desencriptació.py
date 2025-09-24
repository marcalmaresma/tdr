text = input("Introdueix el text a desencriptar (sense accents): ")
desplaçament = int(input("Introdueix el desplaçament (nombre enter):"))
abecedarim = "abcdefghijklmnopqrstuvwxyz"
abecedari = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
position = 0
text_desencriptat = ""
for i in text:
    if i == " ":
        text_desencriptat += " "
    elif i.islower():
        for z in abecedarim[::-1]:
            if i != z:
                position += 1
            else:
                text_desencriptat += abecedarim[(len(abecedarim)-1 - position - desplaçament) % 26]
                position = 0
                break
    elif i.isupper():
        for z in abecedari[::-1]:
            if i != z:
                position += 1
            else:
                text_desencriptat += abecedari[(len(abecedari)-1 - position - desplaçament) % 26]
                position = 0
                break
    else:
        text_desencriptat += i
print("Text desencriptat:", text_desencriptat)
