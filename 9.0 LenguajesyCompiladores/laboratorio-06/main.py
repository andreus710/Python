import re

TOKEN_CODES = {
    'PALABRA_RESERVADA': 400,
    'ACCESO': 401,
    'TIPO_VARIABLE': 402,
    'CLASES': 403,
    'IDENTIFICADOR': 100,
    'ENTERO': 300,
    'REAL': 301,
    'CARACTER': 302,
    'CADENA': 303,
    'BOOLEANO': 304,
    'OPERADOR': 200,
    'DELIMITADOR': 201,
    'COMENTARIO': 500,
    'LECTURA_ESCRITURA': 600,
    'ERROR': 911
}

token_specification = [
    ('COMENTARIO', r'//.*'),
    ('CADENA', r'"[^"\n]*"'),
    ('CARACTER', r"'[^'\n]'"),
    ('REAL', r'\d+\.\d+'),
    ('ENTERO', r'\d+'),
    ('OPERADOR', r'==|<-|!=|<=|>=|&&|\|\||[+\-*/<>]'),
    ('DELIMITADOR', r'[;:,()\[\]{}]'),
    ('ACCESO', r'\b(?:public|private|protected|static|final)\b'),
    ('PALABRA_RESERVADA', r'\b(?:si|sino|mientras|para|segun|caso|defecto|hacer|clase|void)\b'),
    ('TIPO_VARIABLE', r'\b(?:int|float|char|string|bool)\b'),
    ('CLASES', r'\b(?:extiende|super|this|new)\b'),
    ('BOOLEANO', r'\b(?:true|false)\b'),
    ('LECTURA_ESCRITURA', r'\b(?:impr|imprln|leer|leerInt|leerFloat)\b'),
    ('IDENTIFICADOR', r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('ESPACIO', r'[ \t]+'),
    ('SALTO_LINEA', r'\n'),
    ('ERROR', r'.'),
]

token_re = re.compile('|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification))

def analizador_lexico(codigo_fuente):
    lineas = codigo_fuente.split('\n')

    for num_linea, linea in enumerate(lineas, start=1):
        tokens = []
        for match in token_re.finditer(linea):
            tipo = match.lastgroup
            valor = match.group()
            if tipo in ['ESPACIO']:
                continue
            codigo = TOKEN_CODES.get(tipo, 911)
            tokens.append((tipo, valor, codigo))

        if tokens:
            print(f"[Línea {num_linea}]")
            for tipo, valor, codigo in tokens:
                print(f"\t{tipo} (código {codigo}): {valor}")
            print()  # Separador entre líneas

with open('C:/Users/andre/OneDrive/Escritorio/UNI/Python/Python/9.0 LenguajesyCompiladores/read.txt', 'r') as archivo:
    contenido = archivo.read()

analizador_lexico(contenido)
