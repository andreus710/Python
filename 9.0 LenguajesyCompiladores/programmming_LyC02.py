""" Grupo 7:
Cordero Alfaro Renzo Pedro
Macchiavello Perez Giuliano
Morales Usca Andres Fernando
"""

def es_entero(token):
    return token.isdigit()

def es_real(token):
    partes = token.split(".")
    return len(partes) == 2 and partes[0].isdigit() and partes[1].isdigit()

def es_credito(token):
    if token.startswith("CRE") and token[3:].isdigit():
        valor = int(token[3:])
        return 0 < valor < 60
    return False

def es_numero_octal(token):
    return token.endswith("o0") and token[:-2].isdigit()

def analizar_entrada(entrada):
    tokens = entrada.split()
    for token in tokens:
        if es_credito(token):
            print(f"{token} crédito")
        elif token.startswith("CRE") and not es_credito(token):
            print(f"{token} error")
        elif es_real(token):
            print(f"{token} constante real")
        elif es_entero(token):
            print(f"{token} Constante entera")
        elif es_numero_octal(token):
            print(f"{token} Numero octal")
        else:
            print(f"{token} error")

def main():
    value = 1
    while(value != 0):
        entrada = input("Ingrese la cadena ( end para terminar): ")
        if entrada == "end":
            value = 0
        else:
            analizar_entrada(entrada)


if __name__ == "__main__":
    main()
