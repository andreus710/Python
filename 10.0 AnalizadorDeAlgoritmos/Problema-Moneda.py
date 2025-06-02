# Tenemos un sistema monetario con n monedas de valores v, v1 ,v2,... Hay un número ilimitado de monedas 
# de cada valor. El objetivo es devolver una cantidad M utilizando el menor número posible de monedas.

#Complejidad: Se menciona que es de complejidad lineal respecto a n (el número de monedas). 
 # Esto es porque itera una vez sobre cada tipo de moneda (for i in range(n)). 
 # El while interno podría hacer que parezca más, pero en realidad, la cantidad total de restas (contidod = cantidad monedas [i]) 
 # está limitada por la cantidad inicial M, y cada moneda se considera un número limitado de veces. Si los valores de las monedas 
 # crecen exponencialmente, esto sería muy eficiente.
 
 
monedas =[500 ,200 ,100 ,50 ,25 ,5 ,1]
def Devolver_Cambio ( cantidad , monedas ) :
    n = len( monedas )
    cambio = [0 for i in range (n) ]
    for i in range (n) :
        while monedas [i] < cantidad :
            cantidad = cantidad - monedas [i]
            cambio [i] = cambio [i] + 1
    return cambio

def main():
    cantidad = int(input("Ingrese la cantidad de dinero: "))
    cambio = Devolver_Cambio ( cantidad , monedas )
    print("El cambio es:")
    for i in range (len(monedas)):
        if cambio[i] > 0:
            print(f"{cambio[i]} monedas de {monedas[i]} centavos")
    if cantidad > 0:
        print("No se puede devolver el cambio exacto.")
    else:
        print("Cambio devuelto correctamente.")
        
if __name__ == "__main__":
    main()
    
# Contraejemplo para demostrar que el algoritmo voraz no es óptimo para un sistema monetario específico.
# monedas = [11, 5, 1]
   # P1 : [  11, 1, 1, 1, 1]
   # P2 : [  5, 5, 5]

# El algoritmo voraz no es óptimo para este sistema monetario. Este es un contraejemplo 
# que demuestra la suboptimalidad. La "demostración de suboptimalidad" consiste en presentar 
# un caso donde el algoritmo voraz no da la solución óptima. Aquí, al tomar la moneda de 11, 
# el algoritmo se "encajona" y pierde la oportunidad de usar las monedas de 5 de manera más eficiente.