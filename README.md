# Analizador Léxico

Este proyecto implementa un analizador léxico siguiendo los principios SOLID en Python. El analizador es parte de un compilador y está diseñado para ser extensible y mantenible.

## Estructura del Proyecto

```
lexer/
├── src/
│   ├── tokens/
│   │   ├── __init__.py
│   │   ├── token.py
│   │   └── token_type.py
│   ├── lexer/
│   │   ├── __init__.py
│   │   ├── lexer_interface.py
│   │   └── lexer.py
│   └── readers/
│       ├── __init__.py
│       └── source_reader.py
├── tests/
│   └── test_lexer.py
├── requirements.txt
└── README.md
```

## Componentes Principales

### 1. TokenType (token_type.py)
Define todos los tipos de tokens que el analizador puede reconocer:
- Operadores: `+`, `-`, `*`, `/`, `=`, `==`, `!=`, etc.
- Delimitadores: `(`, `)`, `{`, `}`, `;`
- Palabras clave: `if`, `else`, `while`, `function`
- Literales: números, strings, identificadores
- Tokens especiales: EOF, ERROR

### 2. Token (token.py)
Representa un token individual con:
- `type`: Tipo del token (TokenType)
- `lexeme`: Texto original encontrado
- `literal`: Valor procesado (ej: string "42" → float 42.0)
- `line`: Número de línea
- `column`: Número de columna

### 3. SourceReader (source_reader.py)
Maneja la lectura del código fuente:
- Mantiene la posición actual de lectura
- Rastrea línea y columna
- Proporciona métodos para:
  - Mirar el siguiente carácter (`peek()`)
  - Avanzar al siguiente carácter (`advance()`)
  - Verificar fin del archivo (`is_at_end()`)

### 4. LexerInterface (lexer_interface.py)
Define el contrato para analizadores léxicos:
- `tokenize()`: Analiza todo el código
- `next_token()`: Obtiene siguiente token
- `peek()`: Mira siguiente token sin consumirlo

### 5. Lexer (lexer.py)
Implementación principal del analizador léxico:
- Procesa el código fuente carácter por carácter
- Identifica y crea tokens
- Maneja errores léxicos

## Proceso de Análisis Léxico

1. **Inicialización**:
   ```python
   reader = SourceReader(codigo_fuente)
   lexer = Lexer(reader)
   ```

2. **Tokenización**:
   - El lexer lee carácter por carácter
   - Identifica patrones (números, palabras, símbolos)
   - Crea tokens según el patrón identificado

3. **Procesamiento de Tokens**:
   - **Números**: Lee dígitos consecutivos y punto decimal
   ```python
   # Entrada: "42.5"
   # Token: NUMBER, "42.5", 42.5
   ```

   - **Identificadores**: Lee letras y dígitos
   ```python
   # Entrada: "variable1"
   # Token: IDENTIFIER, "variable1", "variable1"
   ```

   - **Strings**: Lee caracteres entre comillas
   ```python
   # Entrada: "Hola mundo"
   # Token: STRING, "Hola mundo", "Hola mundo"
   ```

   - **Operadores y Símbolos**: Reconoce símbolos especiales
   ```python
   # Entrada: "+"
   # Token: PLUS, "+", None
   ```

4. **Manejo de Errores**:
   - Detecta caracteres inválidos
   - Reporta strings sin cerrar
   - Mantiene información de posición para debug

## Ejemplo de Uso

```python
# Código fuente de ejemplo
source_code = """
function factorial(n) {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}
"""

# Crear analizador léxico
reader = SourceReader(source_code)
lexer = Lexer(reader)

# Obtener tokens
tokens = lexer.tokenize()

# Imprimir tokens
for token in tokens:
    print(token)
```

## Salida de Ejemplo

```
Token(FUNCTION, "function", None, line=1, col=1)
Token(IDENTIFIER, "factorial", "factorial", line=1, col=10)
Token(LEFT_PAREN, "(", None, line=1, col=18)
Token(IDENTIFIER, "n", "n", line=1, col=19)
Token(RIGHT_PAREN, ")", None, line=1, col=20)
...
```

## Principios SOLID Aplicados

1. **Single Responsibility (SRP)**:
   - Cada clase tiene una única responsabilidad
   - `Token`: Almacena información de un token
   - `SourceReader`: Maneja la lectura del código
   - `Lexer`: Realiza el análisis léxico

2. **Open/Closed (OCP)**:
   - Se pueden agregar nuevos tipos de tokens sin modificar el código existente
   - Fácil extensión para nuevos patrones léxicos

3. **Liskov Substitution (LSP)**:
   - `LexerInterface` define un contrato claro
   - Cualquier implementación puede sustituir a la interfaz

4. **Interface Segregation (ISP)**:
   - Interfaces pequeñas y específicas
   - Métodos claramente definidos y cohesivos

5. **Dependency Inversion (DIP)**:
   - El código depende de abstracciones
   - Uso de inyección de dependencias

## Instalación y Ejecución

1. Clonar el repositorio
2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Ejecutar pruebas:
   ```bash
   python tests/test_lexer.py
   ``` 