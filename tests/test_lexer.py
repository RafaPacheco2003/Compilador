from src.lexer.lexer import Lexer
from src.readers.source_reader import SourceReader
from src.tokens.token_type import TokenType

def main():
    # Código de ejemplo
    source_code = """
    function factorial(n) {
        if (n <= 1) {
            return 1;
        }
        return n * factorial(n - 1);
    }
    
    // Calcular factorial de 5
    result = factorial(5);
    """
    
    # Crear el lector de código fuente
    reader = SourceReader(source_code)
    
    # Crear el analizador léxico
    lexer = Lexer(reader)
    
    # Obtener todos los tokens
    tokens = lexer.tokenize()
    
    # Imprimir los tokens
    print("Tokens encontrados:")
    print("-----------------")
    for token in tokens:
        print(token)

if __name__ == "__main__":
    main() 