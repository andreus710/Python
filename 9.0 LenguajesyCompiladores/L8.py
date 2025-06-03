import sys

# Tabla class with updated parsing table data
class Tabla:
    def __init__(self):
        self.M = [[" " for _ in range(18)] for _ in range(22)]

        # Header Row: Terminals and Non-Terminals
        self.M[0][1] = "switch"
        self.M[0][2] = "case"
        self.M[0][3] = "break"
        self.M[0][4] = "("
        self.M[0][5] = ")"
        self.M[0][6] = "{"
        self.M[0][7] = "}"
        self.M[0][8] = ".."
        self.M[0][9] = ";"
        self.M[0][10] = ":"
        self.M[0][11] = "id"
        self.M[0][12] = "num"
        self.M[0][13] = "$"
        self.M[0][14] = "S"  # Non-terminal
        self.M[0][15] = "A"  # Non-terminal
        self.M[0][16] = "B"  # Non-terminal
        self.M[0][17] = "T"  # Non-terminal

        # State 0
        self.M[1][0] = "0"
        self.M[1][1] = "d2"    # switch
        # GOTO
        self.M[1][14] = "1"   # S

        # State 1
        self.M[2][0] = "1"
        self.M[2][13] = "accept" # $ (accept)

        # State 2
        self.M[3][0] = "2"
        self.M[3][4] = "d3"    # (

        # State 3
        self.M[4][0] = "3"
        self.M[4][11] = "d4"   # id

        # State 4
        self.M[5][0] = "4"
        self.M[5][5] = "d5"    # )

        # State 5
        self.M[6][0] = "5"
        self.M[6][6] = "d6"    # {

        # State 6
        self.M[7][0] = "6"
        self.M[7][2] = "d11"   # case
        self.M[7][7] = "r5"    # } (Reduce B -> &)
        # GOTO
        self.M[7][16] = "7"   # B

        # State 7
        self.M[8][0] = "7"
        self.M[8][7] = "d8"    # }

        # State 8
        self.M[9][0] = "8"
        self.M[9][1] = "d2"    # switch
        self.M[9][13] = "r3"   # $ (Reduce A -> &)
        # GOTO
        self.M[9][14] = "9"   # S (This is GOTO(8,S) = 9)
        self.M[9][15] = "10"  # A (This is GOTO(8,A) = 10)

        # State 9
        self.M[10][0] = "9"
        self.M[10][13] = "r2"   # $ (Reduce A -> S)

        # State 10
        self.M[11][0] = "10"
        # This state seems to be the end of S -> switch(id){B}A
        # The action for $ should be r1 (S -> switch(id){B}A)
        self.M[11][13] = "r1"   # $ (Reduce S -> ...)

        # State 11
        self.M[12][0] = "11"
        self.M[12][12] = "d12"  # num

        # State 12
        self.M[13][0] = "12"
        self.M[13][8] = "d19"   # ..
        self.M[13][10] = "r7"  # : (Reduce T -> &)
        # GOTO
        self.M[13][17] = "13"  # T

        # State 13
        self.M[14][0] = "13"
        self.M[14][10] = "d14"  # :

        # State 14
        self.M[15][0] = "14"
        self.M[15][1] = "d2"    # switch
        self.M[15][13] = "r3"   # $ (Reduce A -> &)
        # GOTO
        self.M[15][14] = "9"   # S (GOTO(14,S) = 9) -> this seems odd, check table logic
                               # More likely GOTO(14,S) = some other state, like '15' for A.
                               # Let's assume GOTO(14,A) = 15 based on typical parsing
        self.M[15][15] = "15"  # A

        # State 15
        self.M[16][0] = "15"
        self.M[16][3] = "d16"   # break

        # State 16
        self.M[17][0] = "16"
        self.M[17][9] = "d17"   # ;

        # State 17
        self.M[18][0] = "17"
        self.M[18][2] = "d11"   # case
        self.M[18][7] = "r5"    # } (Reduce B -> &)
        # GOTO
        # This is after a "break;", so it's GOTO on B for more cases
        self.M[18][16] = "18"  # B (GOTO(17,B) = 18)

        # State 18 - after B -> case num T:A break; B (this B is the recursive one)
        # On '}' this should reduce by B -> case ...
        self.M[19][0] = "18"
        self.M[19][7] = "r4"    # } (Reduce B -> case num T:A break; B)

        # State 19
        self.M[20][0] = "19"
        self.M[20][12] = "d20"  # num (for T -> ..num)

        # State 20
        self.M[21][0] = "20"
        self.M[21][10] = "r6"   # : (Reduce T -> ..num)

        self.M[1][2] = "d11" # case
        self.M[1][3] = "r3"  # break
        self.M[1][7] = "r5"  # }
        self.M[1][8] = "d19" # .. (d19 points to state 19 for T -> .. num)
        self.M[1][10] = "r7" # :
        self.M[1][13] = "r3" # $

        # For M[9][0] == "8"
        # user provided: self.M[9][1] == "d2" ,self.M[9][3] == "r3" ,self.M[9][13] == "r3", self.M[9][14] == "9" , self.M[9][15] == "10"
        self.M[9][3] = "r3" # break; was missing

        # For M[15][0] == "14"
        # user provided: self.M[15][1] == "d2" ,self.M[15][3] == "r3" ,self.M[15][13] == "r3", self.M[15][14] == "9", self.M[15][15] == "15"
        self.M[15][3] = "r3" # break; was missing

    def accion(self, xx_estado_str, ae_simbolo_entrada_str):
        col_idx = 0
        # Max column index is 17 for symbols
        for i in range(1, 18):
            if self.M[0][i] == ae_simbolo_entrada_str:
                col_idx = i
                break
        
        row_idx = 0
        # Max row index is 21 for states 0-20
        for i in range(1, 22):
            if self.M[i][0] == xx_estado_str:
                row_idx = i
                break
        
        if col_idx == 0 or row_idx == 0:
            # print(f"Debug: Symbol or State not found in table. State='{xx_estado_str}', Symbol='{ae_simbolo_entrada_str}'")
            return " "
        else:
            return self.M[row_idx][col_idx]

    def ir_a(self, xx_estado_str, tira_simbolo_str):
        return self.accion(xx_estado_str, tira_simbolo_str)

