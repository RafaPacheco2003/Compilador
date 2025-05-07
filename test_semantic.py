from src.lexer.lexer import Lexer
from src.semantic.semantic_analyzer import SemanticAnalyzer
from src.readers.source_reader import SourceReader

def test_semantic_analysis(file_path: str):
    """
    Realiza el análisis semántico de un archivo y muestra los resultados.
    
    Args:
        file_path (str): Ruta al archivo a analizar
    """
    print(f"\nAnalizando archivo: {file_path}")
    print("=" * 50)
    
    # Leer el archivo
    with open(file_path, 'r', encoding='utf-8') as file:
        source = file.read()
        
    # Mostrar el código fuente
    print("\nCódigo fuente:")
    print("-" * 20)
    print(source)
    
    # Análisis léxico
    reader = SourceReader(source)
    lexer = Lexer(reader)
    tokens = lexer.tokenize()
    
    # Mostrar tokens generados
    print("\nTokens generados:")
    print("-" * 20)
    for token in tokens:
        if token.type.name not in ['SEMICOLON', 'EOF']:
            print(f"Token: {token}")
    
    # Análisis semántico
    semantic_analyzer = SemanticAnalyzer()
    semantic_analyzer.analyze(tokens)
    
    # Mostrar resultados del análisis semántico
    print("\nResultados del análisis semántico:")
    print("-" * 20)
    
    if semantic_analyzer.error_handler.has_errors():
        print("\nErrores encontrados:")
        for error in semantic_analyzer.error_handler.errors:
            print(f"\n- {error}")
    else:
        print("No se encontraron errores semánticos.")
    
    # Mostrar tabla de símbolos
    print("\nTabla de símbolos:")
    print("-" * 20)
    for var_name, var_type in semantic_analyzer.symbol_table.items():
        print(f"Variable: {var_name}, Tipo: {var_type.name}")

if __name__ == "__main__":
    # Probar con nuestro archivo de ejemplo
    test_semantic_analysis("examples/test_tipos.txt") 