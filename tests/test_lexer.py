import pytest
from src.lexer.lexer import Lexer
from src.readers.source_reader import SourceReader
from src.tokens.token_type import TokenType

def get_tokens(source_code: str) -> list:
    """Función auxiliar para obtener tokens de un código fuente"""
    reader = SourceReader(source_code)
    lexer = Lexer(reader)
    return lexer.tokenize()

def test_empty_input():
    """Prueba con entrada vacía"""
    tokens = get_tokens("")
    assert len(tokens) == 1
    assert tokens[0].type == TokenType.EOF

def test_whitespace():
    """Prueba con espacios en blanco"""
    tokens = get_tokens("   \t\n   ")
    assert len(tokens) == 1
    assert tokens[0].type == TokenType.EOF

def test_single_character_tokens():
    """Prueba tokens de un solo carácter"""
    source = "(){},.-+;*"
    tokens = get_tokens(source)
    expected_types = [
        TokenType.LEFT_PAREN,
        TokenType.RIGHT_PAREN,
        TokenType.LEFT_BRACE,
        TokenType.RIGHT_BRACE,
        TokenType.COMMA,
        TokenType.DOT,
        TokenType.MINUS,
        TokenType.PLUS,
        TokenType.SEMICOLON,
        TokenType.STAR,
        TokenType.EOF
    ]
    
    assert len(tokens) == len(expected_types)
    for token, expected_type in zip(tokens, expected_types):
        assert token.type == expected_type

def test_two_character_tokens():
    """Prueba tokens de dos caracteres"""
    source = "== != <= >= ="
    tokens = get_tokens(source)
    expected_types = [
        TokenType.EQUAL_EQUAL,
        TokenType.BANG_EQUAL,
        TokenType.LESS_EQUAL,
        TokenType.GREATER_EQUAL,
        TokenType.EQUAL,
        TokenType.EOF
    ]
    
    assert len(tokens) == len(expected_types)
    for token, expected_type in zip(tokens, expected_types):
        assert token.type == expected_type

def test_string_literals():
    """Prueba literales de string"""
    source = '"Hello, World!" "Test" ""'
    tokens = get_tokens(source)
    
    assert len(tokens) == 4  # 3 strings + EOF
    assert tokens[0].type == TokenType.STRING
    assert tokens[0].literal == "Hello, World!"
    assert tokens[1].type == TokenType.STRING
    assert tokens[1].literal == "Test"
    assert tokens[2].type == TokenType.STRING
    assert tokens[2].literal == ""

def test_number_literals():
    """Prueba literales numéricos"""
    source = "42 3.14 0.123 456.0"
    tokens = get_tokens(source)
    
    assert len(tokens) == 5  # 4 números + EOF
    assert tokens[0].type == TokenType.NUMBER
    assert tokens[0].literal == 42.0
    assert tokens[1].type == TokenType.NUMBER
    assert tokens[1].literal == 3.14
    assert tokens[2].type == TokenType.NUMBER
    assert tokens[2].literal == 0.123
    assert tokens[3].type == TokenType.NUMBER
    assert tokens[3].literal == 456.0

def test_identifiers():
    """Prueba identificadores"""
    source = "variable_1 _test test123"
    tokens = get_tokens(source)
    
    assert len(tokens) == 4  # 3 identificadores + EOF
    assert all(token.type == TokenType.IDENTIFIER for token in tokens[:-1])
    assert tokens[0].literal == "variable_1"
    assert tokens[1].literal == "_test"
    assert tokens[2].literal == "test123"

def test_keywords():
    """Prueba palabras clave"""
    source = "if else while fn return true false"
    tokens = get_tokens(source)
    
    expected_types = [
        TokenType.IF,
        TokenType.ELSE,
        TokenType.WHILE,
        TokenType.FN,
        TokenType.RETURN,
        TokenType.TRUE,
        TokenType.FALSE,
        TokenType.EOF
    ]
    
    assert len(tokens) == len(expected_types)
    for token, expected_type in zip(tokens, expected_types):
        assert token.type == expected_type

def test_complete_expression():
    """Prueba una expresión completa"""
    source = """
    fn factorial(n) {
        if (n <= 1) {
            return 1;
        }
        return n * factorial(n - 1);
    }
    """
    tokens = get_tokens(source)
    
    # Verificar algunos tokens clave
    assert any(t.type == TokenType.FN for t in tokens)
    assert any(t.type == TokenType.IDENTIFIER and t.literal == "factorial" for t in tokens)
    assert any(t.type == TokenType.LESS_EQUAL for t in tokens)
    assert any(t.type == TokenType.RETURN for t in tokens)

def test_error_handling():
    """Prueba manejo de errores"""
    # String sin cerrar
    tokens = get_tokens('"unclosed string')
    assert any(t.type == TokenType.ERROR for t in tokens)
    
    # Carácter inválido
    tokens = get_tokens('@#$')
    assert any(t.type == TokenType.ERROR for t in tokens)

def test_line_numbers():
    """Prueba números de línea"""
    source = """
    line1
    line2
    line3
    """
    tokens = get_tokens(source)
    
    # Verificar que los tokens tienen los números de línea correctos
    line_numbers = [token.line for token in tokens if token.type == TokenType.IDENTIFIER]
    assert line_numbers == [2, 3, 4]

def test_comments():
    """Prueba comentarios"""
    source = """
    // Este es un comentario
    x = 42; // Otro comentario
    y = 10;
    """
    tokens = get_tokens(source)
    
    # Verificar que los comentarios son ignorados
    assert all(t.type != TokenType.ERROR for t in tokens)
    assert any(t.type == TokenType.IDENTIFIER and t.literal == "x" for t in tokens)
    assert any(t.type == TokenType.IDENTIFIER and t.literal == "y" for t in tokens)

if __name__ == "__main__":
    # Ejecutar todas las pruebas y mostrar resultados
    print("Ejecutando pruebas del analizador léxico...")
    
    # Código de ejemplo para demostración
    source_code = """
    fn factorial(n) {
        if (n <= 1) {
            return 1;
        }
        return n * factorial(n - 1);
    }
    
    // Calcular factorial de 5
    result = factorial(5);
    """
    
    reader = SourceReader(source_code)
    lexer = Lexer(reader)
    tokens = lexer.tokenize()
    
    print("\nTokens encontrados en el ejemplo:")
    print("-" * 40)
    for token in tokens:
        print(token) 