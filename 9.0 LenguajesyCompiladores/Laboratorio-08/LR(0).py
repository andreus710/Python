
"""
Analizador Sintáctico LR para gramática 

"""
import sys
import pandas as pd
import os

# Constantes
PRO_TABLE_ENTRY = 15
PRO_PRODUCTION_STR = 40
NUM_PRODUCTIONS = 7
NUM_TABLE_ROWS = 22
NUM_TABLE_COLS = 18
TOTALPILA = 100
LONGITUD_CADENA = 200
S_BUFFER = 10

class Tabla:
    def __init__(self, archivo_excel=None):
        """
        Inicializa la tabla de análisis sintáctico.
        
        Args:
            archivo_excel (str): Ruta al archivo Excel con la tabla.
                               Si es None, usa la tabla por defecto.
        """
        if archivo_excel and os.path.exists(archivo_excel):
            self.cargar_desde_excel(archivo_excel)
        else:
            if archivo_excel:
                print(f"Advertencia: No se encontró el archivo {archivo_excel}. Usando tabla por defecto.")
            self.cargar_tabla_por_defecto()

    def cargar_desde_excel(self, archivo_excel):
        """Carga la tabla desde un archivo Excel"""
        try:
            # Leer el archivo Excel
            df = pd.read_excel(archivo_excel, header=0, index_col=0)
            
            # Inicializar matriz con espacios vacíos
            self.M = [[" " for _ in range(NUM_TABLE_COLS)] for _ in range(NUM_TABLE_ROWS)]
            
            # Obtener encabezados (primera fila)
            columnas = df.columns.tolist()
            
            # Llenar la fila de encabezados (fila 0)
            self.M[0][0] = "Estado"  # Primera columna siempre es "Estado"
            for i, col in enumerate(columnas[:NUM_TABLE_COLS-1], 1):
                self.M[0][i] = str(col) if pd.notna(col) else " "
            
            # Llenar los datos de la tabla
            for idx, (estado, fila) in enumerate(df.iterrows(), 1):
                if idx >= NUM_TABLE_ROWS:
                    break
                    
                self.M[idx][0] = str(estado)  # Estado en la primera columna
                
                for j, valor in enumerate(fila[:NUM_TABLE_COLS-1], 1):
                    if pd.notna(valor):
                        self.M[idx][j] = str(valor).strip()
                    else:
                        self.M[idx][j] = " "
            
            print(f"Tabla cargada exitosamente desde ruta")
            
        except Exception as e:
            print(f"Error al cargar el archivo Excel: {e}")
            print("Usando tabla por defecto...")
            self.cargar_tabla_por_defecto()

    def mostrar_tabla(self):
        """Muestra la tabla en formato legible"""
        print("\nTabla de Análisis Sintáctico LR:")
        print("=" * 150)
        
        # Mostrar encabezados
        print("Estado", end="")
        for j in range(1, NUM_TABLE_COLS):
            print(f"\t{self.M[0][j]}", end="")
        print()
        print("-" * 150)
        
        # Mostrar datos
        for i in range(1, NUM_TABLE_ROWS):
            print(f"{self.M[i][0]}", end="")
            for j in range(1, NUM_TABLE_COLS):
                valor = self.M[i][j] if self.M[i][j] != " " else ""
                print(f"\t{valor}", end="")
            print()

    def accion(self, xx_estado_str, ae_simbolo_entrada_str):
        col_idx = 0
        row_idx = 0
        
        # Buscar columna
        for k in range(1, NUM_TABLE_COLS):
            if self.M[0][k] == ae_simbolo_entrada_str:
                col_idx = k
                break
        
        # Buscar fila
        for k in range(1, NUM_TABLE_ROWS):
            if self.M[k][0] == xx_estado_str:
                row_idx = k
                break
        
        if col_idx == 0 or row_idx == 0:
            return " "
        
        return self.M[row_idx][col_idx]

    def ir_a(self, xx_estado_str, tira_simbolo_str):
        return self.accion(xx_estado_str, tira_simbolo_str)

