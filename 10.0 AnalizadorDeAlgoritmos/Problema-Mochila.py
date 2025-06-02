peso = [10 , 20, 30, 40, 50 ] # Pesos de los objetos
beneficio = [60 , 100, 120 , 80 , 30] # Beneficios de los objetos

def Mochila(peso, beneficio, M):
    n = len(peso)
    solucion = [0.0 for i in range(n)] # Para almacenar la proporción de cada objeto
    peso_actual = 0.0

    # Paso 1: Calcular la relación beneficio/peso para cada objeto
    # y almacenar tuplas (b/p, peso, beneficio, índice original)
    objetos = []
    for i in range(n):
        objetos.append((beneficio[i] / peso[i], peso[i], beneficio[i], i))

    # Paso 2: Ordenar los objetos por la relación beneficio/peso en orden decreciente
    objetos.sort(key=lambda x: x[0], reverse=True)

    # Paso 3: Iterar sobre los objetos y añadirlos a la mochila
    for relacion_bp, p, b, original_idx in objetos:
        if peso_actual + p <= M: # Si el objeto completo cabe
            solucion[original_idx] = 1.0 # Tomamos el 100% del objeto
            peso_actual += p
        else: # Si el objeto no cabe completamente, tomamos una fracción
            espacio_restante = M - peso_actual
            solucion[original_idx] = espacio_restante / p # Tomamos la fracción que cabe
            peso_actual = M # La mochila está llena
            break # Salimos del bucle, no hay más espacio

    return solucion # Devuelve las proporciones x_i de cada objeto


if __name__ == "__main__":
    M = int(input("Ingrese la capacidad máxima de la mochila: "))
    solucion = Mochila(peso, beneficio, M)
    
    print("Proporciones de objetos en la mochila:")
    for i in range(len(solucion)):
        if solucion[i] > 0:
            print(f"Objeto {i+1}: {solucion[i]*100:.2f}%")
    
    total_beneficio = sum(solucion[i] * beneficio[i] for i in range(len(solucion)))
    print(f"Beneficio total obtenido: {total_beneficio:.2f}")