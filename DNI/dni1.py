print("Fet per Marçal Maresma\n")
a = int(input("Introdueix el nombre del teu DNI per obtenir la lletra:\n"))
dni = "TRWAGMYFPDXBNJZSQVHLCKE"                     #Assigno les lletres amb la posició concordant amb el nombre que els hi toqui
print(f"Lletra: {dni[a%23]}")                       #Calculo el nombre que surt de la sequència de nombres i li aplico la lletra corresponent assignada anteriorment