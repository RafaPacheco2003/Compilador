from typing import List, Dict, Optional, Tuple
from .lexer_interface import LexerInterface
from ..tokens.token import Token
from ..tokens.token_type import TokenType
from ..readers.source_reader import SourceReader
from ..types.data_type import DataType

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
        
        # Diccionario de palabras reservadas
        self.keywords: Dict[str, TokenType] = {
            "let": TokenType.LET,
            "mut": TokenType.MUT,
            "fn": TokenType.FN,
            "struct": TokenType.STRUCT,
            "enum": TokenType.ENUM,
            "impl": TokenType.IMPL,
            "pub": TokenType.PUB,
            "return": TokenType.RETURN,
            "if": TokenType.IF,
            "else": TokenType.ELSE,
            "while": TokenType.WHILE,
            "for": TokenType.FOR,
            "in": TokenType.IN,
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
            "str": TokenType.TYPE_STR,
            "String": TokenType.TYPE_STRING,
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
        self._add_token(TokenType.STRING, value)

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
        self._add_token(TokenType.CHAR, value)

    def _number(self) -> None:
        """
        Procesa un número (entero o decimal) y sus posibles sufijos de tipo.
        """
        while self.reader.peek().isdigit():
            self.reader.advance()
            
        # Buscar parte decimal
        is_float = False
        if self.reader.peek() == '.' and self.reader.peek_next().isdigit():
            is_float = True
            self.reader.advance()  # Consumir el punto
            while self.reader.peek().isdigit():
                self.reader.advance()
                
        # Buscar sufijo de tipo
        suffix = ""
        if self.reader.peek().isalpha():
            while self.reader.peek().isalnum():
                suffix += self.reader.advance()
                
        # Obtener el valor completo del número
        value = self.reader.source[self.start_position:self.reader.position-len(suffix) if suffix else self.reader.position]
        number = float(value)
        
        # Crear token con sufijo de tipo si existe
        token = Token(
            type=TokenType.NUMBER,
            lexeme=self.reader.source[self.start_position:self.reader.position],
            literal=number,
            line=self.reader.line,
            column=self.reader.column,
            literal_suffix=suffix if suffix else None
        )
        
        self.tokens.append(token)

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
            self._add_token(self.keywords[value])
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
        """
        Convierte un nombre de tipo en un objeto DataType.
        """
        type_map = {
            "i8": DataType.i8,
            "i16": DataType.i16,
            "i32": DataType.i32,
            "i64": DataType.i64,
            "u8": DataType.u8,
            "u16": DataType.u16,
            "u32": DataType.u32,
            "u64": DataType.u64,
            "f32": DataType.f32,
            "f64": DataType.f64,
            "bool": DataType.bool,
            "char": DataType.char,
        }
        return type_map[type_name]() if type_name in type_map else None

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