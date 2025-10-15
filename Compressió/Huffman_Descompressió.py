import ast

Arbre = input("Introdueix el diccionari amb l'arbre de Huffman:")
Arbredef = ast.literal_eval(Arbre)
Comprimit = input("Introdueix el text comprimit en binari:")
Num = ""
for i in Comprimit:
    Num += i
    for k, v in Arbredef.items():
        if Num == v:
            print(k, end="")
            Num = ""
            break