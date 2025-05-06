from dataclasses import dataclass
from typing import Any, Optional
from .token_type import TokenType
from ..types.data_type import DataType

@dataclass
class Token:
    """
    Clase que representa un token individual en el análisis léxico.
    Ahora incluye soporte para tipos de datos fuertes.
    
    Attributes:
        type (TokenType): El tipo de token.
        lexeme (str): El texto literal del token.
        literal (Any): El valor literal del token (para strings, números, etc.).
        line (int): La línea donde se encontró el token.
        column (int): La columna donde se encontró el token.
        data_type (Optional[DataType]): El tipo de dato del token (si aplica).
        literal_suffix (Optional[str]): El sufijo de tipo para literales (e.g., i32, f64).
    """
    type: TokenType    # Tipo del token
    lexeme: str       # Texto original
    literal: Any      # Valor procesado
    line: int         # Línea donde se encontró
    column: int       # Columna donde se encontró
    data_type: Optional[DataType] = None
    literal_suffix: Optional[str] = None

    def __str__(self) -> str:
        """
        Retorna una representación en string del token.
        
        Returns:
            str: Representación del token en formato legible.
        """
        type_info = ""
        if self.data_type:
            type_info += f":{self.data_type}"
        if self.literal_suffix:
            type_info += f"[{self.literal_suffix}]"
        return f"Token({self.type}, '{self.lexeme}'{type_info}, line={self.line}, col={self.column})"

    def is_numeric(self) -> bool:
        """
        Verifica si el token es un número.
        """
        return self.type == TokenType.NUMBER

    def is_literal(self) -> bool:
        """
        Verifica si el token es un literal (número, string, char, bool).
        """
        return self.type in [
            TokenType.NUMBER,
            TokenType.STRING,
            TokenType.CHAR,
            TokenType.TRUE,
            TokenType.FALSE
        ]

    def has_type_suffix(self) -> bool:
        """
        Verifica si el token tiene un sufijo de tipo.
        """
        return self.literal_suffix is not None 