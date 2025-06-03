"""
INTEGRANTES:
    - Cordero Alfaro Renzo Pedro
    - Macchiavello Perez Giuliano
    - Morales Usca Andres Fernando
    - Padilla Gutierrez Rodrigo Fabien

"""

import re

RESERVED_KEYWORDS = {'switch', 'case', 'break'}

TOKEN_SPEC = [
    ('SWITCH', r'switch'),
    ('CASE', r'case'),
    ('BREAK', r'break'),
    ('ID', r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('NUM', r'\d+'),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('LLAVEL', r'\{'),
    ('LLAVER', r'\}'),
    ('DOSPUNTOS', r':'),
    ('PUNTOYCOMA', r';'),
    ('RANGO', r'\.\.'),
    ('SKIP', r'[ \t\n]+'),
    ('MISMATCH', r'.'),
]

TAS = {
    'S': {
        'SWITCH': ['SWITCH', 'LPAREN', 'ID', 'RPAREN', 'LLAVEL', 'C', 'LLAVER', 'A']
    },
    'A': {
        'SWITCH': ['S'],
        'BREAK': ['λ'],
        '$': ['λ']
    },
    'C': {
        'LLAVER': ['λ'],
        'CASE': ['B', 'C']
    },
    'B': {
        'CASE': ['CASE', 'R', 'DOSPUNTOS', 'A', 'BREAK', 'PUNTOYCOMA']
    },
    'R': {
        'NUM': ['NUM', 'T']
    },
    'T': {
        'DOSPUNTOS': ['λ'],
        'RANGO': ['RANGO', 'NUM']
    }
}

class Lexer:
    def __init__(self, code):
        self.code = code

    def tokenize(self):
        tokens = []
        tok_regex = '|'.join(f'(?P<{name}>{regex})' for name, regex in TOKEN_SPEC)

        for match in re.finditer(tok_regex, self.code):
            kind = match.lastgroup
            value = match.group()

            if kind == 'SKIP':
                continue
            if kind == 'ID' and value in RESERVED_KEYWORDS:
                kind = value.upper()
            if kind == 'MISMATCH':
                raise ValueError(f'Carácter no válido: {value}')

            tokens.append((kind, value))

        tokens.append(('$', '$'))
        return tokens

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.stack = ['$', 'S']
        self.index = 0

    def current_token(self):
        return self.tokens[self.index][0]

    def current_value(self):
        return self.tokens[self.index][1]

    def analyze(self):
        print(f"{'PILA':<50} {'ENTRADA':<50} SALIDA")
        raya()

        while True:
            stack_top = self.stack[-1]
            token = self.current_token()
            value = self.current_value()

            stack_str = ' '.join(self.stack)
            input_str = ' '.join(val for _, val in self.tokens[self.index:])
            action = ""

            if stack_top == '$' and token == '$':
                action = "SE ACEPTA"
                print(f"{stack_str:<50} {input_str:<50} {action}")
                return True

            elif stack_top in TAS:
                rule = TAS[stack_top].get(token)
                if rule:
                    action = f"{stack_top} → {' '.join(rule)}"
                    self.stack.pop()
                    if rule != ['λ']:
                        self.stack.extend(reversed(rule))
                else:
                    action = f"ERROR: No producción para {stack_top} con {token} ({value})"
                    print(f"{stack_str:<50} {input_str:<50} {action}")
                    return False

            elif stack_top == token:
                self.stack.pop()
                self.index += 1
                action = f"Emparejar {token}"
            else:
                action = f"ERROR: Esperaba {stack_top}, encontró {token} ({value})"
                print(f"{stack_str:<50} {input_str:<50} {action}")
                return False

            print(f"{stack_str:<50} {input_str:<50} {action}")

def raya():
    print("=" * 150)

if __name__ == "__main__":
    try:
        with open("C:\\Users\\andre\\OneDrive\\Escritorio\\UNI\\Python\\Python\\9.0 LenguajesyCompiladores\\Laboratorio-07\\Terminal.txt", 'r', encoding='utf-8') as file:
            code = file.read()
    except FileNotFoundError:
        print("Archivo no encontrado.")
        exit()
    except Exception as e:
        print(f"Error al leer archivo: {e}")
        exit()

    try:
        lexer = Lexer(code)
        tokens = lexer.tokenize()

        parser = Parser(tokens)
        success = parser.analyze()

        raya()

        print("\nAnálisis completado con éxito!" if success else "\nError durante el análisis.")

    except ValueError as e:
        print(f"\nError léxico: {e}")
