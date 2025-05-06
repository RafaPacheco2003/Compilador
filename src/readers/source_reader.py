class SourceReader:
    """
    Clase que maneja la lectura del código fuente.
    Siguiendo el principio Single Responsibility, esta clase solo se encarga
    de manejar la lectura del texto fuente y mantener el seguimiento de la posición.
    """
    
    def __init__(self, source: str):
        """
        Inicializa el lector con el código fuente.
        
        Args:
            source (str): El código fuente a analizar.
        """
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1
        self.length = len(source)
    
    def peek(self) -> str:
        """
        Mira el siguiente carácter sin avanzar la posición.
        
        Returns:
            str: El siguiente carácter o un carácter nulo si llegamos al final.
        """
        if self.is_at_end():
            return '\0'
        return self.source[self.position]
    
    def peek_next(self) -> str:
        """
        Mira el carácter después del siguiente sin avanzar la posición.
        
        Returns:
            str: El carácter después del siguiente o un carácter nulo si llegamos al final.
        """
        if self.position + 1 >= self.length:
            return '\0'
        return self.source[self.position + 1]
    
    def advance(self) -> str:
        """
        Avanza la posición y retorna el carácter actual.
        
        Returns:
            str: El carácter actual.
        """
        char = self.peek()
        self.position += 1
        
        if char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
            
        return char
    
    def is_at_end(self) -> bool:
        """
        Verifica si hemos llegado al final del código fuente.
        
        Returns:
            bool: True si estamos al final del código fuente, False en caso contrario.
        """
        return self.position >= self.length
    
    def get_position_info(self) -> tuple[int, int]:
        """
        Obtiene la información actual de posición.
        
        Returns:
            tuple[int, int]: Una tupla con la línea y columna actual.
        """
        return (self.line, self.column) 