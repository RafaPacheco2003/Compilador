import unittest
from src.lexer.lexer import Lexer
from src.semantic.semantic_analyzer import SemanticAnalyzer
from src.readers.source_reader import SourceReader
from src.tokens.token_type import TokenType
from src.semantic.error_handler import ErrorHandler

class TestCompiladorCompleto(unittest.TestCase):
    def setUp(self):
        self.semantic_analyzer = SemanticAnalyzer()

    def analyze_code(self, source_code: str):
        """Helper method to perform lexical and semantic analysis"""
        reader = SourceReader(source_code)
        lexer = Lexer(reader)
        tokens = lexer.tokenize()
        
        # Check for lexical errors
        errors = [t for t in tokens if t.type == TokenType.ERROR]
        if errors:
            return False, [f"Error léxico en línea {e.line}, columna {e.column}: {e.lexeme}" for e in errors]
            
        # Perform semantic analysis
        self.semantic_analyzer.analyze(tokens)
        semantic_errors = self.semantic_analyzer.error_handler.errors
        
        if semantic_errors:
            return False, [str(error) for error in semantic_errors]
        return True, []

    def test_declaraciones_simples(self):
        """Prueba declaraciones simples de variables con diferentes tipos"""
        test_cases = [
            # Enteros con signo
            "let x: i8 = 127;",
            "let x: i16 = 32767;",
            "let x: i32 = 2147483647;",
            "let x: i64 = 9223372036854775807;",
            
            # Enteros sin signo
            "let x: u8 = 255;",
            "let x: u16 = 65535;",
            "let x: u32 = 4294967295;",
            
            # Flotantes
            "let x: f32 = 3.14;",
            "let x: f64 = 3.14159265359;",
            
            # Otros tipos
            "let x: bool = true;",
            "let x: char = 'A';",
            "let x: string = \"Hello, World!\";"
        ]
        
        for code in test_cases:
            success, errors = self.analyze_code(code)
            self.assertTrue(success, f"Falló en {code}: {errors}")

    def test_inferencia_tipos(self):
        """Prueba la inferencia de tipos"""
        test_cases = [
            "let x = 42;",          # Debería inferir i32
            "let x = 3.14;",        # Debería inferir f64
            "let x = true;",        # Debería inferir bool
            "let x = 'X';",         # Debería inferir char
            "let x = \"texto\";",   # Debería inferir string
        ]
        
        for code in test_cases:
            success, errors = self.analyze_code(code)
            self.assertTrue(success, f"Falló en {code}: {errors}")

    def test_operaciones_aritmeticas(self):
        """Prueba operaciones aritméticas entre diferentes tipos"""
        test_cases = [
            # Operaciones entre enteros
            """
            let a: i32 = 10;
            let b: i32 = 20;
            let c: i32 = a + b;
            let d: i32 = a * b;
            let e: i32 = b - a;
            let f: i32 = b / a;
            """,
            
            # Operaciones con flotantes
            """
            let x: f64 = 3.14;
            let y: f64 = 2.0;
            let z: f64 = x + y;
            let w: f64 = x * y;
            """,
            
            # Operaciones mixtas (con conversión implícita segura)
            """
            let i: i32 = 42;
            let f: f64 = 3.14;
            let r: f64 = i + f;
            """
        ]
        
        for code in test_cases:
            success, errors = self.analyze_code(code)
            self.assertTrue(success, f"Falló en operaciones aritméticas: {errors}")

    def test_conversiones_explicitas(self):
        """Prueba conversiones explícitas entre tipos"""
        test_cases = [
            # Conversiones válidas
            """
            let x: i16 = 1000;
            let y: i32 = x;
            """,
            
            """
            let x: f32 = 3.14;
            let y: f64 = x;
            """,
            
            """
            let x: i8 = 100;
            let y: i16 = x;
            """
        ]
        
        for code in test_cases:
            success, errors = self.analyze_code(code)
            self.assertTrue(success, f"Falló en conversiones explícitas: {errors}")
            
    def test_errores_tipo(self):
        """Prueba detección de errores de tipo"""
        test_cases = [
            # Asignación de tipo incorrecto
            "let x: i8 = 128;",  # Fuera de rango para i8
            "let x: u8 = -1;",   # Valor negativo en unsigned
            "let x: i16 = 40000;"  # Fuera de rango para i16
            
            # Operaciones inválidas
            """
            let s: string = "hello";
            let n: i32 = 42;
            let r: string = s + n;
            """,
            
            
            # Conversión insegura
            """
            # let x: i32 = 1000000;
            # let y: i16 = x;
            """
        ]
        
        for code in test_cases:
            success, errors = self.analyze_code(code)
            self.assertFalse(success, f"Debería haber fallado: {code}")
            
    def test_operaciones_strings(self):
        """Prueba operaciones con strings"""
        test_cases = [
            # Concatenación válida
            """
            let s1: string = "Hello, ";
            let s2: string = "World!";
            let s3: string = s1 + s2;
            """,
            
            # Asignación de string literal
            'let msg: string = "Este es un mensaje largo";'
        ]
        
        for code in test_cases:
            success, errors = self.analyze_code(code)
            self.assertTrue(success, f"Falló en operaciones con strings: {errors}")

if __name__ == '__main__':
    unittest.main() 