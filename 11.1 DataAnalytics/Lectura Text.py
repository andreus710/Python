



from pathlib import Path
file_path = Path(r"C:\Users\andre\OneDrive\Escritorio\ \PROGRAM\LENGUAJES\Python\Python\11.1 DataAnalytics\Práctica 1.txt")
with file_path.open("r", encoding="utf-8") as f:
    for linea in f:
        print(linea)