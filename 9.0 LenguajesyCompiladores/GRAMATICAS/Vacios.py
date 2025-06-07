#Introduce los terminales: a, b
#Introduce los no terminales: S, A, B
#Introduce el símbolo inicial: S

#> S -> A B
#> A -> a | ε
#> B -> b | ε
#> fin

def leer_gramatica():
    print("=== Lector de Gramática ===")
    terminales = input("Introduce los terminales (separados por comas): ").replace(" ", "").split(",")
    no_terminales = input("Introduce los no terminales (separados por comas): ").replace(" ", "").split(",")
    simbolo_inicial = input("Introduce el símbolo inicial: ").strip()

    gramatica = {}
    print("\nIntroduce las producciones (usa '->' y separa alternativas con '|'):")
    print("Ejemplo: S -> A B | ε")
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

        if izquierda not in gramatica:
            gramatica[izquierda] = []
        gramatica[izquierda].extend(alternativas)

    return terminales, no_terminales, simbolo_inicial, gramatica

def encontrar_generadores_vacios(gramatica):
    """Encuentra los símbolos que pueden derivar ε."""
    anulables = set()

    # Primera pasada: si hay producción directa a ε
    for nt, prods in gramatica.items():
        if 'ε' in prods:
            anulables.add(nt)

    # Iterativamente, agregar aquellos que pueden producir solo anulables
    cambio = True
    while cambio:
        cambio = False
        for nt, prods in gramatica.items():
            if nt in anulables:
                continue
            for prod in prods:
                if all(s in anulables for s in prod.split()):
                    anulables.add(nt)
                    cambio = True
                    break
    return anulables

def eliminar_producciones_vacias(gramatica, simbolo_inicial):
    anulables = encontrar_generadores_vacios(gramatica)
    nueva_gramatica = {}

    for nt, prods in gramatica.items():
        nuevas_prods = set()
        for prod in prods:
            if prod == 'ε':
                continue  # eliminamos ε
            simbolos = prod.split()
            # Generar todas las combinaciones sin símbolos anulables
            n = len(simbolos)
            combinaciones = [[]]

            for s in simbolos:
                nuevas = []
                if s in anulables:
                    for c in combinaciones:
                        nuevas.append(c + [s])      # con el símbolo
                        nuevas.append(c)            # sin el símbolo
                else:
                    for c in combinaciones:
                        nuevas.append(c + [s])
                combinaciones = nuevas

            for c in combinaciones:
                if c:
                    nuevas_prods.add(" ".join(c))
                elif nt == simbolo_inicial:
                    nuevas_prods.add("ε")  # solo se permite ε si nt es inicial

        if nuevas_prods:
            nueva_gramatica[nt] = list(nuevas_prods)

    return nueva_gramatica

def imprimir_gramatica(gramatica):
    print("\n=== Gramática sin producciones vacías ===")
    for nt, prods in gramatica.items():
        print(f"{nt} -> {' | '.join(prods)}")

if __name__ == "__main__":
    # Programa principal
    terminales, no_terminales, simbolo_inicial, gramatica = leer_gramatica()
    gramatica_sin_vacios = eliminar_producciones_vacias(gramatica, simbolo_inicial)
    imprimir_gramatica(gramatica_sin_vacios)
