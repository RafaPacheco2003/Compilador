from abc import ABC, abstractmethod
from typing import List
from ..tokens.token import Token

class LexerInterface(ABC):
    """
    Interfaz que define el contrato para implementaciones de analizadores léxicos.
    Siguiendo el principio Interface Segregation, esta interfaz define solo los métodos
    esenciales que debe implementar un analizador léxico.
    """
    
    @abstractmethod
    def tokenize(self) -> List[Token]:
        """
        Analiza el texto fuente completo y retorna una lista de tokens.
        
        Returns:
            List[Token]: Lista de tokens encontrados en el texto fuente.
        """
        pass
    
    @abstractmethod
    def next_token(self) -> Token:
        """
        Obtiene el siguiente token del texto fuente.
        
        Returns:
            Token: El siguiente token encontrado.
        """
        pass
    
    @abstractmethod
    def peek(self) -> Token:
        """
        Mira el siguiente token sin consumirlo.
        
        Returns:
            Token: El siguiente token sin consumirlo.
        """
        pass 