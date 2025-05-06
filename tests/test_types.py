import pytest
from src.types.data_type import DataType
from src.lexer.lexer import Lexer
from src.readers.source_reader import SourceReader
from src.tokens.token_type import TokenType

def get_tokens(source_code: str) -> list:
    """Función auxiliar para obtener tokens de un código fuente"""
    reader = SourceReader(source_code)
    lexer = Lexer(reader)
    return lexer.tokenize()

def test_data_type_ranges():
    """Prueba los rangos de los tipos de datos"""
    # Prueba i8
    i8 = DataType.i8()
    assert i8.check_value(-128)  # Valor mínimo
    assert i8.check_value(127)   # Valor máximo
    assert not i8.check_value(128)  # Fuera de rango
    
    # Prueba u8
    u8 = DataType.u8()
    assert u8.check_value(0)     # Valor mínimo
    assert u8.check_value(255)   # Valor máximo
    assert not u8.check_value(-1)  # Fuera de rango
    
    # Prueba f32
    f32 = DataType.f32()
    assert f32.check_value(3.14159)
    assert f32.check_value(-3.14159)

def test_literal_suffixes():
    """Prueba los sufijos de literales numéricos"""
    source = """
    let x = 42i8;
    let y = 1000i16;
    let z = 3.14f32;
    let w = 123u8;
    """
    tokens = get_tokens(source)
    
    # Verificar que los tokens numéricos tienen los sufijos correctos
    number_tokens = [t for t in tokens if t.type == TokenType.NUMBER]
    assert len(number_tokens) == 4
    
    # Verificar que los sufijos son reconocidos correctamente
    suffixes = ['i8', 'i16', 'f32', 'u8']
    for token, expected_suffix in zip(number_tokens, suffixes):
        assert token.literal_suffix == expected_suffix

def test_type_declarations():
    """Prueba las declaraciones de tipos"""
    source = """
    let entero: i32 = 42;
    let flotante: f64 = 3.14;
    let booleano: bool = true;
    let caracter: char = 'A';
    """
    tokens = get_tokens(source)
    
    # Verificar que los tipos son reconocidos correctamente
    type_tokens = [t for t in tokens if t.type == TokenType.TYPE]
    assert len(type_tokens) == 4
    expected_types = ['i32', 'f64', 'bool', 'char']
    for token, expected_type in zip(type_tokens, expected_types):
        assert token.literal == expected_type

def test_type_casting():
    """Prueba las conversiones de tipos"""
    i32_type = DataType.i32()
    f64_type = DataType.f64()
    bool_type = DataType.bool()
    
    # Conversiones válidas
    assert i32_type.cast_value("42") == 42
    assert f64_type.cast_value("3.14") == 3.14
    assert bool_type.cast_value(1) == True
    assert bool_type.cast_value(0) == False
    
    # Conversiones inválidas
    assert i32_type.cast_value("no_un_número") is None
    assert f64_type.cast_value("invalid") is None

def test_struct_declarations():
    """Prueba las declaraciones de estructuras con tipos"""
    source = """
    struct Punto {
        x: f64,
        y: f64
    }
    """
    tokens = get_tokens(source)
    
    # Verificar la estructura del struct
    assert any(t.type == TokenType.STRUCT for t in tokens)
    assert any(t.type == TokenType.IDENTIFIER and t.literal == "Punto" for t in tokens)
    type_tokens = [t for t in tokens if t.type == TokenType.TYPE]
    assert len(type_tokens) == 2  # Dos campos f64

def test_function_type_signatures():
    """Prueba las firmas de tipos en funciones"""
    source = """
    fn suma(a: i32, b: i32) -> i32 {
        return a + b;
    }
    """
    tokens = get_tokens(source)
    
    # Verificar la firma de tipos de la función
    assert any(t.type == TokenType.FN for t in tokens)
    assert any(t.type == TokenType.IDENTIFIER and t.literal == "suma" for t in tokens)
    type_tokens = [t for t in tokens if t.type == TokenType.TYPE]
    assert len(type_tokens) == 3  # Dos parámetros y un retorno, todos i32

def test_invalid_type_values():
    """Prueba valores inválidos para los tipos"""
    source = """
    let x: u8 = 256;  // Fuera de rango
    let y: i8 = -129; // Fuera de rango
    let z: char = 'AB';  // Más de un carácter
    """
    tokens = get_tokens(source)
    
    # Verificar que se generan errores para valores fuera de rango
    error_tokens = [t for t in tokens if t.type == TokenType.ERROR]
    assert len(error_tokens) > 0 