from typing import List, Dict, Optional, Tuple
from .lexer_interface import LexerInterface
from ..tokens.token import Token
from ..tokens.token_type import TokenType
from ..readers.source_reader import SourceReader
from ..types.data_type import DataType
from ..types.data_type import TYPES

class Lexer(LexerInterface):
    """
    Implementación del analizador léxico.
    Esta clase implementa la interfaz LexerInterface y se encarga de convertir
    el código fuente en una secuencia de tokens.
    """

    def __init__(self, reader: SourceReader):
        """
        Inicializa el analizador léxico.
        
        Args:
            reader (SourceReader): El lector de código fuente.
        """
        self.reader = reader
        self.tokens: List[Token] = []
        self.current_token_index = 0
        self.start_position = 0
        self.source = reader.source
        
        # Diccionario de palabras reservadas
        self.keywords: Dict[str, TokenType] = {
            "let": TokenType.LET,
            "true": TokenType.TRUE,
            "false": TokenType.FALSE,
        }
        
        # Diccionario de tipos de datos
        self.type_keywords: Dict[str, TokenType] = {
            "i8": TokenType.TYPE_I8,
            "i16": TokenType.TYPE_I16,
            "i32": TokenType.TYPE_I32,
            "i64": TokenType.TYPE_I64,
            "u8": TokenType.TYPE_U8,
            "u16": TokenType.TYPE_U16,
            "u32": TokenType.TYPE_U32,
            "u64": TokenType.TYPE_U64,
            "f32": TokenType.TYPE_F32,
            "f64": TokenType.TYPE_F64,
            "bool": TokenType.TYPE_BOOL,
            "char": TokenType.TYPE_CHAR,
            "string": TokenType.TYPE_STRING,
        }

    def tokenize(self) -> List[Token]:
        """
        Analiza todo el código fuente y genera una lista de tokens.
        
        Returns:
            List[Token]: Lista de todos los tokens encontrados.
        """
        while not self.reader.is_at_end():
            # Marcar el inicio de un nuevo token
            self.start_position = self.reader.position
            self._scan_token()
            
        # Agregar token EOF al final
        line, column = self.reader.get_position_info()
        self.tokens.append(Token(TokenType.EOF, "", None, line, column))
        return self.tokens

    def next_token(self) -> Token:
        """
        Obtiene el siguiente token de la lista de tokens.
        
        Returns:
            Token: El siguiente token.
        """
        if self.current_token_index >= len(self.tokens):
            return self._create_token(TokenType.EOF, "", None)
        token = self.tokens[self.current_token_index]
        self.current_token_index += 1
        return token

    def peek(self) -> Token:
        """
        Mira el siguiente token sin consumirlo.
        
        Returns:
            Token: El siguiente token sin consumirlo.
        """
        if self.current_token_index >= len(self.tokens):
            return self._create_token(TokenType.EOF, "", None)
        return self.tokens[self.current_token_index]

    def _scan_token(self) -> None:
        """
        Escanea y procesa el siguiente token del código fuente.
        """
        char = self.reader.advance()

        # Procesar caracteres simples
        if char == '(': self._add_token(TokenType.LEFT_PAREN)
        elif char == ')': self._add_token(TokenType.RIGHT_PAREN)
        elif char == '{': self._add_token(TokenType.LEFT_BRACE)
        elif char == '}': self._add_token(TokenType.RIGHT_BRACE)
        elif char == '[': self._add_token(TokenType.LEFT_BRACKET)
        elif char == ']': self._add_token(TokenType.RIGHT_BRACKET)
        elif char == ',': self._add_token(TokenType.COMMA)
        elif char == '.': self._add_token(TokenType.DOT)
        elif char == '-': 
            if self._match('>'):
                self._add_token(TokenType.ARROW)
            elif self.reader.peek().isdigit():
                # Si el siguiente carácter es un dígito, procesar como número negativo
                self.start_position = self.reader.position - 1  # Incluir el signo menos
                self._number()
            else:
                self._add_token(TokenType.MINUS)
        elif char == '+': self._add_token(TokenType.PLUS)
        elif char == ';': self._add_token(TokenType.SEMICOLON)
        elif char == '*': self._add_token(TokenType.STAR)
        elif char == ':': 
            if self._match(':'):
                self._add_token(TokenType.DOUBLE_COLON)
            else:
                self._add_token(TokenType.COLON)
        elif char == '/': 
            if self._match('/'):
                # Comentario de una línea
                while self.reader.peek() != '\n' and not self.reader.is_at_end():
                    self.reader.advance()
            else:
                self._add_token(TokenType.SLASH)
        
        # Procesar operadores de dos caracteres
        elif char == '!': 
            self._add_token(TokenType.BANG_EQUAL if self._match('=') else TokenType.BANG)
        elif char == '=':
            if self._match('='):
                self._add_token(TokenType.EQUAL_EQUAL)
            elif self._match('>'):
                self._add_token(TokenType.FAT_ARROW)
            else:
                self._add_token(TokenType.EQUAL)
        elif char == '<':
            self._add_token(TokenType.LESS_EQUAL if self._match('=') else TokenType.LESS)
        elif char == '>':
            self._add_token(TokenType.GREATER_EQUAL if self._match('=') else TokenType.GREATER)
        elif char == '&' and self._match('&'):
            self._add_token(TokenType.AND)
        elif char == '|' and self._match('|'):
            self._add_token(TokenType.OR)
        
        # Ignorar espacios en blanco
        elif char in [' ', '\r', '\t', '\n']:
            pass
        
        # Procesar strings
        elif char == '"':
            self._string()
        elif char == "'":
            self._char()
        
        # Procesar números
        elif char.isdigit():
            self._number()
        
        # Procesar identificadores y palabras clave
        elif char.isalpha() or char == '_':
            self._identifier()
        
        else:
            line, column = self.reader.get_position_info()
            self._add_error(f"Carácter inesperado: {char}", line, column)

    def _string(self) -> None:
        """
        Procesa una cadena de texto entre comillas.
        """
        value = ""
        while self.reader.peek() != '"' and not self.reader.is_at_end():
            value += self.reader.advance()
            
        if self.reader.is_at_end():
            line, column = self.reader.get_position_info()
            self._add_error("Cadena sin terminar", line, column)
            return
            
        # Consumir la comilla de cierre
        self.reader.advance()
        
        # Crear token con tipo string
        token = Token(
            type=TokenType.STRING,
            lexeme=self.reader.source[self.start_position:self.reader.position],
            literal=value,
            line=self.reader.line,
            column=self.reader.column,
            data_type=TYPES['string']
        )
        self.tokens.append(token)

    def _char(self) -> None:
        """
        Procesa un carácter entre comillas simples.
        """
        if self.reader.is_at_end():
            line, column = self.reader.get_position_info()
            self._add_error("Carácter sin terminar", line, column)
            return
            
        value = self.reader.advance()
        
        if self.reader.peek() != "'":
            line, column = self.reader.get_position_info()
            self._add_error("Carácter debe ser de longitud 1", line, column)
            return
            
        # Consumir la comilla de cierre
        self.reader.advance()
        
        # Crear token con tipo char
        token = Token(
            type=TokenType.CHAR,
            lexeme=self.reader.source[self.start_position:self.reader.position],
            literal=value,
            line=self.reader.line,
            column=self.reader.column,
            data_type=TYPES['char']
        )
        self.tokens.append(token)

    def _number(self) -> None:
        """Procesa un número (entero o flotante)."""
        # Determinar si es negativo
        is_negative = self.reader.source[self.start_position] == '-'
        
        # Consumir dígitos antes del punto decimal
        while self.reader.peek().isdigit():
            self.reader.advance()
            
        # Verificar si hay punto decimal
        has_decimal = False
        decimal_digits = 0
        if self.reader.peek() == '.' and self.reader.peek_next().isdigit():
            has_decimal = True
            # Consumir el punto
            self.reader.advance()
            
            # Consumir dígitos después del punto y contarlos
            while self.reader.peek().isdigit():
                decimal_digits += 1
                self.reader.advance()
                
        # Obtener el valor literal
        try:
            text = self.reader.source[self.start_position:self.reader.position]
            if has_decimal:
                literal = float(text)
                # Usar f64 si hay más de 7 dígitos decimales (precisión de f32)
                data_type = TYPES['f64'] if decimal_digits > 7 else TYPES['f32']
            else:
                literal = int(text)
                # Si es negativo, solo puede ser tipo signed
                if is_negative:
                    if literal >= -128:
                        data_type = TYPES['i8']
                    elif literal >= -32768:
                        data_type = TYPES['i16']
                    elif literal >= -2147483648:
                        data_type = TYPES['i32']
                    else:
                        data_type = TYPES['i64']
                else:
                    # Para positivos, elegir el tipo más pequeño que lo pueda contener
                    if literal <= 127:
                        data_type = TYPES['i8']
                    elif literal <= 255:
                        data_type = TYPES['u8']
                    elif literal <= 32767:
                        data_type = TYPES['i16']
                    elif literal <= 65535:
                        data_type = TYPES['u16']
                    elif literal <= 2147483647:
                        data_type = TYPES['i32']
                    elif literal <= 4294967295:
                        data_type = TYPES['u32']
                    elif literal <= 9223372036854775807:
                        data_type = TYPES['i64']
                    else:
                        data_type = TYPES['u64']
                    
            # Crear token con el tipo correcto
            token = Token(
                type=TokenType.NUMBER,
                lexeme=text,
                literal=literal,
                line=self.reader.line,
                column=self.reader.column,
                data_type=data_type
            )
            self.tokens.append(token)
        except ValueError:
            line, column = self.reader.get_position_info()
            self._add_error(f"Número inválido: {text}", line, column)

    def _identifier(self) -> None:
        """
        Procesa un identificador, palabra clave o tipo.
        """
        while self.reader.peek().isalnum() or self.reader.peek() == '_':
            self.reader.advance()
            
        # Obtener el texto del identificador
        value = self.reader.source[self.start_position:self.reader.position]
            
        # Verificar si es una palabra clave o un tipo
        if value in self.keywords:
            token_type = self.keywords[value]
            # Asignar tipo de dato para true/false
            data_type = None
            if value in ['true', 'false']:
                data_type = TYPES['bool']
                
            token = Token(
                type=token_type,
                lexeme=value,
                literal=value == 'true' if value in ['true', 'false'] else None,
                line=self.reader.line,
                column=self.reader.column,
                data_type=data_type
            )
            self.tokens.append(token)
        elif value in self.type_keywords:
            token = Token(
                type=TokenType.TYPE,
                lexeme=value,
                literal=value,
                line=self.reader.line,
                column=self.reader.column,
                data_type=self._get_data_type(value)
            )
            self.tokens.append(token)
        else:
            self._add_token(TokenType.IDENTIFIER, value)

    def _get_data_type(self, type_name: str) -> Optional[DataType]:
        """Obtiene el tipo de dato correspondiente al nombre."""
        return TYPES.get(type_name)

    def _match(self, expected: str) -> bool:
        """
        Verifica si el siguiente carácter coincide con el esperado.
        
        Args:
            expected (str): El carácter esperado.
            
        Returns:
            bool: True si coincide, False en caso contrario.
        """
        if self.reader.is_at_end() or self.reader.peek() != expected:
            return False
            
        self.reader.advance()
        return True

    def _add_token(self, type: TokenType, literal: any = None) -> None:
        """
        Agrega un nuevo token a la lista de tokens.
        
        Args:
            type (TokenType): El tipo de token.
            literal (any, optional): El valor literal del token. Defaults to None.
        """
        line, column = self.reader.get_position_info()
        lexeme = self.reader.source[self.start_position:self.reader.position]
        self.tokens.append(Token(type, lexeme, literal, line, column))

    def _add_error(self, message: str, line: int, column: int) -> None:
        """
        Agrega un token de error.
        
        Args:
            message (str): El mensaje de error.
            line (int): La línea donde ocurrió el error.
            column (int): La columna donde ocurrió el error.
        """
        self.tokens.append(Token(TokenType.ERROR, message, None, line, column))

    def _create_token(self, type: TokenType, lexeme: str, literal: any) -> Token:
        """
        Crea un nuevo token.
        
        Args:
            type (TokenType): El tipo de token.
            lexeme (str): El texto del token.
            literal (any): El valor literal del token.
            
        Returns:
            Token: El token creado.
        """
        line, column = self.reader.get_position_info()
        return Token(type, lexeme, literal, line, column) 