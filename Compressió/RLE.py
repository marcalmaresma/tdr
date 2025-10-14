# Programa senzill de compressió i descompressió RLE sense funcions
print("\n--- Compressió RLE ---")
print("1. Comprimir text")
print("2. Descomprimir text")

opcio = input("Escull una opció: ").strip()

if opcio == "1":
    text = input("Introdueix el text a comprimir: ")
    if not text:
        print("Text buit!")
        exit()

    resultat = ""
    comptador = 1
    lletra_anterior = text[0]

    # Recorrem cada lletra a partir de la segona
    for lletra in text[1:]:
        if lletra == lletra_anterior:
            comptador += 1
        else:
            resultat += str(comptador) + lletra_anterior
            lletra_anterior = lletra
            comptador = 1

    # Afegim l’última seqüència
    resultat += str(comptador) + lletra_anterior

    print("Text comprimit:", resultat)
    exit()
elif opcio == "2":
    text_comprimit = input("Introdueix el text comprimit: ")
    if not text_comprimit:
        print("Text buit!")
        exit()

    resultat = ""
    numero = ""

    # Recorrem cada caràcter
    for caracter in text_comprimit:
        if caracter.isdigit():
            numero += caracter
        else:
            if not numero:
                print("Format invàlid: falta nombre abans del caràcter")
                exit()
            try:
                resultat += caracter * int(numero)
            except ValueError:
                print("Nombre invàlid a la cadena comprimida")
                exit()
            numero = ""

    if numero:
        print("Format invàlid: cadena acaba amb número sols")
        exit()

    print("Text descomprimit:", resultat)
    exit()
else:
    print("Opció no vàlida, torna-ho a provar.")
    exit()