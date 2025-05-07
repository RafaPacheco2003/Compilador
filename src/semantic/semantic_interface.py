# src/semantic/semantic_interface.py
from abc import ABC, abstractmethod
from typing import List
from ..tokens.token import Token
from ..types.data_type import DataType

class SemanticAnalyzerInterface(ABC):
    
    
    @abstractmethod
    def analyze(self, tokens: List[Token]) -> bool:
        """Analiza semánticamente la lista de tokens"""
        pass


class TypeCheckerInterface(ABC):
    @abstractmethod
    def check_type_compatibility(self, value: Token, expected_type: DataType) -> bool:
        """Verifica la compatibilidad de tipos"""
        pass

class ScopeManagerInterface(ABC):
    @abstractmethod
    def enter_scope(self) -> None:
        """Entra en un nuevo ámbito"""
        pass

    @abstractmethod
    def exit_scope(self) -> None:
        """Sale del ámbito actual"""
        pass

    @abstractmethod
    def declare_variable(self, name: str, data_type: DataType) -> None:
        """Declara una variable en el ámbito actual"""
        pass