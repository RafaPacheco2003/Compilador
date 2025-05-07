from typing import List, Dict, Optional
from .semantic_analyzer_interface import SemanticAnalyzerInterface
from .semantic_error import SemanticError, SemanticErrorHandler
from ..tokens.token import Token
from ..tokens.token_type import TokenType
from ..types.data_type import DataType, TYPES
from .error_handler import ErrorHandler

class SemanticAnalyzer(SemanticAnalyzerInterface):
    """
    Implementación principal del analizador semántico.
    Sigue los principios SOLID:
    - Single Responsibility (SRP): Se encarga únicamente del análisis semántico
    - Open/Closed (OCP): Extensible para nuevos tipos y reglas semánticas
    - Liskov Substitution (LSP): Implementa correctamente la interfaz
    - Interface Segregation (ISP): Usa interfaces específicas
    - Dependency Inversion (DIP): Depende de abstracciones, no implementaciones
    """
    
    def __init__(self):
        """
        Inicializa el analizador semántico.
        Configura el manejador de errores y la tabla de símbolos.
        """
        self.error_handler = ErrorHandler()
        self.symbol_table: Dict[str, DataType] = {}  # Tabla de símbolos simple
        
    def analyze(self, tokens: List[Token]) -> List[Token]:
        """
        Realiza el análisis semántico completo de una lista de tokens.
        
        Args:
            tokens: Lista de tokens a analizar
            
        Returns:
            List[Token]: Lista de tokens con información semántica añadida
        """
        self.error_handler.clear()
        self.symbol_table.clear()  # Clear symbol table at start of analysis
        i = 0
        
        while i < len(tokens):
            # Analizar declaraciones de variables
            if tokens[i].type == TokenType.LET:
                if i + 3 >= len(tokens):
                    self.error_handler.add_error(SemanticError(
                        "Declaración de variable incompleta",
                        tokens[i]
                    ))
                    break
                    
                identifier = tokens[i + 1]
                type_token = None
                value_token = None
                
                # Verificar si hay tipo explícito
                if i + 2 < len(tokens) and tokens[i + 2].type == TokenType.COLON:
                    if i + 5 >= len(tokens):
                        self.error_handler.add_error(SemanticError(
                            "Declaración de variable incompleta",
                            tokens[i]
                        ))
                        break
                    type_token = tokens[i + 3]
                    value_token = tokens[i + 5]
                    i = self._analyze_variable_declaration(tokens, i)
                else:
                    value_token = tokens[i + 3]
                    i = self._analyze_variable_declaration(tokens, i)
                    
            # Analizar asignaciones
            elif tokens[i].type == TokenType.IDENTIFIER and i + 1 < len(tokens) and tokens[i + 1].type == TokenType.EQUAL:
                i = self._analyze_assignment(tokens, i)
                
            # Analizar expresiones
            elif tokens[i].is_literal() or tokens[i].type == TokenType.IDENTIFIER:
                i = self._analyze_expression(tokens, i)
            else:
                i += 1
                
        return tokens
        
    def check_type_compatibility(self, value_token: Token, target_type: DataType) -> bool:
        """
        Verifica si un valor es compatible con un tipo objetivo.
        
        Args:
            value_token: Token del valor
            target_type: Tipo objetivo
            
        Returns:
            bool: True si el valor es compatible con el tipo
        """
        # Si el valor ya tiene un tipo asignado, verificar compatibilidad
        if value_token.data_type:
            source_type = value_token.data_type
            value = value_token.literal
            
            # Mismo tipo
            if source_type.name == target_type.name:
                return True
                
            # Conversiones numéricas
            if source_type.is_numeric and target_type.is_numeric:
                # No permitir conversión de float a int
                if source_type.is_float and not target_type.is_float:
                    self.error_handler.add_error(SemanticError(
                        f"No se puede convertir de {source_type.name} a {target_type.name} sin conversión explícita",
                        value_token
                    ))
                    return False
                    
                # Si el tipo origen es más grande que el destino, verificar el valor
                if source_type.size > target_type.size:
                    if isinstance(value, (int, float)):
                        if value < target_type.min_value or value > target_type.max_value:
                            self.error_handler.add_error(SemanticError(
                                f"El valor {value} está fuera del rango permitido para {target_type.name}",
                                value_token,
                                f"Rango permitido: [{target_type.min_value}, {target_type.max_value}]"
                            ))
                            return False
                            
                # Verificar signos
                if not target_type.is_signed and source_type.is_signed:
                    if isinstance(value, (int, float)) and value < 0:
                        self.error_handler.add_error(SemanticError(
                            f"No se puede convertir un valor negativo a {target_type.name}",
                            value_token
                        ))
                        return False
                        
                return True
                
            self.error_handler.add_error(SemanticError(
                f"No se puede convertir de {source_type.name} a {target_type.name}",
                value_token
            ))
            return False
            
        # Para valores literales, verificar el tipo primero
        if value_token.is_literal() and value_token.literal is not None:
            value = value_token.literal
            
            # Verificar tipo básico primero
            if target_type.name == 'bool':
                return isinstance(value, bool) or value in [0, 1]
            elif target_type.name == 'char':
                return isinstance(value, str) and len(value) == 1
            elif target_type.name == 'string':
                return isinstance(value, str)
                
            # Para tipos numéricos, verificar que el valor sea numérico
            if target_type.is_numeric:
                if not isinstance(value, (int, float)):
                    self.error_handler.add_error(SemanticError(
                        f"Se esperaba un valor numérico para el tipo {target_type.name}",
                        value_token
                    ))
                    return False
                    
                # Verificar signo para tipos unsigned
                if not target_type.is_signed and value < 0:
                    self.error_handler.add_error(SemanticError(
                        f"No se puede asignar un valor negativo al tipo sin signo {target_type.name}",
                        value_token
                    ))
                    return False
                    
                # Verificar rango
                if value < target_type.min_value or value > target_type.max_value:
                    self.error_handler.add_error(SemanticError(
                        f"Valor {value} fuera del rango permitido para {target_type.name}",
                        value_token,
                        f"Rango permitido: [{target_type.min_value}, {target_type.max_value}]"
                    ))
                    return False
                    
                return True
            else:
                self.error_handler.add_error(SemanticError(
                    f"Tipo de dato no soportado: {target_type.name}",
                    value_token
                ))
                return False
                
        return False
        
    def validate_declaration(self, identifier: Token, type_token: Token, value_token: Token) -> bool:
        """
        Valida una declaración de variable.
        
        Args:
            identifier: Token del identificador
            type_token: Token del tipo de dato
            value_token: Token del valor asignado
            
        Returns:
            bool: True si la declaración es válida
        """
        # Verificar si la variable ya está declarada
        if identifier.lexeme in self.symbol_table:
            self.error_handler.add_error(SemanticError(
                f"Variable '{identifier.lexeme}' ya declarada",
                identifier
            ))
            return False
            
        # Obtener el tipo declarado
        declared_type = self._get_data_type(type_token)
        if not declared_type:
            self.error_handler.add_error(SemanticError(
                f"Tipo de dato '{type_token.lexeme}' no válido",
                type_token
            ))
            return False
            
        # Si el valor es una expresión, analizarla primero
        if value_token.type == TokenType.IDENTIFIER:
            # Si es un identificador, verificar que esté declarado y obtener su tipo
            if value_token.lexeme not in self.symbol_table:
                self.error_handler.add_error(SemanticError(
                    f"Variable '{value_token.lexeme}' no declarada",
                    value_token
                ))
                return False
            value_type = self.symbol_table[value_token.lexeme]
            value_token.data_type = value_type
            
            # Verificar compatibilidad de tipos
            if not self.check_type_compatibility(value_token, declared_type):
                return False
                
        elif value_token.is_literal():
            # Para literales, verificar el rango directamente
            if not declared_type.check_value(value_token.literal):
                self.error_handler.add_error(SemanticError(
                    f"Valor {value_token.literal} fuera del rango para tipo {declared_type.name}",
                    value_token,
                    f"Rango permitido: [{declared_type.min_value}, {declared_type.max_value}]"
                ))
                return False
                
        # Agregar a la tabla de símbolos
        self.symbol_table[identifier.lexeme] = declared_type
        identifier.data_type = declared_type
        return True
        
    def validate_operation(self, left: Token, operator: Token, right: Token) -> Optional[DataType]:
        """
        Valida una operación entre dos tokens y determina el tipo resultante.
        
        Args:
            left: Token del operando izquierdo
            operator: Token del operador
            right: Token del operando derecho
            
        Returns:
            Optional[DataType]: Tipo resultante o None si la operación no es válida
        """
        # Obtener tipos de los operandos
        left_type = left.data_type or self._get_token_type(left)
        right_type = right.data_type or self._get_token_type(right)
        
        if not left_type or not right_type:
            self.error_handler.add_error(SemanticError(
                "No se puede determinar el tipo de uno de los operandos",
                operator
            ))
            return None
            
        # Validar operaciones según los tipos
        if operator.type == TokenType.PLUS:
            # Si uno de los operandos es string, ambos deben ser string
            if left_type.name == "string" or right_type.name == "string":
                if left_type.name != "string" or right_type.name != "string":
                    self.error_handler.add_error(SemanticError(
                        "La concatenación solo es válida entre strings",
                        operator,
                        f"No se puede concatenar {left_type.name} con {right_type.name}"
                    ))
                    return None
                return TYPES['string']
                
            # Operaciones numéricas
            if not (left_type.is_numeric and right_type.is_numeric):
                self.error_handler.add_error(SemanticError(
                    "Operación no válida entre estos tipos",
                    operator,
                    f"No se puede sumar {left_type.name} con {right_type.name}"
                ))
                return None
                
            # Si alguno es flotante, el resultado es flotante
            if left_type.is_float or right_type.is_float:
                return TYPES['f64'] if max(left_type.size, right_type.size) > 32 else TYPES['f32']
                
            # Entre enteros
            max_size = max(left_type.size, right_type.size)
            if left_type.is_signed or right_type.is_signed:
                return TYPES['i64'] if max_size > 32 else TYPES['i32']
            return TYPES['u64'] if max_size > 32 else TYPES['u32']
            
        # Otras operaciones aritméticas
        elif operator.type in [TokenType.MINUS, TokenType.STAR, TokenType.SLASH]:
            # No permitir operaciones aritméticas con strings
            if left_type.name == "string" or right_type.name == "string":
                self.error_handler.add_error(SemanticError(
                    "No se pueden realizar operaciones aritméticas con strings",
                    operator,
                    f"No se puede operar {left_type.name} con {right_type.name}"
                ))
                return None
                
            if not (left_type.is_numeric and right_type.is_numeric):
                self.error_handler.add_error(SemanticError(
                    "Operación aritmética no válida entre estos tipos",
                    operator,
                    f"No se puede operar {left_type.name} con {right_type.name}"
                ))
                return None
                
            # Si alguno es flotante, el resultado es flotante
            if left_type.is_float or right_type.is_float:
                return TYPES['f64'] if max(left_type.size, right_type.size) > 32 else TYPES['f32']
                
            # Entre enteros
            max_size = max(left_type.size, right_type.size)
            if left_type.is_signed or right_type.is_signed:
                return TYPES['i64'] if max_size > 32 else TYPES['i32']
            return TYPES['u64'] if max_size > 32 else TYPES['u32']
            
        # Operaciones de comparación
        elif operator.type in [TokenType.EQUAL_EQUAL, TokenType.BANG_EQUAL]:
            if left_type.name != right_type.name:
                self.error_handler.add_error(SemanticError(
                    "No se pueden comparar tipos diferentes",
                    operator,
                    f"No se puede comparar {left_type.name} con {right_type.name}"
                ))
                return None
            return TYPES['bool']
            
        elif operator.type in [TokenType.LESS, TokenType.LESS_EQUAL,
                             TokenType.GREATER, TokenType.GREATER_EQUAL]:
            if not (left_type.is_numeric and right_type.is_numeric):
                self.error_handler.add_error(SemanticError(
                    "Comparación no válida entre estos tipos",
                    operator,
                    f"No se puede comparar {left_type.name} con {right_type.name}"
                ))
                return None
            return TYPES['bool']
            
        self.error_handler.add_error(SemanticError(
            f"Operador '{operator.lexeme}' no válido para los tipos dados",
            operator
        ))
        return None
        
    def _analyze_variable_declaration(self, tokens: List[Token], start_index: int) -> int:
        """
        Analiza una declaración de variable.
        """
        # Verificar formato básico: let identifier
        if start_index + 1 >= len(tokens) or tokens[start_index + 1].type != TokenType.IDENTIFIER:
            self.error_handler.add_error(SemanticError(
                "Se esperaba un identificador después de 'let'",
                tokens[start_index]
            ))
            return start_index + 1
            
        identifier = tokens[start_index + 1]
        
        # Verificar si la variable ya está declarada
        if identifier.lexeme in self.symbol_table:
            self.error_handler.add_error(SemanticError(
                f"Variable '{identifier.lexeme}' ya declarada",
                identifier
            ))
            return start_index + 2
            
        # Verificar si hay tipo explícito: let identifier: type
        if start_index + 2 < len(tokens) and tokens[start_index + 2].type == TokenType.COLON:
            if start_index + 3 >= len(tokens):
                self.error_handler.add_error(SemanticError(
                    "Se esperaba un tipo después de ':'",
                    tokens[start_index + 2]
                ))
                return start_index + 3
                
            type_token = tokens[start_index + 3]
            declared_type = self._get_data_type(type_token)
            if not declared_type:
                self.error_handler.add_error(SemanticError(
                    f"Tipo de dato '{type_token.lexeme}' no válido",
                    type_token
                ))
                return start_index + 4
                
            # Verificar asignación: let identifier: type = value
            if start_index + 4 >= len(tokens) or tokens[start_index + 4].type != TokenType.EQUAL:
                self.error_handler.add_error(SemanticError(
                    "Se esperaba '=' después del tipo",
                    type_token
                ))
                return start_index + 5
                
            if start_index + 5 >= len(tokens):
                self.error_handler.add_error(SemanticError(
                    "Se esperaba un valor después de '='",
                    tokens[start_index + 4]
                ))
                return start_index + 6
                
            value_token = tokens[start_index + 5]
            
            # Si el valor es un identificador (variable)
            if value_token.type == TokenType.IDENTIFIER:
                if value_token.lexeme not in self.symbol_table:
                    self.error_handler.add_error(SemanticError(
                        f"Variable '{value_token.lexeme}' no declarada",
                        value_token
                    ))
                    return start_index + 6
                    
                source_type = self.symbol_table[value_token.lexeme]
                value_token.data_type = source_type
                
                # Verificar compatibilidad de tipos y rangos
                if not self._check_type_compatibility(source_type, declared_type, value_token):
                    return start_index + 6
                    
            # Si es un valor literal
            elif value_token.is_literal():
                if declared_type.name == "string" and not isinstance(value_token.literal, str):
                    self.error_handler.add_error(SemanticError(
                        f"Se esperaba un string pero se encontró {type(value_token.literal).__name__}",
                        value_token
                    ))
                    return start_index + 6
                    
                if not declared_type.check_value(value_token.literal):
                    self.error_handler.add_error(SemanticError(
                        f"Valor {value_token.literal} fuera del rango permitido para {declared_type.name}",
                        value_token,
                        f"Rango permitido: [{declared_type.min_value}, {declared_type.max_value}]"
                    ))
                    return start_index + 6
                    
            # Agregar a la tabla de símbolos
            self.symbol_table[identifier.lexeme] = declared_type
            identifier.data_type = declared_type
            value_token.data_type = declared_type
            return start_index + 6
            
        # Si no hay tipo explícito, inferir del valor
        if start_index + 2 >= len(tokens) or tokens[start_index + 2].type != TokenType.EQUAL:
            self.error_handler.add_error(SemanticError(
                "Se esperaba '=' después del identificador",
                identifier
            ))
            return start_index + 3
            
        if start_index + 3 >= len(tokens):
            self.error_handler.add_error(SemanticError(
                "Se esperaba un valor después de '='",
                tokens[start_index + 2]
            ))
            return start_index + 4
            
        value_token = tokens[start_index + 3]
        inferred_type = self._get_token_type(value_token)
        
        if not inferred_type:
            self.error_handler.add_error(SemanticError(
                "No se puede inferir el tipo del valor",
                value_token
            ))
            return start_index + 4
            
        # Agregar a la tabla de símbolos
        self.symbol_table[identifier.lexeme] = inferred_type
        identifier.data_type = inferred_type
        value_token.data_type = inferred_type
        return start_index + 4
        
    def _infer_type(self, token: Token) -> Optional[DataType]:
        """
        Infiere el tipo de un token.
        
        Args:
            token (Token): Token del cual inferir el tipo.
            
        Returns:
            Optional[DataType]: Tipo inferido o None si no se puede inferir.
        """
        if token.type == TokenType.NUMBER:
            if isinstance(token.literal, float):
                return TYPES['f64']
            return TYPES['i32']
        elif token.type == TokenType.STRING:
            return TYPES['string']
        elif token.type == TokenType.CHAR:
            return TYPES['char']
        elif token.type in [TokenType.TRUE, TokenType.FALSE]:
            return TYPES['bool']
        elif token.type == TokenType.IDENTIFIER:
            return self.symbol_table.get(token.lexeme)
        return None
        
    def _analyze_assignment(self, tokens: List[Token], start_index: int) -> int:
        """
        Analiza una asignación de variable.
        
        Args:
            tokens: Lista completa de tokens
            start_index: Índice donde comienza la asignación
            
        Returns:
            int: Índice siguiente al final de la asignación
        """
        identifier = tokens[start_index]
        value_token = tokens[start_index + 2]
        
        if identifier.lexeme not in self.symbol_table:
            self.error_handler.add_error(SemanticError(
                f"Variable '{identifier.lexeme}' no declarada",
                identifier
            ))
            return start_index + 3
            
        expected_type = self.symbol_table[identifier.lexeme]
        
        # Si el valor es una expresión, analizarla primero
        if start_index + 4 < len(tokens) and tokens[start_index + 3].type in [
            TokenType.PLUS, TokenType.MINUS, TokenType.STAR, TokenType.SLASH
        ]:
            self._analyze_expression(tokens, start_index + 2)
            
        # Verificar compatibilidad de tipos
        if not self.check_type_compatibility(value_token, expected_type):
            return start_index + 3
            
        return start_index + 3
        
    def _analyze_expression(self, tokens: List[Token], start_index: int) -> int:
        """
        Analiza una expresión.
        
        Args:
            tokens: Lista de tokens
            start_index: Índice donde comienza la expresión
            
        Returns:
            int: Índice siguiente al final de la expresión
        """
        i = start_index
        left_token = None
        
        while i < len(tokens) and tokens[i].type != TokenType.SEMICOLON:
            current_token = tokens[i]
            
            # Si es un identificador, verificar que esté declarado
            if current_token.type == TokenType.IDENTIFIER:
                if current_token.lexeme not in self.symbol_table:
                    self.error_handler.add_error(SemanticError(
                        f"Variable '{current_token.lexeme}' no declarada",
                        current_token
                    ))
                    return i + 1
                current_token.data_type = self.symbol_table[current_token.lexeme]
                if not left_token:
                    left_token = current_token
                
            # Si es un literal, inferir su tipo
            elif current_token.is_literal():
                current_token.data_type = self._get_token_type(current_token)
                if not left_token:
                    left_token = current_token
                
            # Si es un operador, validar la operación
            elif current_token.type in [TokenType.PLUS, TokenType.MINUS, TokenType.STAR, TokenType.SLASH]:
                if not left_token:
                    self.error_handler.add_error(SemanticError(
                        "Operador sin operando izquierdo",
                        current_token
                    ))
                    return i + 1
                    
                if i + 1 >= len(tokens):
                    self.error_handler.add_error(SemanticError(
                        "Expresión incompleta",
                        current_token
                    ))
                    return i + 1
                    
                # Obtener el operando derecho
                right_token = tokens[i + 1]
                if right_token.type == TokenType.IDENTIFIER:
                    if right_token.lexeme not in self.symbol_table:
                        self.error_handler.add_error(SemanticError(
                            f"Variable '{right_token.lexeme}' no declarada",
                            right_token
                        ))
                        return i + 2
                    right_token.data_type = self.symbol_table[right_token.lexeme]
                elif right_token.is_literal():
                    right_token.data_type = self._get_token_type(right_token)
                
                # Validar la operación
                result_type = self.validate_operation(left_token, current_token, right_token)
                if not result_type:
                    return i + 2
                    
                # Crear un nuevo token que representa el resultado de la operación
                left_token = Token(
                    type=TokenType.NUMBER if result_type.is_numeric else TokenType.STRING,
                    lexeme="",
                    literal=None,
                    line=left_token.line,
                    column=left_token.column,
                    data_type=result_type
                )
                
                i += 1
                
            i += 1
            
        return i
        
    def _get_data_type(self, type_token: Token) -> Optional[DataType]:
        """
        Convierte un token de tipo en un objeto DataType.
        
        Args:
            type_token (Token): Token que representa el tipo.
            
        Returns:
            Optional[DataType]: Objeto DataType correspondiente, o None si no es válido.
        """
        return TYPES.get(type_token.lexeme)
        
    def _get_token_type(self, token: Token) -> Optional[DataType]:
        """
        Obtiene el tipo de dato de un token.
        
        Args:
            token: Token del cual obtener el tipo
            
        Returns:
            Optional[DataType]: Tipo de dato del token, o None si no se puede determinar
        """
        # Si el token ya tiene un tipo asignado, usarlo
        if token.data_type:
            return token.data_type
            
        # Para identificadores, buscar en la tabla de símbolos
        if token.type == TokenType.IDENTIFIER:
            return self.symbol_table.get(token.lexeme)
            
        # Para literales, inferir el tipo
        if token.is_literal():
            if token.type == TokenType.NUMBER:
                if isinstance(token.literal, float):
                    return TYPES['f64']
                # Para enteros, inferir basado en el valor
                value = token.literal
                if value >= 0:
                    if value <= 127:
                        return TYPES['i8']
                    elif value <= 255:
                        return TYPES['u8']
                    elif value <= 32767:
                        return TYPES['i16']
                    elif value <= 65535:
                        return TYPES['u16']
                    elif value <= 2147483647:
                        return TYPES['i32']
                    elif value <= 4294967295:
                        return TYPES['u32']
                    elif value <= 9223372036854775807:
                        return TYPES['i64']
                    else:
                        return TYPES['u64']
                else:
                    if value >= -128:
                        return TYPES['i8']
                    elif value >= -32768:
                        return TYPES['i16']
                    elif value >= -2147483648:
                        return TYPES['i32']
                    else:
                        return TYPES['i64']
            elif token.type == TokenType.STRING:
                return TYPES['string']
            elif token.type == TokenType.CHAR:
                return TYPES['char']
            elif token.type in [TokenType.TRUE, TokenType.FALSE]:
                return TYPES['bool']
                
        return None
        
    def _check_type_compatibility(self, value_type: DataType, target_type: DataType, token: Token) -> bool:
        """Verifica la compatibilidad entre tipos."""
        # Si son el mismo tipo, son compatibles
        if value_type == target_type:
            return True
            
        # Verificar conversiones numéricas
        if value_type.is_numeric and target_type.is_numeric:
            # No permitir conversión de float a int sin conversión explícita
            if value_type.is_float and not target_type.is_float:
                self.error_handler.add_error(SemanticError(
                    f"No se puede convertir de {value_type.name} a {target_type.name} sin conversión explícita",
                    token
                ))
                return False
                
            # Verificar rangos para enteros
            if not value_type.is_float and not target_type.is_float:
                try:
                    value = token.literal
                    if isinstance(value, (int, float)):
                        if value < target_type.min_value or value > target_type.max_value:
                            self.error_handler.add_error(SemanticError(
                                f"El valor {value} está fuera del rango permitido para {target_type.name}",
                                token,
                                f"Rango permitido: [{target_type.min_value}, {target_type.max_value}]"
                            ))
                            return False
                except (TypeError, AttributeError):
                    pass
                    
            # Verificar signos
            if not target_type.is_signed and value_type.is_signed:
                try:
                    value = token.literal
                    if isinstance(value, (int, float)) and value < 0:
                        self.error_handler.add_error(SemanticError(
                            f"No se puede asignar un valor negativo a un tipo sin signo {target_type.name}",
                            token
                        ))
                        return False
                except (TypeError, AttributeError):
                    pass
                    
            return True
            
        # Verificar operaciones con strings
        if value_type.name == "string" or target_type.name == "string":
            if value_type.name != target_type.name:
                self.error_handler.add_error(SemanticError(
                    "No se pueden mezclar strings con otros tipos",
                    token,
                    f"No se puede convertir de {value_type.name} a {target_type.name}"
                ))
                return False
            return True
            
        self.error_handler.add_error(SemanticError(
            f"No se puede convertir de {value_type.name} a {target_type.name}",
            token
        ))
        return False

    def _check_explicit_conversion(self, value_type: DataType, target_type: DataType, token: Token) -> bool:
        """Verifica si una conversión explícita es válida."""
        # Permitir conversiones entre tipos numéricos
        if value_type.is_numeric and target_type.is_numeric:
            value = token.literal
            
            # Verificar rangos
            if value < target_type.min_value or value > target_type.max_value:
                self.error_handler.add_error(SemanticError(
                    f"El valor {value} está fuera del rango permitido para {target_type.name} ({target_type.min_value} a {target_type.max_value})",
                    token
                ))
                return False
                
            # Verificar signos para enteros
            if not value_type.is_float and not target_type.is_float:
                if not value_type.is_signed and target_type.is_signed:
                    if value < 0:
                        self.error_handler.add_error(SemanticError(
                            f"No se puede convertir un valor negativo a {target_type.name}",
                            token
                        ))
                        return False
                        
            return True
            
        self.error_handler.add_error(SemanticError(
            f"No se puede convertir explícitamente de {value_type.name} a {target_type.name}",
            token
        ))
        return False 