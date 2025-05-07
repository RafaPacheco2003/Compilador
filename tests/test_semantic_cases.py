import pytest
from src.semantic.semantic_analyzer import SemanticAnalyzer
from src.tokens.token import Token
from src.tokens.token_type import TokenType
from src.types.data_type import DataType

def create_token(type: TokenType, lexeme: str, literal=None, line=1, column=1, data_type=None, literal_suffix=None) -> Token:
    """Helper para crear tokens de prueba."""
    return Token(type, lexeme, literal, line, column, data_type, literal_suffix)

class TestSemanticCases:
    """Pruebas específicas para diferentes casos del analizador semántico."""
    
    @pytest.fixture
    def analyzer(self):
        """Fixture que proporciona una instancia limpia del analizador."""
        return SemanticAnalyzer()
    
    def test_u8_range(self, analyzer):
        """Prueba el rango de valores para u8 (0-255)."""
        test_cases = [
            (0, True),      # Mínimo válido
            (255, True),    # Máximo válido
            (256, False),   # Fuera de rango superior
            (-1, False),    # Fuera de rango inferior
        ]
        
        for value, should_be_valid in test_cases:
            token = create_token(TokenType.NUMBER, str(value), value)
            is_valid = analyzer.check_type_compatibility(token, DataType.u8())
            assert is_valid == should_be_valid, f"Falló para u8 con valor {value}"
    
    def test_i8_range(self, analyzer):
        """Prueba el rango de valores para i8 (-128 a 127)."""
        test_cases = [
            (-128, True),   # Mínimo válido
            (127, True),    # Máximo válido
            (128, False),   # Fuera de rango superior
            (-129, False),  # Fuera de rango inferior
        ]
        
        for value, should_be_valid in test_cases:
            token = create_token(TokenType.NUMBER, str(value), value)
            is_valid = analyzer.check_type_compatibility(token, DataType.i8())
            assert is_valid == should_be_valid, f"Falló para i8 con valor {value}"
    
    def test_string_operations(self, analyzer):
        """Prueba operaciones con strings."""
        # String + String (válido)
        tokens_valid = [
            create_token(TokenType.STRING, '"Hola "', "Hola "),
            create_token(TokenType.PLUS, "+"),
            create_token(TokenType.STRING, '"mundo"', "mundo"),
        ]
        
        result = analyzer.validate_operation(tokens_valid[0], tokens_valid[1], tokens_valid[2])
        assert result is not None, "La concatenación de strings debería ser válida"
        
        # String + Number (inválido)
        tokens_invalid = [
            create_token(TokenType.STRING, '"Texto"', "Texto"),
            create_token(TokenType.PLUS, "+"),
            create_token(TokenType.NUMBER, "42", 42),
        ]
        
        result = analyzer.validate_operation(tokens_invalid[0], tokens_invalid[1], tokens_invalid[2])
        assert result is None, "La suma de string y número debería ser inválida"
    
    def test_type_conversion(self, analyzer):
        """Prueba conversiones entre tipos."""
        # i32 a i64 (válido - promoción segura)
        i32_token = create_token(TokenType.NUMBER, "42", 42, data_type=DataType.i32())
        assert analyzer.check_type_compatibility(i32_token, DataType.i64())
        
        # f64 a i32 (inválido - pérdida de precisión)
        f64_token = create_token(TokenType.NUMBER, "3.14", 3.14, data_type=DataType.f64())
        assert not analyzer.check_type_compatibility(f64_token, DataType.i32())
    
    def test_overflow_detection(self, analyzer):
        """Prueba la detección de overflow en operaciones."""
        max_u16 = create_token(TokenType.NUMBER, "65535", 65535, data_type=DataType.u16())
        one = create_token(TokenType.NUMBER, "1", 1)
        plus = create_token(TokenType.PLUS, "+")
        
        result_type = analyzer.validate_operation(max_u16, plus, one)
        assert result_type is not None, "La operación debería ser válida sintácticamente"
        
        # Verificar que el valor resultante está fuera de rango
        result_token = create_token(TokenType.NUMBER, "65536", 65536)
        assert not analyzer.check_type_compatibility(result_token, DataType.u16())
    
    def test_variable_scope(self, analyzer):
        """Prueba el manejo de ámbito de variables."""
        # Declarar variable
        tokens = [
            create_token(TokenType.LET, "let"),
            create_token(TokenType.IDENTIFIER, "x"),
            create_token(TokenType.COLON, ":"),
            create_token(TokenType.TYPE, "i32"),
            create_token(TokenType.EQUAL, "="),
            create_token(TokenType.NUMBER, "42", 42),
        ]
        
        analyzer.analyze(tokens)
        assert "x" in analyzer.symbol_table
        
        # Intentar redeclarar la misma variable
        analyzer.analyze(tokens)
        assert analyzer.error_handler.has_errors()
        assert any("ya declarada" in str(error) for error in analyzer.error_handler.errors) 