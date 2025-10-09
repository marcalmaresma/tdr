# Programa senzill de compressió i descompressió RLE sense funcions

while True:
    print("\n--- Compressió RLE ---")
    print("1. Comprimir text")
    print("2. Descomprimir text")
    print("3. Sortir")

    opcio = input("Escull una opció: ")

    if opcio == "1":
        text = input("Introdueix el text a comprimir: ")

        if not text:
            print("Text buit!")
            continue

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

    elif opcio == "2":
        text_comprimit = input("Introdueix el text comprimit: ")

        resultat = ""
        numero = ""

        # Recorrem cada caràcter
        for caracter in text_comprimit:
            if caracter.isdigit():
                numero += caracter
            else:
                resultat += caracter * int(numero)
                numero = ""

        print("Text descomprimit:", resultat)

    elif opcio == "3":
        print("Adeu!")
        break

    else:
        print("Opció no vàlida, torna-ho a provar.")