class Parser:
    def __init__(self, archivo_tabla_excel=None):
        self.t = Tabla(archivo_tabla_excel)
        self.pila = []
        self.ae = ""
        self.cad = ""
        self.p = 0
        
        # Inicializar producciones
        self.produccion = [
            "S-> switch ( id ) { B } A",  # Regla 1
            "A->S",                       # Regla 2
            "A->&",                       # Regla 3
            "B->case num T : A break ;",  # Regla 4
            "B->&",                       # Regla 5
            "T->..num",                   # Regla 6
            "T->&"                        # Regla 7
        ]
        
        # Longitudes del lado derecho de las producciones
        self.produccion_rhs_len = [8, 1, 0, 7, 0, 2, 0]
        
        # Inicializar pila con estado inicial
        self.pila = ["0"]

    def empilar(self, simbolo):
        if len(self.pila) < TOTALPILA:
            self.pila.append(str(simbolo))
        else:
            print("Error: Desbordamiento de la pila!", file=sys.stderr)

    def cima_de_pila(self):
        if self.pila:
            return self.pila[-1]
        return ""

    def op(self, tira):
        if tira and len(tira) > 0:
            return tira[0]
        return ' '

    def estado(self, tira):
        if len(tira) > 1:
            return tira[1:]
        return ""

    def long_produccion(self, num_regla_str):
        try:
            regla_num = int(num_regla_str)
            if 1 <= regla_num <= NUM_PRODUCTIONS:
                return self.produccion_rhs_len[regla_num - 1]
        except ValueError:
            print(f"Error: Número de regla inválido en long_produccion: {num_regla_str}", file=sys.stderr)
        return 0

    def sacar(self, total):
        for _ in range(min(total, len(self.pila))):
            if self.pila:
                self.pila.pop()

    def ret_pila(self):
        return "".join(self.pila)

    def lado_izq(self, num_regla_str):
        try:
            regla_num = int(num_regla_str)
            if 1 <= regla_num <= NUM_PRODUCTIONS:
                return self.produccion[regla_num - 1][0]
        except ValueError:
            pass
        return ""

    def ret_cad(self):
        if self.p < len(self.cad):
            return self.cad[self.p:]
        return ""

    def mover(self, pos):
        self.p = pos

    def mostrar_produccion(self, num_regla_str):
        try:
            regla_num = int(num_regla_str)
            if 1 <= regla_num <= NUM_PRODUCTIONS:
                return self.produccion[regla_num - 1]
        except ValueError:
            pass
        return "Error: Regla no existe"

    def lexico(self):
        """Analizador léxico que devuelve el siguiente token y actualiza la posición"""
        current_scan_p = self.p
        
        # Saltar espacios en blanco
        while current_scan_p < len(self.cad) and self.cad[current_scan_p].isspace():
            current_scan_p += 1
        
        # Comprobar fin de cadena
        if current_scan_p >= len(self.cad):
            return "$", current_scan_p
        
        # Palabras clave
        keywords = ["switch", "case", "break"]
        for keyword in keywords:
            if (self.cad[current_scan_p:current_scan_p + len(keyword)] == keyword and
                (current_scan_p + len(keyword) >= len(self.cad) or 
                 not self.cad[current_scan_p + len(keyword)].isalnum())):
                return keyword, current_scan_p + len(keyword)
        
        # Operador ".."
        if self.cad[current_scan_p:current_scan_p + 2] == "..":
            return "..", current_scan_p + 2
        
        # Tokens de un solo carácter
        ch = self.cad[current_scan_p]
        single_char_ops = "(){};:$"
        if ch in single_char_ops:
            return ch, current_scan_p + 1
        
        # Números
        if ch.isdigit():
            start_pos = current_scan_p
            while current_scan_p < len(self.cad) and self.cad[current_scan_p].isdigit():
                current_scan_p += 1
            return "num", current_scan_p
        
        # Identificadores
        if ch.isalpha():
            start_pos = current_scan_p
            while (current_scan_p < len(self.cad) and 
                   (self.cad[current_scan_p].isalnum() or self.cad[current_scan_p] == '_')):
                current_scan_p += 1
            return "id", current_scan_p
        
        # Error léxico
        print(f"Error Léxico: Carácter desconocido '{ch}' en la posición {current_scan_p}", file=sys.stderr)
        return ch, current_scan_p + 1

    def leer(self):
        """Lee la cadena de entrada del usuario"""
        try:
            entrada = input("\nleer cadena: ")
            self.cad = entrada + " $"
            self.p = 0
            
            # Reiniciar la pila
            self.pila = ["0"]
            
            return self.sintactico()
        except EOFError:
            print("\nEntrada terminada.")
            return False
        except KeyboardInterrupt:
            print("\nProceso interrumpido por el usuario.")
            return False

    def sintactico(self):
        """Analizador sintáctico LR"""
        while True:
            xx = self.cima_de_pila()  # Estado actual
            
            # Obtener siguiente token
            ae_token, pos_para_mover = self.lexico()
            self.ae = ae_token
            
            # Obtener acción de la tabla
            interseccion = self.t.accion(xx, self.ae)
            
            # Mostrar estado actual
            ret_pila = self.ret_pila()
            ret_cad = self.ret_cad()
            print(f"\n{ret_pila}\t\t{ret_cad}", end="")
            
            op_char = self.op(interseccion)
            estado_o_regla_str = self.estado(interseccion)
            
            if op_char == 'd':  # Desplazar
                print(f"\tAccion: Desplazar a {estado_o_regla_str} (simbolo: {self.ae})")
                self.empilar(self.ae)
                self.empilar(estado_o_regla_str)
                self.mover(pos_para_mover)
                
            elif op_char == 'r':  # Reducir
                len_rhs = self.long_produccion(estado_o_regla_str)
                self.sacar(2 * len_rhs)
                
                xx = self.cima_de_pila()
                prod_a_mostrar = self.mostrar_produccion(estado_o_regla_str)
                lhs_simbolo = self.lado_izq(estado_o_regla_str)
                
                print(f"\tAccion: Reducir por Regla {estado_o_regla_str} ({prod_a_mostrar})")
                
                self.empilar(lhs_simbolo)
                goto_estado = self.t.ir_a(xx, lhs_simbolo)
                
                if goto_estado == " " or not goto_estado:
                    print(f"\nError Sintáctico: No hay GOTO para estado '{xx}' y símbolo '{lhs_simbolo}'")
                    return False
                
                self.empilar(goto_estado)
                
            elif interseccion == "accept":  # Aceptar
                print("\tAccion: Aceptar")
                print("\n\nCadena Aceptada!")
                return True
                
            else:  # Error
                print(f"\tAccion: Error (Celda de tabla: '{interseccion}')")
                print("\n\nError Sintáctico: Cadena Rechazada.")
                print(f"  Estado actual en pila: {xx}, Símbolo de entrada actual: '{self.ae}'")
                print(f"  Contenido de la celda M[{xx}][{self.ae}] = '{interseccion}'")
                return False
            
        
            try:
                print(" ")
            except (EOFError, KeyboardInterrupt):
                return interseccion == "accept"

