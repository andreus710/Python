#Introduce los terminales (separados por comas): +,*,id,(,)
#Introduce los no terminales (separados por comas): E,T,F

#Introduce las producciones:
##> E -> E + T | T
##> T -> T * F | F
##> F -> ( E ) | id
##> fin


def leer_gramatica():
    print("=== Lector de Gramática ===")
    terminales = input("Introduce los terminales (separados por comas): ").split(",")
    no_terminales = input("Introduce los no terminales (separados por comas): ").split(",")
    
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
        derechas = [d.strip() for d in derecha.strip().split("|")]

        if izquierda not in gramatica:
            gramatica[izquierda] = []
        gramatica[izquierda].extend(derechas)

    return terminales, no_terminales, gramatica

def eliminar_recursion_izquierda(no_terminal, producciones):
    directas = []
    no_directas = []

    for prod in producciones:
        if prod.startswith(no_terminal):
            directas.append(prod[len(no_terminal):].strip())
        else:
            no_directas.append(prod)

    if not directas:
        return {no_terminal: producciones}

    nuevo = no_terminal + "'"
    nuevas_prods = [p + " " + nuevo for p in no_directas]
    nuevas_recursivas = [p + " " + nuevo for p in directas] + ["ε"]

    return {
        no_terminal: nuevas_prods,
        nuevo: nuevas_recursivas
    }

def factoring_izquierda(producciones):
    from collections import defaultdict
    grupos = defaultdict(list)

    for prod in producciones:
        primer = prod.split()[0] if prod != "ε" else "ε"
        grupos[primer].append(prod)

    resultado = {}
    nuevas = []

    for clave, prods in grupos.items():
        if len(prods) == 1:
            nuevas.append(prods[0])
        else:
            nuevo = clave + "_fact"
            sufijos = [' '.join(p.split()[1:]) if len(p.split()) > 1 else "ε" for p in prods]
            resultado[nuevo] = sufijos
            nuevas.append(clave + " " + nuevo)

    return nuevas, resultado

def desambiguar_gramatica(gramatica):
    nueva_gramatica = {}

    for no_terminal, producciones in gramatica.items():
        print(f"\nProcesando {no_terminal}: {producciones}")

        if any(p.startswith(no_terminal) for p in producciones):
            print(f"-> Eliminando recursión izquierda en {no_terminal}")
            eliminadas = eliminar_recursion_izquierda(no_terminal, producciones)
            nueva_gramatica.update(eliminadas)
        else:
            nuevas, factorizadas = factoring_izquierda(producciones)
            nueva_gramatica[no_terminal] = nuevas
            nueva_gramatica.update(factorizadas)

    return nueva_gramatica

def imprimir_gramatica(gramatica):
    print("\n=== Gramática resultante ===")
    for no_terminal, producciones in gramatica.items():
        print(f"{no_terminal} -> {' | '.join(producciones)}")

if __name__ == "__main__":
    # Programa principal
    terminales, no_terminales, gramatica = leer_gramatica()
    gramatica_sin_ambiguedad = desambiguar_gramatica(gramatica)
    imprimir_gramatica(gramatica_sin_ambiguedad)
