from enum import Enum, auto

class TokenType(Enum):
    """
    Operadores: +, -, *, /, =, ==, !=, etc.
    Delimitadores: (, ), {, }, ;, etc.
    Palabras clave: if, else, while, function, etc.
    Literales: números, strings, identificadores
    Tokens especiales: EOF (fin de archivo), ERROR
    
    Enumeración que define todos los tipos de tokens posibles en el lenguaje.
    Siguiendo el principio Single Responsibility, esta clase solo se encarga de definir los tipos de tokens.
    """
    # Tokens de un solo carácter
    LEFT_PAREN = auto()    # (
    RIGHT_PAREN = auto()   # )
    LEFT_BRACE = auto()    # {
    RIGHT_BRACE = auto()   # }
    COMMA = auto()         # ,
    DOT = auto()          # .
    MINUS = auto()        # -
    PLUS = auto()         # +
    SEMICOLON = auto()    # ;
    SLASH = auto()        # /
    STAR = auto()         # *

    # Tokens de uno o dos caracteres
    BANG = auto()         # !
    BANG_EQUAL = auto()   # !=
    EQUAL = auto()        # =
    EQUAL_EQUAL = auto()  # ==
    GREATER = auto()      # >
    GREATER_EQUAL = auto()# >=
    LESS = auto()         # <
    LESS_EQUAL = auto()   # <=

    # Literales
    IDENTIFIER = auto()   # identificadores
    STRING = auto()       # cadenas
    NUMBER = auto()       # números

    # Palabras clave
    AND = auto()
    OR = auto()
    IF = auto()
    ELSE = auto()
    FOR = auto()
    WHILE = auto()
    FUNCTION = auto()
    RETURN = auto()
    TRUE = auto()
    FALSE = auto()
    
    # Tokens especiales
    EOF = auto()          # fin de archivo
    ERROR = auto()        # token de error 