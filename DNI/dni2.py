print("Fet per Marçal Maresma\n")
a = input("Introdueix el teu DNI per verificar la lletra:\n")
dni = "TRWAGMYFPDXBNJZSQVHLCKE"                  #Assigno les lletres amb la posició concordant amb el nombre que els hi toqui
if len(a) != 9:                                   #Els dnis consten de 9 caràcters, 8 nombres i 1 lletra, per tant si el dni introduit conté un nombre diferent a 9 de caràcters és incorrecte
    print("DNI incorrecte")
else:
    if dni[int(a[0:8])%23] == a[8].upper():       #Calculo la lletra que obtenim del nombre i si coincideix amb la que s'ha introduit és correcte
        print("DNI correcte")
    else:                                         #Si en canvi no coincideix mostro la lletra que correspon al nombre
        print(f"Lletra incorrecta, hauria de ser: {dni[int(a[0:8])%23]}")