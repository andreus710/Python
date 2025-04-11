# El ciclo for se utiliza para iterar sobre una secuencia (lista, tupla, diccionario, conjunto o cadena)
#El break detiene el ciclo for cuando se cumple la condicion
# y el continue salta a la siguiente iteracion del ciclo for

for n in range(2, 10):
    for x in range(2, n):
        if n % x == 0:
            print(f"{n} equals {x} * {n//x}")
            break
        
# La funcion continue se utiliza para saltar a la siguiente iteracion del ciclo for
# y no ejecuta las instrucciones restantes en el ciclo for

for num in range(2, 10):
    if num % 2 == 0:
        print(f"Found an even number {num}")
        continue
    print(f"Found an odd number {num}")