from enum import Enum, auto

class TokenType(Enum):
    """
    Enumeración que define todos los tipos de tokens posibles en el lenguaje.
    Incluye soporte para tipos de datos fuertes similar a Rust.
    """
    # Tipos de datos
    TYPE = auto()         # Tipo de dato genérico
    TYPE_I8 = auto()      # i8: entero con signo de 8 bits (-128 a 127)
    TYPE_I16 = auto()     # i16: entero con signo de 16 bits (-32,768 a 32,767)
    TYPE_I32 = auto()     # i32: entero con signo de 32 bits (default para enteros)
    TYPE_I64 = auto()     # i64: entero con signo de 64 bits
    TYPE_U8 = auto()      # u8: entero sin signo de 8 bits (0 a 255)
    TYPE_U16 = auto()     # u16: entero sin signo de 16 bits (0 a 65,535)
    TYPE_U32 = auto()     # u32: entero sin signo de 32 bits
    TYPE_U64 = auto()     # u64: entero sin signo de 64 bits
    TYPE_F32 = auto()     # f32: punto flotante de 32 bits
    TYPE_F64 = auto()     # f64: punto flotante de 64 bits (default para flotantes)
    TYPE_BOOL = auto()    # bool: booleano
    TYPE_CHAR = auto()    # char: carácter Unicode
    TYPE_STR = auto()     # &str: string
    TYPE_STRING = auto()  # String: string owned

    # Literales
    NUMBER = auto()       # Números (enteros o flotantes)
    STRING = auto()       # Cadenas de texto
    CHAR = auto()         # Caracteres
    TRUE = auto()         # true
    FALSE = auto()        # false

    # Palabras clave de declaración
    LET = auto()         # let: declaración de variables
    MUT = auto()         # mut: mutabilidad
    FN = auto()          # fn: declaración de funciones
    STRUCT = auto()      # struct: declaración de estructuras
    ENUM = auto()        # enum: declaración de enumeraciones
    IMPL = auto()        # impl: implementación de métodos
    PUB = auto()         # pub: visibilidad pública
    RETURN = auto()      # return
    IF = auto()          # if
    ELSE = auto()        # else
    WHILE = auto()       # while
    FOR = auto()         # for
    IN = auto()          # in

    # Operadores
    PLUS = auto()        # +
    MINUS = auto()       # -
    STAR = auto()        # *
    SLASH = auto()       # /
    PERCENT = auto()     # %
    EQUAL = auto()       # =
    EQUAL_EQUAL = auto() # ==
    BANG = auto()        # !
    BANG_EQUAL = auto()  # !=
    LESS = auto()        # <
    LESS_EQUAL = auto()  # <=
    GREATER = auto()     # >
    GREATER_EQUAL = auto() # >=
    AND = auto()         # &&
    OR = auto()          # ||
    COLON = auto()       # :
    DOUBLE_COLON = auto() # ::
    ARROW = auto()       # ->
    FAT_ARROW = auto()   # =>

    # Delimitadores
    LEFT_PAREN = auto()    # (
    RIGHT_PAREN = auto()   # )
    LEFT_BRACE = auto()    # {
    RIGHT_BRACE = auto()   # }
    LEFT_BRACKET = auto()  # [
    RIGHT_BRACKET = auto() # ]
    COMMA = auto()         # ,
    DOT = auto()          # .
    SEMICOLON = auto()     # ;
    
    # Identificadores y otros
    IDENTIFIER = auto()    # nombres de variables, funciones, etc.
    COMMENT = auto()       # comentarios
    EOF = auto()          # fin de archivo
    ERROR = auto()        # token de error 