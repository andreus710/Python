#Introduce los terminales: a, b
#Introduce los no terminales: S, A, B, C
#Introduce el símbolo inicial: S

#> S -> A b
#> A -> a
#> B -> b
#> C -> A
#> fin

def leer_gramatica():
    print("=== Lector de Gramática ===")
    terminales = input("Introduce los terminales (separados por comas): ").replace(" ", "").split(",")
    no_terminales = input("Introduce los no terminales (separados por comas): ").replace(" ", "").split(",")
    simbolo_inicial = input("Introduce el símbolo inicial: ").strip()

    gramatica = {}
    print("\nIntroduce las producciones (usa '->' y separa alternativas con '|'):")
    print("Ejemplo: E -> E+T | T")
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


def obtener_generadores(gramatica, terminales):
    generadores = set()

    while True:
        cambios = False
        for nt, prods in gramatica.items():
            if nt in generadores:
                continue
            for prod in prods:
                simbolos = prod.split()
                if all(s in terminales or s in generadores or s == 'ε' for s in simbolos):
                    generadores.add(nt)
                    cambios = True
                    break
        if not cambios:
            break

    return generadores


def obtener_alcanzables(gramatica, simbolo_inicial):
    alcanzables = set([simbolo_inicial])
    cola = [simbolo_inicial]

    while cola:
        actual = cola.pop(0)
        for prod in gramatica.get(actual, []):
            for simbolo in prod.split():
                if simbolo in gramatica and simbolo not in alcanzables:
                    alcanzables.add(simbolo)
                    cola.append(simbolo)

    return alcanzables


def eliminar_simbolos_inutiles(terminales, no_terminales, simbolo_inicial, gramatica):
    generadores = obtener_generadores(gramatica, terminales)
    alcanzables = obtener_alcanzables(gramatica, simbolo_inicial)

    utiles = generadores & alcanzables

    nueva_gramatica = {
        nt: [p for p in prods if all(s in terminales or s in utiles or s == 'ε' for s in p.split())]
        for nt, prods in gramatica.items() if nt in utiles
    }

    nuevos_no_terminales = [nt for nt in no_terminales if nt in utiles]

    return terminales, nuevos_no_terminales, simbolo_inicial, nueva_gramatica


def imprimir_gramatica(gramatica):
    print("\n=== Gramática sin símbolos inútiles ===")
    for nt, prods in gramatica.items():
        print(f"{nt} -> {' | '.join(prods)}")

if __name__ == "__main__":
    # Programa principal
    terminales, no_terminales, simbolo_inicial, gramatica = leer_gramatica()
    terminales, no_terminales, simbolo_inicial, gramatica_util = eliminar_simbolos_inutiles(terminales, no_terminales, simbolo_inicial, gramatica)
    imprimir_gramatica(gramatica_util)
