
def verif_valor(valor):
    """
    Verifica si el valor es un número entero o decimal.
    """
    try:
        num = float(valor)
        if (1 <= num <= 10):
            return True
        else:
            return False
    except ValueError:
        return False
    
def ver_expo(n):
    try:
        int(n)
        return True
    except ValueError:
        return False


def nota_cientif(expr):
    expr = expr.replace(" ", "")
    
    if "x10^" not in expr:
        return False

    partes = expr.split("x10^") #separa la parte base y el exponente
    if len(partes) != 2:
        return False

    a, n = partes
    return verif_valor(a) and ver_expo(n)


def main():
    while True:
        expr = input("Ingrese una expresión en notación científica (o '0' para terminar) Ejemplo: 1.23x10^4  ---------> ")
        if expr.lower() == "0":
            break
        resultado = nota_cientif(expr)
        
        print(f"\n{expr} -> {'VÁLIDA' if resultado else 'INVÁLIDA'}\n")

if __name__ == "__main__":
    main()
    
    
