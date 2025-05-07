from enum import Enum, auto

class TokenType(Enum):
    """
    Enumeración que define los tipos de tokens para el lenguaje.
    Se enfoca especialmente en el sistema de tipos y sus rangos.
    """
    # Tipos de datos básicos
    TYPE_I8 = auto()      # i8: entero con signo de 8 bits (-128 a 127)
    TYPE_I16 = auto()     # i16: entero con signo de 16 bits (-32,768 a 32,767)
    TYPE_I32 = auto()     # i32: entero con signo de 32 bits (-2^31 a 2^31-1)
    TYPE_I64 = auto()     # i64: entero con signo de 64 bits (-2^63 a 2^63-1)
    TYPE_U8 = auto()      # u8: entero sin signo de 8 bits (0 a 255)
    TYPE_U16 = auto()     # u16: entero sin signo de 16 bits (0 a 65,535)
    TYPE_U32 = auto()     # u32: entero sin signo de 32 bits (0 a 2^32-1)
    TYPE_U64 = auto()     # u64: entero sin signo de 64 bits (0 a 2^64-1)
    TYPE_F32 = auto()     # f32: punto flotante de 32 bits
    TYPE_F64 = auto()     # f64: punto flotante de 64 bits
    TYPE_BOOL = auto()    # bool: booleano
    TYPE_CHAR = auto()    # char: carácter Unicode
    TYPE_STRING = auto()  # string: cadena de texto
    TYPE = auto()         # Para tokens de tipo

    # Literales
    NUMBER = auto()       # Números (enteros o flotantes)
    STRING = auto()       # Cadenas de texto
    CHAR = auto()         # Caracteres
    TRUE = auto()         # true
    FALSE = auto()        # false

    # Palabras clave
    LET = auto()         # Declaración de variables
    
    # Operadores
    PLUS = auto()        # +
    MINUS = auto()       # -
    STAR = auto()        # *
    SLASH = auto()       # /
    EQUAL = auto()       # =
    EQUAL_EQUAL = auto() # ==
    BANG_EQUAL = auto()  # !=
    LESS = auto()        # <
    LESS_EQUAL = auto()  # <=
    GREATER = auto()     # >
    GREATER_EQUAL = auto()# >=
    COLON = auto()       # :
    
    # Delimitadores
    SEMICOLON = auto()    # ;
    LEFT_PAREN = auto()   # (
    RIGHT_PAREN = auto()  # )
    LEFT_BRACE = auto()   # {
    RIGHT_BRACE = auto()  # }
    LEFT_BRACKET = auto() # [
    RIGHT_BRACKET = auto()# ]
    COMMA = auto()        # ,
    DOT = auto()         # .
    
    # Otros
    IDENTIFIER = auto()   # Identificadores
    EOF = auto()         # Fin de archivo
    ERROR = auto()       # Token de error 