def main():
    """Función principal"""
    print("Analizador Sintáctico LR para gramática ")
    print("=" * 50)
    
    # Preguntar por archivo Excel
    archivo_excel = None
    archivo_excel = "C:\\Users\\andre\\OneDrive\\Escritorio\\UNI\\Python\\Python\\9.0 LenguajesyCompiladores\\Laboratorio-08\\tabla.xlsx"

    parser = Parser(archivo_excel)
    
    while True:
        print("\nOpciones:")
        print("1. Analizar una cadena")
        print("2. Mostrar tabla de análisis")
        print("0. Salir")
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == "1":
            try:
                resultado = parser.leer()
                if resultado:
                    print("\nAnálisis completado exitosamente.")
                else:
                    print("\nAnálisis falló.")
                    
            except KeyboardInterrupt:
                print("\nAnálisis interrumpido por el usuario.")
            except Exception as e:
                print(f"\nError durante el análisis: {e}", file=sys.stderr)
        
        elif opcion == "2":
            parser.t.mostrar_tabla()
            
        elif opcion == "3":
            archivo_salida = input("Nombre del archivo de salida (por defecto: tabla_lr_exportada.xlsx): ").strip()
            if not archivo_salida:
                archivo_salida = "tabla_lr_exportada.xlsx"
            parser.t.exportar_a_excel(archivo_salida)
            
        elif opcion == "0":
            break
            
        else:
            print("Opción no válida. Por favor, seleccione 1, 2, 3 o 4.")

if __name__ == "__main__":
    main()