
"""
Analizador Sintáctico LR para gramática 

"""
import sys
import pandas as pd
import os

# Constantes
PRO_TABLE_ENTRY = 15
PRO_PRODUCTION_STR = 40
NUM_PRODUCTIONS = 142
NUM_TABLE_ROWS = 239
NUM_TABLE_COLS = 126
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
        
        # Inicializar producciones con la gramática completa (λ reemplazado por &)
        self.produccion = [
            "S' → S",
            "S → A B",
            "B → C B id D { E }",
            "C → F",
            "C → &",
            "F → private",
            "F → public",
            "F → protected",
            "D → extiende id",
            "D → &",
            "E → A G A H A",
            "G → I id ( K ) { H }",
            "H → J H",
            "H → &",
            "J → V",
            "J → AD",
            "J → AI",
            "J → AK",
            "J → AO",
            "J → BG",
            "J → A",
            "I → L",
            "I → &",
            "L → private M",
            "L → public M",
            "L → protected M",
            "L → static M",
            "L → final M",
            "M → static N",
            "M → final",
            "M → &",
            "N → final",
            "N → &",
            "K → O",
            "K → &",
            "O → P Q",
            "Q → , P Q",
            "Q → &",
            "P → R id",
            "R → T",
            "R → U",
            "U → T [ ]",
            "T → int",
            "T → string",
            "T → float",
            "T → bool",
            "T → double",
            "T → short",
            "T → id",
            "V → I X;",
            "X → T Y",
            "X → U id Z",
            "Y → id AA AB",
            "AB → , id AA AB",
            "AB → &",
            "AA → ← AC",
            "AA → &",
            "Z → ← new T [ num ]",
            "Z → ← id",
            "Z → &",
            "AC → id",
            "AC → num",
            "AC → \" id \"", # Aquí " id " es un token literal, lo cuento como 1
            "AD → I AE id ( K ) { H AF }",
            "AE → void",
            "AE → T",
            "AE → U",
            "AF → AG",
            "AF → &",
            "AG → retorna AH ;",
            "AH → id",
            "AH → num",
            "AH → &",
            "AI → I id id AJ;",
            "AJ → ← new id ( AL)",
            "AJ → ← id",
            "AJ → &",
            "AK → id . id ( AL ) ;",
            "AL → AM",
            "AL → &",
            "AM → id AN",
            "AN → , id AN",
            "AN → &",
            "AO → ES",
            "AO → EP",
            "AO → EM",
            "AO → EH",
            "AO → EU",
            "AO → break ;",
            "ES → Si ( AP ) { H } AQ AR",
            "AQ → SinoSi ( AP ) { H } AQ",
            "AQ → &",
            "AR → Sino { H }",
            "AR → &",
            "EP → Para ( AS ; AP ; AT) { H }",
            "AS → T id = num",
            "AS → id = num",
            "AT → id ++",
            "AT → id --",
            "AT → id += num",
            "AT → id -= num",
            "EM → Mientras ( AP ) { H }",
            "EH → Hacer { H } Mientras ( AP ) ;",
            "EU → Según ( AU) { AV AZ }",
            "AU → id",
            "AU → num",
            "AV → AW AV",
            "AV → &",
            "AW → caso AX : AY",
            "AX → num",
            "AX → id",
            "AY → J AY",
            "AY → &",
            "AZ → defecto : AY",
            "AZ → &",
            "AP → BA",
            "BA → BB BC",
            "BC → BD BB BC",
            "BC → &",
            "BD → &&",
            "BD → ||",
            "BB → BE BF BE",
            "BF → ==",
            "BF → !=",
            "BF → <",
            "BF → <=",
            "BF → >",
            "BF → >=",
            "BE → id",
            "BE → num",
            "BG → id BH ;",
            "BH → = BI",
            "BH → = id BJ num",
            "BI → id",
            "BI → num",
            "BJ → +",
            "BJ → -",
            "BJ → *",
            "BJ → /",
            "A → // texto A",   # Ajustado aquí
            "A → *** texto *** A", # Ajustado aquí
            "A → &"
        ]
        
        # Longitudes del lado derecho (RHS) de las producciones
        # Calculado contando los símbolos a la derecha de '→' o '&'
        self.produccion_rhs_len = [
            1, # S' → S
            2, # S → A B
            7, # B → C B id D { E }
            1, # C → F
            0, # C → & (epsilon)
            1, # F → private
            1, # F → public
            1, # F → protected
            2, # D → extiende id
            0, # D → & (epsilon)
            5, # E → A G A H A
            7, # G → I id ( K ) { H }
            2, # H → J H
            0, # H → & (epsilon)
            1, # J → V
            1, # J → AD
            1, # J → AI
            1, # J → AK
            1, # J → AO
            1, # J → BG
            1, # J → A
            1, # I → L
            0, # I → & (epsilon)
            2, # L → private M
            2, # L → public M
            2, # L → protected M
            2, # L → static M
            2, # L → final M
            2, # M → static N
            1, # M → final
            0, # M → & (epsilon)
            1, # N → final
            0, # N → & (epsilon)
            1, # K → O
            0, # K → & (epsilon)
            2, # O → P Q
            3, # Q → , P Q
            0, # Q → & (epsilon)
            2, # P → R id
            1, # R → T
            1, # R → U
            3, # U → T [ ]
            1, # T → int
            1, # T → string
            1, # T → float
            1, # T → bool
            1, # T → double
            1, # T → short
            1, # T → id
            3, # V → I X;
            2, # X → T Y
            3, # X → U id Z
            3, # Y → id AA AB
            4, # AB → , id AA AB
            0, # AB → & (epsilon)
            2, # AA → ← AC
            0, # AA → & (epsilon)
            5, # Z → ← new T [ num ]
            3, # Z → ← id
            0, # Z → & (epsilon)
            1, # AC → id
            1, # AC → num
            1, # AC → " id " (Si " id " es un único token literal en su léxico)
            8, # AD → I AE id ( K ) { H AF }
            1, # AE → void
            1, # AE → T
            1, # AE → U
            1, # AF → AG
            0, # AF → & (epsilon)
            3, # AG → retorna AH ;
            1, # AH → id
            1, # AH → num
            0, # AH → & (epsilon)
            5, # AI → I id id AJ;
            4, # AJ → ← new id ( AL)
            2, # AJ → ← id
            0, # AJ → & (epsilon)
            6, # AK → id . id ( AL ) ;
            1, # AL → AM
            0, # AL → & (epsilon)
            2, # AM → id AN
            4, # AN → , id AN
            0, # AN → & (epsilon)
            1, # AO → ES
            1, # AO → EP
            1, # AO → EM
            1, # AO → EH
            1, # AO → EU
            2, # AO → break ;
            8, # ES → Si ( AP ) { H } AQ AR
            7, # AQ → SinoSi ( AP ) { H } AQ
            0, # AQ → & (epsilon)
            3, # AR → Sino { H }
            0, # AR → & (epsilon)
            7, # EP → Para ( AS ; AP ; AT) { H }
            4, # AS → T id = num
            3, # AS → id = num
            2, # AT → id ++
            2, # AT → id --
            3, # AT → id += num
            3, # AT → id -= num
            5, # EM → Mientras ( AP ) { H }
            7, # EH → Hacer { H } Mientras ( AP ) ;
            6, # EU → Según ( AU) { AV AZ }
            1, # AU → id
            1, # AU → num
            2, # AV → AW AV
            0, # AV → & (epsilon)
            4, # AW → caso AX : AY
            1, # AX → num
            1, # AX → id
            2, # AY → J AY
            0, # AY → & (epsilon)
            3, # AZ → defecto : AY
            0, # AZ → & (epsilon)
            1, # AP → BA
            2, # BA → BB BC
            3, # BC → BD BB BC
            0, # BC → & (epsilon)
            1, # BD → &&
            1, # BD → ||
            3, # BB → BE BF BE
            1, # BF → ==
            1, # BF → !=
            1, # BF → <
            1, # BF → <=
            1, # BF → >
            1, # BF → >=
            1, # BE → id
            1, # BE → num
            3, # BG → id BH ;
            2, # BH → = BI
            4, # BH → = id BJ num
            1, # BI → id
            1, # BI → num
            1, # BJ → +
            1, # BJ → -
            1, # BJ → *
            1, # BJ → /
            2, # A → // texto A (considerando "// texto" como 1 token y "A" como otro)
            2, # A → *** texto *** A (considerando "*** texto ***" como 1 token y "A" como otro)
            0  # A → & (epsilon)
        ]
        
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
        """Analizador léxico que devuelve el siguiente token y actualiza la posición."""
        current_scan_p = self.p
        
        # Saltar espacios en blanco
        while current_scan_p < len(self.cad) and self.cad[current_scan_p].isspace():
            current_scan_p += 1
        
        # Actualizar la posición de inicio para el siguiente escaneo
        self.p = current_scan_p

        # Comprobar fin de cadena
        if self.p >= len(self.cad):
            return "$", self.p

        # --- Manejo de comentarios ---
        # Comentario de una línea "//"
        if self.cad[self.p:self.p + 2] == "//":
            end_of_line = self.cad.find('\n', self.p + 2)
            if end_of_line == -1: # Comentario hasta el final de la cadena
                self.p = len(self.cad)
                return "// texto", self.p # Asumimos "// texto" es un solo token literal para la gramática
            else:
                self.p = end_of_line
                return "// texto", self.p # Asumimos "// texto" es un solo token literal
        
        # Comentario multi-línea "***"
        if self.cad[self.p:self.p + 3] == "***":
            end_comment = self.cad.find('***', self.p + 3)
            if end_comment == -1:
                # Esto es un error si el comentario no cierra
                print(f"Error Léxico: Comentario de bloque sin cerrar en la posición {self.p}", file=sys.stderr)
                self.p = len(self.cad)
                return "ERROR", self.p
            else:
                self.p = end_comment + 3
                return "*** texto ***", self.p # Asumimos "*** texto ***" es un solo token literal

        # --- Palabras clave ---
        # Ordenar por longitud descendente para evitar coincidencias parciales (ej. "int" antes que "id")
        keywords = [
            "switch", "case", "break", "extends", "private", "public", "protected",
            "static", "final", "void", "retorna", "Si", "SinoSi", "Sino", "Para",
            "Mientras", "Hacer", "Según", "caso", "defecto", "int", "string",
            "float", "bool", "double", "short"
        ]
        # Para evitar problemas con 'id' que empieza igual que una keyword (ej. 'int')
        keywords.sort(key=len, reverse=True) 

        for keyword in keywords:
            if (self.cad[self.p : self.p + len(keyword)] == keyword and
                (self.p + len(keyword) >= len(self.cad) or 
                 not self.cad[self.p + len(keyword)].isalnum() and self.cad[self.p + len(keyword)] != '_')):
                self.p += len(keyword)
                return keyword, self.p
        
        # --- Operadores de múltiples caracteres y símbolos especiales ---
        multi_char_tokens = [
            "..", "==", "!=", "<=", ">=", "++", "--", "+=", "-=", "&&", "||", "<<" # Agregué "<<" por si acaso, no vi "<<" explícito en tu gramática
        ]
        multi_char_tokens.sort(key=len, reverse=True) # Ordenar por longitud descendente

        for token in multi_char_tokens:
            if self.cad[self.p : self.p + len(token)] == token:
                self.p += len(token)
                return token, self.p

        # --- Tokens de un solo carácter ---
        # Asegúrate de que $ sea manejado al inicio y no aquí si es un marcador de EOF
        single_char_tokens = "(){}[];,.:=+-*/" # Eliminé '$' ya que se maneja al inicio
        
        ch = self.cad[self.p]
        if ch in single_char_tokens:
            self.p += 1
            return ch, self.p
        
        # --- Operador '←' (flecha izquierda) ---
        if ch == '←':
            self.p += 1
            return '←', self.p

        # --- Literais de cadena (ej. " id ") ---
        if ch == '"':
            start_quote = self.p
            end_quote = self.cad.find('"', start_quote + 1)
            if end_quote == -1:
                print(f"Error Léxico: Literal de cadena sin cerrar en la posición {start_quote}", file=sys.stderr)
                return "ERROR", start_quote + 1
            
            # Asumimos que el contenido dentro de las comillas es parte del token " id "
            # Si " id " es un token específico, se retorna como tal.
            # De lo contrario, se podría retornar como "STRING_LITERAL" y el valor.
            # Para tu gramática, 'AC → " id "' sugiere que es un token específico.
            if self.cad[start_quote : end_quote + 1] == '" id "':
                self.p = end_quote + 1
                return '" id "', self.p
            else:
                # Si no es exactamente " id ", podríamos manejarlo como un literal de cadena genérico
                print(f"Advertencia: Literal de cadena no reconocido: '{self.cad[start_quote : end_quote + 1]}'", file=sys.stderr)
                self.p = end_quote + 1
                return "STRING_LITERAL", self.p # O un token genérico para cualquier string literal


        # --- Números ---
        if ch.isdigit():
            start_pos = self.p
            while self.p < len(self.cad) and self.cad[self.p].isdigit():
                self.p += 1
            return "num", self.p
        
        # --- Identificadores ---
        # Debe ir después de las palabras clave para que las keywords tengan prioridad
        if ch.isalpha() or ch == '_': # Los identificadores pueden empezar con letra o '_'
            start_pos = self.p
            while (self.p < len(self.cad) and 
                   (self.cad[self.p].isalnum() or self.cad[self.p] == '_')):
                self.p += 1
            # Aquí es crucial asegurarse de que no se haya emparejado una palabra clave
            # ya que las keywords se verificaron antes.
            return "id", self.p
        
        # --- Error léxico ---
        print(f"Error Léxico: Carácter desconocido '{ch}' en la posición {self.p}", file=sys.stderr)
        self.p += 1 # Avanza para evitar bucle infinito en caso de error
        return "ERROR", self.p

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
    archivo_excel = "C:\\Users\\andre\\OneDrive\\Escritorio\\UNI\\Python\\Python\\9.0 LenguajesyCompiladores\\Proyecto\\proyecto.xlsx"

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