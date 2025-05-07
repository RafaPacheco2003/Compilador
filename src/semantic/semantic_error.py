from dataclasses import dataclass
from typing import Optional
from ..tokens.token import Token

class SemanticError:
    def __init__(self, message: str, token: Token, details: str = ""):
        """
        Inicializa un error semántico.
        
        Args:
            message: Mensaje de error
            token: Token donde ocurrió el error
            details: Detalles adicionales del error (opcional)
        """
        self.message = message
        self.token = token
        self.details = details

    def __str__(self) -> str:
        """
        Convierte el error a string.
        
        Returns:
            str: Representación en string del error
        """
        error = f"Error semántico en línea {self.token.line}, columna {self.token.column}: {self.message}"
        if self.details:
            error += f"\nDetalles: {self.details}"
        return error

class SemanticErrorHandler:
    """
    Clase que maneja la colección y reporte de errores semánticos.
    Sigue el principio de Single Responsibility (SRP) de SOLID.
    """
    
    def __init__(self):
        """Inicializa el manejador de errores semánticos."""
        self.errors: list[SemanticError] = []
        
    def add_error(self, error: SemanticError) -> None:
        """
        Añade un nuevo error semántico a la lista.
        
        Args:
            error (SemanticError): Error semántico a añadir.
        """
        self.errors.append(error)
        
    def has_errors(self) -> bool:
        """
        Verifica si hay errores semánticos.
        
        Returns:
            bool: True si hay errores, False en caso contrario.
        """
        return len(self.errors) > 0
        
    def get_errors(self) -> list[SemanticError]:
        """
        Obtiene la lista de errores semánticos.
        
        Returns:
            list[SemanticError]: Lista de errores semánticos.
        """
        return self.errors
        
    def clear_errors(self) -> None:
        """Limpia la lista de errores semánticos."""
        self.errors.clear()
        
    def report_errors(self) -> str:
        """
        Genera un reporte de todos los errores semánticos.
        
        Returns:
            str: Reporte formateado de errores.
        """
        if not self.has_errors():
            return "No se encontraron errores semánticos."
            
        return "\n".join(str(error) for error in self.errors) 