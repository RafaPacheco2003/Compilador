from dataclasses import dataclass
from typing import Optional, Union, Any
import struct

@dataclass
class DataType:
    """
    Clase que representa un tipo de dato en el lenguaje.
    Implementa verificación de rangos y conversiones similares a Rust.
    """
    name: str
    size: int  # tamaño en bits
    signed: bool  # True para tipos con signo, False para unsigned
    is_float: bool  # True para tipos flotantes
    min_value: Union[int, float]
    max_value: Union[int, float]

    @staticmethod
    def i8() -> 'DataType':
        return DataType("i8", 8, True, False, -128, 127)

    @staticmethod
    def i16() -> 'DataType':
        return DataType("i16", 16, True, False, -32768, 32767)

    @staticmethod
    def i32() -> 'DataType':
        return DataType("i32", 32, True, False, -2147483648, 2147483647)

    @staticmethod
    def i64() -> 'DataType':
        return DataType("i64", 64, True, False, -9223372036854775808, 9223372036854775807)

    @staticmethod
    def u8() -> 'DataType':
        return DataType("u8", 8, False, False, 0, 255)

    @staticmethod
    def u16() -> 'DataType':
        return DataType("u16", 16, False, False, 0, 65535)

    @staticmethod
    def u32() -> 'DataType':
        return DataType("u32", 32, False, False, 0, 4294967295)

    @staticmethod
    def u64() -> 'DataType':
        return DataType("u64", 64, False, False, 0, 18446744073709551615)

    @staticmethod
    def f32() -> 'DataType':
        return DataType("f32", 32, True, True, float('-inf'), float('inf'))

    @staticmethod
    def f64() -> 'DataType':
        return DataType("f64", 64, True, True, float('-inf'), float('inf'))

    @staticmethod
    def bool() -> 'DataType':
        return DataType("bool", 1, False, False, 0, 1)

    @staticmethod
    def char() -> 'DataType':
        return DataType("char", 32, False, False, 0, 0x10FFFF)  # Máximo valor Unicode

    def check_value(self, value: Any) -> bool:
        """
        Verifica si un valor está dentro del rango válido para este tipo.
        """
        if isinstance(value, bool) and self.name == "bool":
            return True
        
        if isinstance(value, str):
            if self.name == "char":
                return len(value) == 1 and ord(value) <= self.max_value
            return True  # Para strings normales
            
        if isinstance(value, (int, float)):
            return self.min_value <= value <= self.max_value
            
        return False

    def cast_value(self, value: Any) -> Optional[Any]:
        """
        Intenta convertir un valor al tipo correcto, retorna None si no es posible.
        """
        try:
            if self.name == "bool":
                return bool(value)
                
            if self.name == "char":
                if isinstance(value, str) and len(value) == 1:
                    return value
                return None
                
            if self.is_float:
                value = float(value)
            else:
                value = int(float(value))
                
            if self.check_value(value):
                return value
                
            return None
        except (ValueError, TypeError):
            return None

    def get_literal_suffix(self) -> str:
        """
        Retorna el sufijo que se usa en los literales de este tipo.
        Por ejemplo: 42i32, 3.14f64
        """
        if self.is_float:
            return f"f{self.size}"
        if not self.signed:
            return f"u{self.size}"
        return f"i{self.size}"

    def __str__(self) -> str:
        return self.name 