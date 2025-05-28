class Tabla:
    def __init__(tabla):
        tabla.M = [[" " for _ in range(7)] for _ in range(6)]
        tabla.produccion = ""

        tabla.M[0][1] = "i"
        tabla.M[0][2] = "+"
        tabla.M[0][3] = "*"
        tabla.M[0][4] = "("
        tabla.M[0][5] = ")"
        tabla.M[0][6] = "$"

        tabla.M[1][0] = "E"
        tabla.M[1][1] = "RT"
        tabla.M[1][4] = "RT"

        tabla.M[2][0] = "R"
        tabla.M[2][2] = "+RT"
        tabla.M[2][5] = "&"
        tabla.M[2][6] = "&"

        tabla.M[3][0] = "T"
        tabla.M[3][1] = "GF"
        tabla.M[3][4] = "GF"

        tabla.M[4][0] = "G"
        tabla.M[4][2] = "&"
        tabla.M[4][3] = "*GF"
        tabla.M[4][5] = "&"
        tabla.M[4][6] = "&"

        tabla.M[5][0] = "F"
        tabla.M[5][1] = "i"
        tabla.M[5][4] = "(E)"

    def terminal(tabla, car):
        return car in tabla.M[0][1:]

    def ret_produccion(tabla):
        return tabla.produccion

    def existe_interseccion(tabla, XX, ae):
        x = y = 0
        for i in range(1, 7):
            if tabla.M[0][i] == ae:
                x = i
        for i in range(1, 6):
            if tabla.M[i][0] == XX:
                y = i
        if x == 0 or y == 0 or tabla.M[y][x] == " ":
            return False
        tabla.produccion = tabla.M[y][x]
        return True


def lexico(cad, p):
    while p < len(cad) and cad[p] == ' ':
        p += 1
    if p >= len(cad):
        return "", p

    c = cad[p]
    pos = p + 1

    if c.isalpha():
        return "i", pos
    elif c in ['+', '*', '(', ')', '$']:
        return c, pos
    else:
        return "", pos


def empilar(pila, i, produccion):
    for simbolo in reversed(produccion):
        pila.append(simbolo)
        i += 1
    return pila, i


def ret_pila(pila, i):
    return ''.join(pila[:i])


def ret_cad(cad, p):
    return cad[p:]


def error():
    print("Error de sintaxis")
    exit(0)


def sintactico(cad, tabla):
    pila = ["$", "E"]
    i = 2
    p = 0

    while True:
        ae, pos = lexico(cad, p)
        XX = pila[i - 1]

        if XX == "$":
            break

        if tabla.terminal(XX):
            if XX == ae:
                i -= 1
                p = pos
            else:
                print("1")
                error()
        else:
            if tabla.existe_interseccion(XX, ae):
                produccion = tabla.ret_produccion()
                print(f"| {ret_pila(pila, i)} | {ret_cad(cad, p)} | {XX} --> {produccion}")
                i -= 1
                if produccion != "&":
                    pila, i = empilar(pila, i, produccion)
            else:
                print("2")
                error()

    print("\nAnálisis correcto")


def lectura():
    cad = input("LEER CADENA: ") + " $"
    tabla = Tabla()
    sintactico(cad, tabla)


if __name__ == "__main__":
    lectura()