class Parser:
    def __init__(self):
        self.t = Tabla()
        self.pila = []
        self.ae = ""
        self.cad = ""
        self.p = 0 # Pointer for input string

        self.produccion = [
            "S→switch(id){B}A",   # Rule 1 (index 0)
            "A→S",                 # Rule 2 (index 1)
            "A→&",                 # Rule 3 (index 2) (Epsilon)
            "B→case num T:A break;",# Rule 4 (index 3)
            "B→&",                 # Rule 5 (index 4) (Epsilon)
            "T→..num",             # Rule 6 (index 5)
            "T→&"                  # Rule 7 (index 6) (Epsilon)
        ]
        
        self.produccion_rhs_len = [
            8,  # S → switch ( id ) { B } A  (8 symbols)
            1,  # A → S                     (1 symbol)
            0,  # A → &                     (0 symbols)
            7,  # B → case num T : A break ; (7 symbols)
            0,  # B → &                     (0 symbols)
            2,  # T → .. num                (2 symbols)
            0   # T → &                     (0 symbols)
        ]
        self.empilar("0") # Initial state

    def empilar(self, simbolo):
        self.pila.append(simbolo)

    def cima_de_pila(self):
        if not self.pila: return ""
        return self.pila[-1]

    def op(self, tira):
        if not tira: return ""
        return tira[0]

    def estado(self, tira):
        if len(tira) > 1: return tira[1:]
        return ""

    def long_produccion(self, num_regla_str):
        rule_index = int(num_regla_str) - 1
        if 0 <= rule_index < len(self.produccion_rhs_len):
            return self.produccion_rhs_len[rule_index]
        return 0 # Should not happen

    def sacar(self, total):
        for _ in range(total):
            if self.pila: self.pila.pop()

    def ret_pila(self):
        return "".join(self.pila)

    def lado_izq(self, num_regla_str):
        rule_index = int(num_regla_str) - 1
        # Production is like "S→...", LHS is the first char "S"
        return self.produccion[rule_index][0]

    def ret_cad(self):
        if self.p < len(self.cad):
            return self.cad[self.p:]
        return ""

    def mostrar_produccion(self, num_regla_str):
        rule_index = int(num_regla_str) - 1
        return self.produccion[rule_index]

    def leer(self):
        try:
            self.cad = input("\nleer cadena: ")
        except EOFError:
            print("No input provided. Exiting.")
            return
            
        self.cad = self.cad.strip() + " $"
        self.p = 0
        # Reset stack for new input, keep initial state 0
        self.pila = ["0"]
        self.sintactico()

    def lexico(self):
        # Skip leading spaces
        while self.p < len(self.cad) and self.cad[self.p].isspace():
            self.p += 1

        if self.p >= len(self.cad):
            return "$"

        # Check for multi-character tokens first
        # Keywords
        keywords = ["switch", "case", "break"]
        for kw in keywords:
            if self.cad.startswith(kw, self.p):
                # Check for word boundary if it's an alphanumeric keyword
                if self.p + len(kw) == len(self.cad) or not self.cad[self.p + len(kw)].isalnum():
                    self.p += len(kw)
                    return kw
        
        # Two-character operator
        if self.cad.startswith("..", self.p):
            self.p += 2
            return ".."

        # Single character operators/delimiters
        single_char_tokens = ['(', ')', '{', '}', ';', ':', '$']
        char = self.cad[self.p]
        if char in single_char_tokens:
            self.p += 1
            return char

        # Numbers (num)
        if char.isdigit():
            start_num = self.p
            while self.p < len(self.cad) and self.cad[self.p].isdigit():
                self.p += 1
            # No need to return the actual number, just the token "num"
            return "num" 

        # Identifiers (id)
        if char.isalpha():
            start_id = self.p
            while self.p < len(self.cad) and (self.cad[self.p].isalnum() or self.cad[self.p] == '_'):
                self.p += 1
            # No need to return the actual identifier, just the token "id"
            return "id"
        
        # If no token is matched, it's an error or unknown character
        print(f"Error Lexico: Caracter desconocido '{self.cad[self.p]}' en posicion {self.p}")
        self.p += 1 # Skip to avoid infinite loop
        return "LEXICAL_ERROR"


    def sintactico(self):
        while True:
            xx = self.cima_de_pila()
            # Store current position in case lexico fails or to backtrack if needed for error reporting.
            pos_before_lexico = self.p 
            self.ae = self.lexico()
            
            if self.ae == "LEXICAL_ERROR":
                print("\nAnalisis abortado debido a error lexico.")
                return 0

            interseccion = self.t.accion(xx, self.ae)
            
            sys.stdout.write(f"\n{self.ret_pila():<40}{self.ret_cad():<40}")
            sys.stdout.flush()

            operacion = self.op(interseccion)
            estado_o_regla = self.estado(interseccion)

            if operacion == 'd': # Desplazar (Shift)
                sys.stdout.write(f"Accion: Desplazar a {estado_o_regla} (simbolo: {self.ae})")
                sys.stdout.flush()
                self.empilar(self.ae)
                self.empilar(estado_o_regla)
            elif operacion == 'r': # Reducir (Reduce)
                num_simbolos_rhs = self.long_produccion(estado_o_regla)
                
                # Pop 2*|beta| symbols (symbol + state for each) from stack
                # The actual symbols are not used from stack for reduction decision, only states
                self.sacar(2 * num_simbolos_rhs) 
                
                xx_despues_sacar = self.cima_de_pila()
                lhs_produccion = self.lado_izq(estado_o_regla)
                
                sys.stdout.write(f"Accion: Reducir por Regla {estado_o_regla} ({self.mostrar_produccion(estado_o_regla)})")
                sys.stdout.flush()
                
                self.empilar(lhs_produccion) # Push LHS of production
                goto_estado = self.t.ir_a(xx_despues_sacar, lhs_produccion)
                if goto_estado == " ": # Error in GOTO
                    print(f"\nError Sintactico: No hay GOTO para estado {xx_despues_sacar} y simbolo {lhs_produccion}")
                    return 0
                self.empilar(goto_estado) # Push new state from GOTO
            elif interseccion == "accept": # Note: your table uses "accept"
                sys.stdout.write("Accion: Aceptar")
                sys.stdout.flush()
                print("\n\nCadena Aceptada!")
                return 1
            else: # Error
                sys.stdout.write(f"Accion: Error (Celda vacia o invalida: '{interseccion}')")
                sys.stdout.flush()
                print(f"\n\nError Sintactico: Cadena Rechazada.")
                print(f"  Estado actual: {xx}, Simbolo de entrada: '{self.ae}' (leido desde pos: {pos_before_lexico})")
                print(f"  Contenido de la celda M[{xx}][{self.ae}] = '{interseccion}'")
                return 0
            
            # input("  (presione <ENTER> para continuar)") # Uncomment for step-by-step
            
            
if __name__ == "__main__":
    a = Parser()
    a.leer()