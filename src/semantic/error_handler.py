from typing import List
from .semantic_error import SemanticError

class ErrorHandler:
    def __init__(self):
        self.errors: List[SemanticError] = []

    def add_error(self, error: SemanticError):
        """
        Agrega un error a la lista.
        
        Args:
            error: Error semántico a agregar
        """
        self.errors.append(error)

    def clear(self):
        """Limpia la lista de errores."""
        self.errors.clear()

    def has_errors(self) -> bool:
        """
        Verifica si hay errores.
        
        Returns:
            bool: True si hay errores
        """
        return len(self.errors) > 0 