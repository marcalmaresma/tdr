import heapq

text = input("Introdueix el text a comprimir: ")
repeticions = {}
for lletra in text:
    if lletra in repeticions:
        repeticions[lletra] += 1
    else:
        repeticions[lletra] = 1

# construir arbre de Huffman amb un heap (freq, contador, node)
heap = []
contador = 0
for lletra, freq in repeticions.items():
    heapq.heappush(heap, (freq, contador, lletra))  # fulla: node = lletra (string)
    contador += 1

# combinar nodes fins a tenir l'arbre complet
while len(heap) > 1:
    f1, _, n1 = heapq.heappop(heap)
    f2, _, n2 = heapq.heappop(heap)
    # posar el fill amb més freqüència a l'esquerre perquè rebi '0' abans
    node = (n2, n1)  # abans estava (n1, n2)
    heapq.heappush(heap, (f1 + f2, contador, node))
    contador += 1

root = heap[0][2] if heap else None

# assignar codis fent un recorregut iteratiu (evita definir funcions noves)
assignacions = {}
if root is None:
    assignacions = {}
elif isinstance(root, str):
    # només un caràcter al text -> donar-li '0'
    assignacions[root] = "0"
else:
    stack = [(root, "")]  # (node, codi_actual)
    while stack:
        node, codi = stack.pop()
        left, right = node

        # si ambdós fills són nodes, empilem dret primer i esquerre després
        # així l'esquerre es processa abans (LIFO) i s'insereix primer al dict
        if not isinstance(left, str) and not isinstance(right, str):
            stack.append((right, codi + "1"))
            stack.append((left, codi + "0"))
            continue

        # en la resta de casos, assignem l'esquerre abans de la dreta
        if isinstance(left, str):
            assignacions[left] = codi + "0"
        else:
            stack.append((left, codi + "0"))

        if isinstance(right, str):
            assignacions[right] = codi + "1"
        else:
            stack.append((right, codi + "1"))

print(assignacions)
comprimit = ""
for i in text:
    comprimit += assignacions[i]
print("Text comprimit:", comprimit)
    