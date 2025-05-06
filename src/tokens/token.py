from dataclasses import dataclass
from typing import Any
from .token_type import TokenType

@dataclass
class Token:
    """
    type: El tipo de token (de TokenType)
    lexeme: El texto exacto encontrado en el código
    literal: El valor procesado (por ejemplo, para números convierte el string a float)
    line y column: La ubicación exacta para mensajes de error



    Clase que representa un token individual en el análisis léxico.
    Siguiendo el principio Single Responsibility, esta clase solo se encarga de almacenar
    la información de un token.
    
    Attributes:
        type (TokenType): El tipo de token.
        lexeme (str): El texto literal del token.
        literal (Any): El valor literal del token (para strings, números, etc.).
        line (int): La línea donde se encontró el token.
        column (int): La columna donde se encontró el token.
    """
    type: TokenType    # Tipo del token
    lexeme: str       # Texto original
    literal: Any      # Valor procesado
    line: int         # Línea donde se encontró
    column: int       # Columna donde se encontró

    def __str__(self) -> str:
        """
        Retorna una representación en string del token.
        
        Returns:
            str: Representación del token en formato legible.
        """
        return f"Token({self.type}, '{self.lexeme}', {self.literal}, line={self.line}, col={self.column})" 