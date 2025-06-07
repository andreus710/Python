#Introduce los terminales: a, b
#Introduce los no terminales: S, A, B, C
#Introduce el símbolo inicial: S

#> S -> A
#> A -> B
#> B -> C
#> C -> a | b
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

def eliminar_producciones_unitarias(gramatica):
    nueva_gramatica = {nt: [] for nt in gramatica}

    # Paso 1: construir el conjunto de cerraduras unitarias para cada no terminal
    unitarios = {nt: set() for nt in gramatica}

    for A in gramatica:
        unitarios[A].add(A)
        cambios = True
        while cambios:
            cambios = False
            for prod in gramatica[A]:
                if prod in gramatica and prod not in unitarios[A]:
                    unitarios[A].add(prod)
                    cambios = True

    # Paso 2: agregar todas las producciones no unitarias
    for A in gramatica:
        for B in unitarios[A]:
            for prod in gramatica.get(B, []):
                if not (prod in gramatica and len(prod.split()) == 1 and prod in unitarios):
                    if prod not in nueva_gramatica[A]:
                        nueva_gramatica[A].append(prod)

    return nueva_gramatica

def imprimir_gramatica(gramatica):
    print("\n=== Gramática sin producciones unitarias ===")
    for nt, prods in gramatica.items():
        if prods:
            print(f"{nt} -> {' | '.join(prods)}")

if __name__ == "__main__":
    # Programa principal
    terminales, no_terminales, simbolo_inicial, gramatica = leer_gramatica()
    gramatica_sin_unitarias = eliminar_producciones_unitarias(gramatica)
    imprimir_gramatica(gramatica_sin_unitarias)
