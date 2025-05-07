from abc import ABC, abstractmethod
from typing import List
from ..tokens.token import Token
from ..types.data_type import DataType

class SemanticAnalyzerInterface(ABC):
    """
    Interfaz base para el analizador semántico.
    Define los métodos que debe implementar cualquier analizador semántico.
    
    Esta interfaz sigue el principio de Interface Segregation (ISP) de SOLID,
    proporcionando métodos específicos para cada tipo de análisis semántico.
    """
    
    @abstractmethod
    def analyze(self, tokens: List[Token]) -> List[Token]:
        """
        Realiza el análisis semántico completo de una lista de tokens.
        
        Args:
            tokens (List[Token]): Lista de tokens a analizar.
            
        Returns:
            List[Token]: Lista de tokens con información semántica añadida.
                        Los tokens pueden incluir errores semánticos.
        """
        pass
    
    @abstractmethod
    def check_type_compatibility(self, value: Token, expected_type: DataType) -> bool:
        """
        Verifica si un valor es compatible con un tipo de dato esperado.
        
        Args:
            value (Token): Token que contiene el valor a verificar.
            expected_type (DataType): Tipo de dato esperado.
            
        Returns:
            bool: True si el valor es compatible, False en caso contrario.
        """
        pass
    
    @abstractmethod
    def validate_declaration(self, identifier: Token, type_token: Token, value_token: Token) -> bool:
        """
        Valida una declaración de variable.
        
        Args:
            identifier (Token): Token del identificador.
            type_token (Token): Token del tipo de dato.
            value_token (Token): Token del valor asignado.
            
        Returns:
            bool: True si la declaración es válida, False en caso contrario.
        """
        pass
    
    @abstractmethod
    def validate_operation(self, left: Token, operator: Token, right: Token) -> DataType:
        """
        Valida una operación entre dos tokens y determina el tipo resultante.
        
        Args:
            left (Token): Token del operando izquierdo.
            operator (Token): Token del operador.
            right (Token): Token del operando derecho.
            
        Returns:
            DataType: Tipo de dato resultante de la operación.
        """
        pass 