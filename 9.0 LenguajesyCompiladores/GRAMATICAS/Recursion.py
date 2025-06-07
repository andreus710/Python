#Introduce los terminales (separados por comas): id,+,*
#Introduce los no terminales (separados por comas): E,T

#> E -> E + T | T
#> T -> T * id | id
#> fin

def leer_gramatica():
    print("=== Lector de Gramática ===")
    terminales = input("Introduce los terminales (separados por comas): ").replace(" ", "").split(",")
    no_terminales = input("Introduce los no terminales (separados por comas): ").replace(" ", "").split(",")
    
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

    return terminales, no_terminales, gramatica

def eliminar_recursion_izquierda_directa(A, producciones):
    """Elimina la recursión izquierda directa de un no terminal."""
    alpha = []
    beta = []
    for prod in producciones:
        if prod.startswith(A):
            alpha.append(prod[len(A):].strip())
        else:
            beta.append(prod.strip())

    if not alpha:
        return {A: producciones}

    A_prime = A + "'"
    nuevas_A = [b + " " + A_prime for b in beta]
    nuevas_A_prime = [a + " " + A_prime for a in alpha] + ["ε"]
    return {
        A: nuevas_A,
        A_prime: nuevas_A_prime
    }

def eliminar_recursion_indirecta(no_terminales, gramatica):
    """Elimina la recursión izquierda indirecta."""
    nueva_gramatica = dict(gramatica)

    for i in range(len(no_terminales)):
        Ai = no_terminales[i]
        for j in range(i):
            Aj = no_terminales[j]
            nuevas_prods = []
            for prod in nueva_gramatica[Ai]:
                if prod.startswith(Aj):
                    for gamma in nueva_gramatica[Aj]:
                        nuevas_prods.append(gamma + " " + " ".join(prod.split()[1:]))
                else:
                    nuevas_prods.append(prod)
            nueva_gramatica[Ai] = nuevas_prods

        # Eliminar recursión izquierda directa de Ai
        resultado = eliminar_recursion_izquierda_directa(Ai, nueva_gramatica[Ai])
        nueva_gramatica.update(resultado)

    return nueva_gramatica

def imprimir_gramatica(gramatica):
    print("\n=== Gramática sin recursión ===")
    for no_terminal, producciones in gramatica.items():
        print(f"{no_terminal} -> {' | '.join(producciones)}")

if __name__ == "__main__":
    # Leer la gramática desde la entrada del usuario
    terminales, no_terminales, gramatica = leer_gramatica()
    gramatica_sin_recursion = eliminar_recursion_indirecta(no_terminales, gramatica)
    imprimir_gramatica(gramatica_sin_recursion)
