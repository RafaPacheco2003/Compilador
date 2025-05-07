import pytest
from src.semantic.semantic_analyzer import SemanticAnalyzer
from src.tokens.token import Token
from src.tokens.token_type import TokenType
from src.types.data_type import DataType

def create_token(type: TokenType, lexeme: str, literal=None, line=1, column=1, data_type=None, literal_suffix=None) -> Token:
    """Helper para crear tokens de prueba."""
    return Token(type, lexeme, literal, line, column, data_type, literal_suffix)

class TestSemanticAnalyzer:
    """
    Pruebas unitarias para el analizador semántico.
    Verifica la correcta validación de tipos y detección de errores semánticos.
    """
    
    @pytest.fixture
    def analyzer(self):
        """Fixture que proporciona una instancia limpia del analizador para cada prueba."""
        return SemanticAnalyzer()
    
    def test_variable_declaration_valid(self, analyzer):
        """Prueba una declaración de variable válida."""
        tokens = [
            create_token(TokenType.LET, "let"),
            create_token(TokenType.IDENTIFIER, "x"),
            create_token(TokenType.COLON, ":"),
            create_token(TokenType.TYPE, "i32"),
            create_token(TokenType.EQUAL, "="),
            create_token(TokenType.NUMBER, "42", 42),
            create_token(TokenType.SEMICOLON, ";")
        ]
        
        analyzer.analyze(tokens)
        assert not analyzer.error_handler.has_errors()
        assert "x" in analyzer.symbol_table
        
    def test_variable_declaration_type_mismatch(self, analyzer):
        """Prueba una declaración con tipo incompatible."""
        tokens = [
            create_token(TokenType.LET, "let"),
            create_token(TokenType.IDENTIFIER, "x"),
            create_token(TokenType.COLON, ":"),
            create_token(TokenType.TYPE, "u8"),
            create_token(TokenType.EQUAL, "="),
            create_token(TokenType.NUMBER, "256", 256),  # Fuera del rango de u8
            create_token(TokenType.SEMICOLON, ";")
        ]
        
        analyzer.analyze(tokens)
        assert analyzer.error_handler.has_errors()
        
    def test_variable_redeclaration(self, analyzer):
        """Prueba la redeclaración de una variable."""
        tokens = [
            # Primera declaración
            create_token(TokenType.LET, "let"),
            create_token(TokenType.IDENTIFIER, "x"),
            create_token(TokenType.COLON, ":"),
            create_token(TokenType.TYPE, "i32"),
            create_token(TokenType.EQUAL, "="),
            create_token(TokenType.NUMBER, "42", 42),
            create_token(TokenType.SEMICOLON, ";"),
            # Segunda declaración del mismo identificador
            create_token(TokenType.LET, "let"),
            create_token(TokenType.IDENTIFIER, "x"),
            create_token(TokenType.COLON, ":"),
            create_token(TokenType.TYPE, "i32"),
            create_token(TokenType.EQUAL, "="),
            create_token(TokenType.NUMBER, "43", 43),
            create_token(TokenType.SEMICOLON, ";")
        ]
        
        analyzer.analyze(tokens)
        assert analyzer.error_handler.has_errors()
        error = analyzer.error_handler.errors[0]
        assert "ya declarada" in error.message
        
    def test_arithmetic_operations(self, analyzer):
        """Prueba operaciones aritméticas con tipos compatibles e incompatibles."""
        # Operación válida
        tokens_valid = [
            create_token(TokenType.NUMBER, "10", 10),
            create_token(TokenType.PLUS, "+"),
            create_token(TokenType.NUMBER, "20", 20),
            create_token(TokenType.SEMICOLON, ";")
        ]
        
        analyzer.analyze(tokens_valid)
        assert not analyzer.error_handler.has_errors()
        
        # Operación inválida (mezcla de tipos incompatibles)
        tokens_invalid = [
            create_token(TokenType.STRING, '"texto"', "texto"),
            create_token(TokenType.PLUS, "+"),
            create_token(TokenType.NUMBER, "42", 42),
            create_token(TokenType.SEMICOLON, ";")
        ]
        
        analyzer.analyze(tokens_invalid)
        assert analyzer.error_handler.has_errors()
        
    def test_type_ranges(self, analyzer):
        """Prueba la validación de rangos para diferentes tipos de datos."""
        test_cases = [
            # u8: 0 a 255
            (DataType.u8(), 0, True),
            (DataType.u8(), 255, True),
            (DataType.u8(), 256, False),
            (DataType.u8(), -1, False),
            
            # i8: -128 a 127
            (DataType.i8(), -128, True),
            (DataType.i8(), 127, True),
            (DataType.i8(), 128, False),
            (DataType.i8(), -129, False),
            
            # u16: 0 a 65535
            (DataType.u16(), 0, True),
            (DataType.u16(), 65535, True),
            (DataType.u16(), 65536, False),
            (DataType.u16(), -1, False),
        ]
        
        for data_type, value, should_be_valid in test_cases:
            token = create_token(TokenType.NUMBER, str(value), value)
            is_valid = analyzer.check_type_compatibility(token, data_type)
            assert is_valid == should_be_valid, f"Falló para {data_type.name} con valor {value}"
            
    def test_complex_expression(self, analyzer):
        """Prueba una expresión compleja con múltiples operaciones."""
        # Declarar variables
        setup_tokens = [
            create_token(TokenType.LET, "let"),
            create_token(TokenType.IDENTIFIER, "a"),
            create_token(TokenType.COLON, ":"),
            create_token(TokenType.TYPE, "i32"),
            create_token(TokenType.EQUAL, "="),
            create_token(TokenType.NUMBER, "10", 10),
            create_token(TokenType.SEMICOLON, ";"),
            
            create_token(TokenType.LET, "let"),
            create_token(TokenType.IDENTIFIER, "b"),
            create_token(TokenType.COLON, ":"),
            create_token(TokenType.TYPE, "i32"),
            create_token(TokenType.EQUAL, "="),
            create_token(TokenType.NUMBER, "20", 20),
            create_token(TokenType.SEMICOLON, ";"),
        ]
        
        analyzer.analyze(setup_tokens)
        assert not analyzer.error_handler.has_errors()
        
        # Expresión: a + b * 2
        expression_tokens = [
            create_token(TokenType.IDENTIFIER, "a"),
            create_token(TokenType.PLUS, "+"),
            create_token(TokenType.IDENTIFIER, "b"),
            create_token(TokenType.STAR, "*"),
            create_token(TokenType.NUMBER, "2", 2),
            create_token(TokenType.SEMICOLON, ";")
        ]
        
        analyzer.analyze(expression_tokens)
        assert not analyzer.error_handler.has_errors()
        
    def test_error_reporting(self, analyzer):
        """Prueba el formato y contenido de los mensajes de error."""
        tokens = [
            create_token(TokenType.LET, "let"),
            create_token(TokenType.IDENTIFIER, "x"),
            create_token(TokenType.COLON, ":"),
            create_token(TokenType.TYPE, "u8"),
            create_token(TokenType.EQUAL, "="),
            create_token(TokenType.NUMBER, "256", 256, line=5, column=10),
            create_token(TokenType.SEMICOLON, ";")
        ]
        
        analyzer.analyze(tokens)
        assert analyzer.error_handler.has_errors()
        
        error = analyzer.error_handler.errors[0]
        error_str = str(error)
        
        # Verificar que el mensaje de error contiene la información necesaria
        assert "línea 5" in error_str
        assert "columna 10" in error_str
        assert "256" in error_str
        assert "u8" in error_str 