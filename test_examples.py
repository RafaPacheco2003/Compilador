from src.lexer.lexer import Lexer
from src.readers.source_reader import SourceReader
from src.tokens.token_type import TokenType
import os

def format_token_value(token):
    """Formatea el valor del token para mejor visualización"""
    if token.type == TokenType.STRING:
        return f'"{token.literal}"'
    elif token.type == TokenType.CHAR:
        return f"'{token.literal}'"
    elif token.type == TokenType.NUMBER:
        suffix = f":{token.literal_suffix}" if token.literal_suffix else ""
        return f"{token.literal}{suffix}"
    elif token.type == TokenType.TYPE:
        return token.literal
    elif token.type == TokenType.IDENTIFIER:
        return token.literal
    elif token.type in [TokenType.TRUE, TokenType.FALSE]:
        return str(token.type.name).lower()
    return ""

def print_token_table(tokens):
    """Imprime los tokens en formato de tabla"""
    # Definir anchos de columna
    col_widths = {
        "LÍNEA": 6,
        "COL": 5,
        "TIPO": 15,
        "LEXEMA": 20,
        "VALOR": 20,
        "TIPO_DATO": 10
    }
    
    # Imprimir encabezado
    header = "┌" + "┬".join("─" * width for width in col_widths.values()) + "┐"
    print(header)
    
    # Imprimir títulos
    row_format = "│{:^6}│{:^5}│{:^15}│{:^20}│{:^20}│{:^10}│"
    print(row_format.format("LÍNEA", "COL", "TIPO", "LEXEMA", "VALOR", "TIPO_DATO"))
    
    # Imprimir separador
    separator = "├" + "┼".join("─" * width for width in col_widths.values()) + "┤"
    print(separator)
    
    # Imprimir tokens
    for token in tokens:
        tipo = token.type.name
        valor = format_token_value(token)
        tipo_dato = str(token.data_type) if token.data_type else ""
        print(row_format.format(
            token.line,
            token.column,
            tipo[:15],
            str(token.lexeme)[:20],
            valor[:20],
            tipo_dato[:10]
        ))
    
    # Imprimir pie
    footer = "└" + "┴".join("─" * width for width in col_widths.values()) + "┘"
    print(footer)

def print_token_summary(tokens):
    """Imprime un resumen de los tipos de tokens encontrados"""
    token_counts = {}
    for token in tokens:
        token_type = token.type.name
        token_counts[token_type] = token_counts.get(token_type, 0) + 1
    
    print("\nResumen de Tokens:")
    print("=" * 40)
    
    # Agrupar por categorías
    categories = {
        "Tipos": [t for t in token_counts.keys() if t.startswith("TYPE_") or t == "TYPE"],
        "Literales": ["NUMBER", "STRING", "CHAR", "TRUE", "FALSE"],
        "Palabras clave": ["LET", "MUT", "FN", "STRUCT", "ENUM", "IMPL", "PUB", "RETURN", "IF", "ELSE", "WHILE", "FOR", "IN"],
        "Operadores": ["PLUS", "MINUS", "STAR", "SLASH", "PERCENT", "EQUAL", "EQUAL_EQUAL", "BANG", "BANG_EQUAL", 
                      "LESS", "LESS_EQUAL", "GREATER", "GREATER_EQUAL", "AND", "OR", "COLON", "DOUBLE_COLON", 
                      "ARROW", "FAT_ARROW"],
        "Delimitadores": ["LEFT_PAREN", "RIGHT_PAREN", "LEFT_BRACE", "RIGHT_BRACE", "LEFT_BRACKET", "RIGHT_BRACKET",
                         "COMMA", "DOT", "SEMICOLON"],
        "Otros": ["IDENTIFIER", "COMMENT", "EOF", "ERROR"]
    }
    
    for category, types in categories.items():
        count = sum(token_counts.get(t, 0) for t in types)
        if count > 0:
            print(f"\n{category}:")
            print("-" * 20)
            for t in types:
                if t in token_counts:
                    print(f"{t:15} : {token_counts[t]} tokens")
    
    print("\n" + "=" * 40)
    print(f"Total de tokens: {len(tokens)}")

def analyze_file(filename: str):
    """
    Analiza un archivo y muestra los tokens encontrados
    """
    print(f"\nAnalizando archivo: {filename}")
    print("=" * 70)
    
    try:
        # Leer el archivo y mostrar el contenido
        with open(filename, 'r', encoding='utf-8') as file:
            source_code = file.read()
        
        print("Código fuente:")
        print("-" * 70)
        print(source_code)
        print("-" * 70)
        
        # Crear el lexer y obtener tokens
        reader = SourceReader(source_code)
        lexer = Lexer(reader)
        tokens = lexer.tokenize()
        
        # Mostrar tokens en formato de tabla
        print("\nTokens encontrados:")
        print_token_table(tokens)
        
        # Mostrar resumen
        print_token_summary(tokens)
        
    except Exception as e:
        print(f"Error al analizar el archivo: {e}")

def main():
    # Directorio de ejemplos
    examples_dir = "examples"
    
    # Obtener todos los archivos .txt del directorio
    example_files = [f for f in os.listdir(examples_dir) if f.endswith('.txt')]
    
    print(f"Encontrados {len(example_files)} archivos de ejemplo:")
    for i, file in enumerate(example_files, 1):
        print(f"{i}. {file}")
    
    while True:
        print("\nOpciones:")
        print("1-N. Analizar un archivo específico")
        print("0. Analizar todos los archivos")
        print("q. Salir")
        
        choice = input("\nElige una opción: ").lower()
        
        if choice == 'q':
            break
        
        try:
            if choice == '0':
                # Analizar todos los archivos
                for file in example_files:
                    analyze_file(os.path.join(examples_dir, file))
                    input("\nPresiona Enter para continuar...")
            else:
                # Analizar archivo específico
                index = int(choice) - 1
                if 0 <= index < len(example_files):
                    analyze_file(os.path.join(examples_dir, example_files[index]))
                else:
                    print("Número de archivo inválido")
        except ValueError:
            print("Opción inválida")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main() 