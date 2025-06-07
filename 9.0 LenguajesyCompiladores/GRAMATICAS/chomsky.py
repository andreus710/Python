import copy
from collections import defaultdict

def leer_gramatica():
    print("=== Lector de Gramática ===")
    terminales = input("Introduce los terminales (separados por comas): ").replace(" ", "").split(",")
    no_terminales = input("Introduce los no terminales (separados por comas): ").replace(" ", "").split(",")
    simbolo_inicial = input("Introduce el símbolo inicial: ").strip()

    gramatica = defaultdict(list)
    print("\nIntroduce las producciones (usa '->' y separa alternativas con '|'):")
    print("Ejemplo: S -> A B | a")
    print("Escribe 'fin' para terminar.\n")

    while True:
        entrada = input("> ")
        if entrada.lower() == "fin":
            break
        if "->" not in entrada:
            print("Producción inválida. Usa '->'.")
            continue

        izquierda, derecha = entrada.split("->")
        izquierda = izquierda.strip()
        alternativas = [d.strip() for d in derecha.strip().split("|")]
        gramatica[izquierda].extend(alternativas)

    return terminales, no_terminales, simbolo_inicial, dict(gramatica)

# Paso 1: Eliminar símbolos inútiles
def eliminar_simbolos_inutiles(terminales, no_terminales, simbolo_inicial, gramatica):
    # Generadores
    generadores = set()
    cambios = True
    while cambios:
        cambios = False
        for nt, prods in gramatica.items():
            for prod in prods:
                if all(s in terminales or s in generadores for s in prod.split()):
                    if nt not in generadores:
                        generadores.add(nt)
                        cambios = True

    # Alcanzables
    alcanzables = set([simbolo_inicial])
    cola = [simbolo_inicial]
    while cola:
        actual = cola.pop()
        for prod in gramatica.get(actual, []):
            for s in prod.split():
                if s in gramatica and s not in alcanzables:
                    alcanzables.add(s)
                    cola.append(s)

    utiles = generadores & alcanzables
    nueva_gramatica = {
        nt: [p for p in prods if all(s in utiles or s in terminales for s in p.split())]
        for nt, prods in gramatica.items() if nt in utiles
    }
    nuevos_no_terminales = [nt for nt in no_terminales if nt in utiles]
    return terminales, nuevos_no_terminales, simbolo_inicial, nueva_gramatica

# Paso 2: Eliminar ε-producciones
def encontrar_anulables(gramatica):
    anulables = set()
    cambios = True
    while cambios:
        cambios = False
        for nt, prods in gramatica.items():
            for prod in prods:
                if prod == 'ε' or all(s in anulables for s in prod.split()):
                    if nt not in anulables:
                        anulables.add(nt)
                        cambios = True
    return anulables

def eliminar_epsilon(gramatica, simbolo_inicial):
    anulables = encontrar_anulables(gramatica)
    nueva_gramatica = defaultdict(list)

    for nt, prods in gramatica.items():
        for prod in prods:
            if prod == 'ε':
                continue
            symbols = prod.split()
            n = len(symbols)
            for i in range(2 ** n):
                combo = []
                for j in range(n):
                    if not ((i >> j) & 1) or symbols[j] not in anulables:
                        combo.append(symbols[j])
                if combo:
                    nueva_gramatica[nt].append(" ".join(combo))
                elif nt == simbolo_inicial:
                    nueva_gramatica[nt].append("ε")

    return dict(nueva_gramatica)

# Paso 3: Eliminar producciones unitarias
def eliminar_unitarias(gramatica):
    nueva_gramatica = defaultdict(list)
    unitarios = {nt: set([nt]) for nt in gramatica}

    for A in gramatica:
        cambios = True
        while cambios:
            cambios = False
            for B in list(unitarios[A]):
                for prod in gramatica.get(B, []):
                    if prod in gramatica and len(prod.split()) == 1 and prod.isupper():
                        if prod not in unitarios[A]:
                            unitarios[A].add(prod)
                            cambios = True

    for A in gramatica:
        for B in unitarios[A]:
            for prod in gramatica[B]:
                if not (prod.isupper() and prod in gramatica and len(prod.split()) == 1):
                    if prod not in nueva_gramatica[A]:
                        nueva_gramatica[A].append(prod)

    return dict(nueva_gramatica)

# Paso 4: Convertir a Forma Normal de Chomsky
def convertir_a_cnf(gramatica, terminales):
    nueva_gramatica = defaultdict(list)
    terminal_map = {}
    contador = 1

    # Reemplazar terminales en reglas largas
    for nt, prods in gramatica.items():
        for prod in prods:
            symbols = prod.split()
            if len(symbols) == 1:
                nueva_gramatica[nt].append(prod)
            else:
                nueva = []
                for s in symbols:
                    if s in terminales:
                        if s not in terminal_map:
                            new_nt = f"T{contador}"
                            contador += 1
                            terminal_map[s] = new_nt
                            nueva_gramatica[new_nt].append(s)
                        nueva.append(terminal_map[s])
                    else:
                        nueva.append(s)
                nueva_gramatica[nt].append(" ".join(nueva))

    # Convertir reglas con más de 2 símbolos
    convertido = defaultdict(list)
    contador_nt = 1

    for nt, prods in nueva_gramatica.items():
        for prod in prods:
            symbols = prod.split()
            while len(symbols) > 2:
                nuevo = f"X{contador_nt}"
                contador_nt += 1
                convertido[nuevo].append(f"{symbols[0]} {symbols[1]}")
                symbols = [nuevo] + symbols[2:]
            convertido[nt].append(" ".join(symbols))

    return dict(convertido)

# Imprimir gramática
def imprimir_gramatica(gramatica):
    print("\n=== Gramática en Forma Normal de Chomsky ===")
    for nt, prods in gramatica.items():
        print(f"{nt} -> {' | '.join(prods)}")

# Programa principal
terminales, no_terminales, simbolo_inicial, gramatica = leer_gramatica()
terminales, no_terminales, simbolo_inicial, gramatica = eliminar_simbolos_inutiles(
    terminales, no_terminales, simbolo_inicial, gramatica
)
gramatica = eliminar_epsilon(gramatica, simbolo_inicial)
gramatica = eliminar_unitarias(gramatica)
gramatica_cnf = convertir_a_cnf(gramatica, terminales)
imprimir_gramatica(gramatica_cnf)
