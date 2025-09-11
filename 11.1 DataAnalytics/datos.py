#LEER TODAS LAS LINEAS EN UNA LISTA


from pathlib import Path

file_path = Path("C:\\Users\\andre\\OneDrive\\Escritorio\\PROGRAM\\LENGUAJES\\Python\\Python\\11.1 DataAnalytics\\Práctica 1.txt")

# Añadir "setiembre 2026" como nueva línea al final del archivo
nuevo_texto = "setiembre 2026"

with open(file_path, "a", encoding="utf-8") as f:
    f.write("\n" + nuevo_texto)

# Imprimir solo lo agregado
print(nuevo_texto)
