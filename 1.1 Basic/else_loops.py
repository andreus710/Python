#los comentarios son para entender el funcionamiento del codigo
# este codigo demuestra el uso de la funcion range en un ciclo for
# genera una secuencia de numeros del 2 al 10 e improme los numero primos por la consola

for n in range(2, 10):
    for x in range(2, n):
        if n % x == 0:
            print(n, 'equals', x, '*', n//x)
            break
    else:
        # loop fell through without finding a factor
        print(n, 'is a prime number')