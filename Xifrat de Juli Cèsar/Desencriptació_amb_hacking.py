text = input("Introdueix el text a desencriptar (sense accents): ")
desplaçament = 0
abecedarim = "abcdefghijklmnopqrstuvwxyz"
abecedari = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
position = 0
text_desencriptat = ""
f = True
q = 0
with open("/Users/marcal/Desktop/TDR/tdr/Xifrat de Juli Cèsar/Dict.txt", "r", encoding="utf-8") as fitxer:
    diccionari = fitxer.read().splitlines()

print(diccionari)
if "casa" in diccionari:
    print("Funciona")

for x in range(1, 26):
    desplaçament = x
    for i in text:
        if i == " ":
            text_desencriptat += " "
        elif i.islower():
            for z in abecedarim:
                if i != z:
                    position += 1
                else:
                    text_desencriptat += abecedarim[(position + desplaçament) % 26]
                    position = 0
                    break
        elif i.isupper():
            for z in abecedari:
                if i != z:
                    position += 1
                else:
                    text_desencriptat += abecedari[(position + desplaçament) % 26]
                    position = 0
                    break
        else:
            text_desencriptat += i

    t_d_split1 = ""
    for p in text_desencriptat:
        if p == " ":
            t_d_split1 += " "
        elif p in abecedarim or p in abecedari:
            t_d_split1 += p.lower()
    t_d_split = t_d_split1.split()

    while f != False:
        if q == len(t_d_split):
            break
        else:
            if t_d_split[q] in diccionari:
                f = True
                q+=1
            else:
                f = False
    if f == True:
        break
    else:
        text_desencriptat = ""
        f = True
        q = 0

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