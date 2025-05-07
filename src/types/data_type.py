from dataclasses import dataclass
from typing import Optional, Union, Any
import math

class DataType:
    def __init__(self, name: str, size: int, is_signed: bool = True, is_float: bool = False,
                 min_value: Union[int, float] = None, max_value: Union[int, float] = None):
        self.name = name
        self.size = size
        self.is_signed = is_signed
        self.is_float = is_float
        self.min_value = min_value
        self.max_value = max_value
        self.is_numeric = not name in ['bool', 'char', 'string']

    def __eq__(self, other: 'DataType') -> bool:
        if other is None:
            return False
        return (self.name == other.name and
                self.size == other.size and
                self.is_signed == other.is_signed and
                self.is_float == other.is_float)

    def check_value(self, value) -> bool:
        """Verifica si un valor está dentro del rango permitido para este tipo."""
        if not self.is_numeric:
            if self.name == 'bool':
                return isinstance(value, bool) or value in [0, 1]
            if self.name == 'char':
                return isinstance(value, str) and len(value) == 1
            if self.name == 'string':
                return isinstance(value, str)
            return False
            
        try:
            # Convertir strings a números si es posible
            if isinstance(value, str):
                value = float(value) if self.is_float else int(value)
                
            # Para tipos sin signo, verificar que no sea negativo
            if not self.is_signed and value < 0:
                return False
                
            # Verificar el rango
            if self.min_value is not None and value < self.min_value:
                return False
            if self.max_value is not None and value > self.max_value:
                return False
                
            return True
        except (ValueError, TypeError):
            return False

    def is_numeric(self) -> bool:
        """
        Verifica si el tipo es numérico (entero o flotante).
        """
        return not self.name in ["bool", "char", "string"]

    def can_convert_from(self, other: 'DataType') -> bool:
        """Verifica si se puede convertir desde otro tipo."""
        if not self.is_numeric or not other.is_numeric:
            return self.name == other.name
            
        # Permitir conversión a tipo más grande
        if self.is_float and other.is_float:
            return self.size >= other.size
            
        # Permitir conversión de entero a float
        if self.is_float and not other.is_float:
            return True
            
        # Entre enteros
        if not self.is_float and not other.is_float:
            if not self.is_signed and other.is_signed:
                return False
            return self.size >= other.size
            
        return False

    def get_operation_result(self, other: 'DataType', operator: str) -> Optional['DataType']:
        """
        Determina el tipo resultante de una operación entre dos tipos.
        Implementa reglas precisas para operaciones entre tipos.
        
        Args:
            other (DataType): Segundo tipo en la operación
            operator (str): Operador ('+', '-', '*', '/', '%')
            
        Returns:
            Optional[DataType]: Tipo resultante o None si la operación no es válida
        """
        # Operaciones con strings
        if self.name == "string" or other.name == "string":
            if operator == "+" and self.name == "string" and other.name == "string":
                return DataType.string()
            return None

        # Operaciones numéricas
        if not (self.is_numeric() and other.is_numeric()):
            return None
            
        if operator in ['+', '-', '*', '/', '%']:
            # División siempre produce float
            if operator == '/':
                return DataType.f64() if self.size > 32 or other.size > 32 else DataType.f32()
                
            # Módulo solo entre enteros
            if operator == '%':
                if self.is_float or other.is_float:
                    return None
                # Usar el tipo más grande
                max_size = max(self.size, other.size)
                if self.is_signed or other.is_signed:
                    return DataType.i64() if max_size > 32 else DataType.i32()
                return DataType.u64() if max_size > 32 else DataType.u32()
                
            # Otras operaciones aritméticas
            if self.is_float or other.is_float:
                return DataType.f64() if max(self.size, other.size) > 32 else DataType.f32()
                
            # Entre enteros
            max_size = max(self.size, other.size)
            if self.is_signed or other.is_signed:
                return DataType.i64() if max_size > 32 else DataType.i32()
            return DataType.u64() if max_size > 32 else DataType.u32()

        return None

    def cast_value(self, value: Any) -> Optional[Any]:
        """
        Intenta convertir un valor al tipo correcto.
        Implementa reglas estrictas de conversión de valores.
        
        Args:
            value: Valor a convertir
            
        Returns:
            Optional[Any]: Valor convertido o None si la conversión no es válida
        """
        try:
            if self.name == "bool":
                if isinstance(value, bool):
                    return value
                return None
                
            if self.name == "char":
                if isinstance(value, str) and len(value) == 1:
                    return value
                if isinstance(value, int) and 0 <= value <= 0x10FFFF:
                    return chr(value)
                return None
                
            if self.name == "string":
                return str(value)
                
            if self.is_float:
                if isinstance(value, (int, float)):
                    float_val = float(value)
                    if self.min_value <= float_val <= self.max_value:
                        return float_val
                return None
                
            # Enteros
            if isinstance(value, (int, float)):
                int_val = int(float(value))
                if float(int_val) != float(value):  # Verificar pérdida de precisión
                    return None
                if self.min_value <= int_val <= self.max_value:
                    return int_val
                    
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
        if not self.is_signed:
            return f"u{self.size}"
        return f"i{self.size}"

    def __str__(self) -> str:
        return self.name 

# Definición de tipos básicos
TYPES = {
    'i8': DataType('i8', 1, True, False, -128, 127),
    'i16': DataType('i16', 2, True, False, -32768, 32767),
    'i32': DataType('i32', 4, True, False, -2147483648, 2147483647),
    'i64': DataType('i64', 8, True, False, -9223372036854775808, 9223372036854775807),
    'u8': DataType('u8', 1, False, False, 0, 255),
    'u16': DataType('u16', 2, False, False, 0, 65535),
    'u32': DataType('u32', 4, False, False, 0, 4294967295),
    'u64': DataType('u64', 8, False, False, 0, 18446744073709551615),
    'f32': DataType('f32', 4, True, True, float('-3.4e38'), float('3.4e38')),
    'f64': DataType('f64', 8, True, True, float('-1.8e308'), float('1.8e308')),
    'bool': DataType('bool', 1, False, False, 0, 1),
    'char': DataType('char', 1, False, False, 0, 255),
    'string': DataType('string', 0, False, False)
} 