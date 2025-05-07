import unittest
from src.lexer.lexer import Lexer
from src.semantic.semantic_analyzer import SemanticAnalyzer
from src.readers.source_reader import SourceReader
from src.tokens.token_type import TokenType

class TestCompiler(unittest.TestCase):
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

    def test_integer_ranges(self):
        # Test valid integer ranges
        test_cases = [
            "let x: i8 = 127;",      # Max i8
            "let x: i8 = -128;",     # Min i8
            "let x: u8 = 255;",      # Max u8
            "let x: u8 = 0;",        # Min u8
            "let x: i16 = 32767;",   # Max i16
            "let x: i16 = -32768;",  # Min i16
        ]
        
        for code in test_cases:
            success, errors = self.analyze_code(code)
            self.assertTrue(success, f"Failed on {code}: {errors}")

    def test_invalid_ranges(self):
        # Test invalid integer ranges
        test_cases = [
            "let x: i8 = 128;",      # Exceeds i8 max
            "let x: i8 = -129;",     # Exceeds i8 min
            "let x: u8 = 256;",      # Exceeds u8 max
            "let x: u8 = -1;",       # Invalid negative for u8
        ]
        
        for code in test_cases:
            success, errors = self.analyze_code(code)
            self.assertFalse(success, f"Should fail on {code} but didn't")

    def test_type_compatibility(self):
        # Test type compatibility rules
        test_cases = [
            # Valid cases
            "let x: i16 = 1000; let y: i32 = x;",  # Widening conversion
            "let x: f32 = 3.14; let y: f64 = x;",  # Float widening
            
            # Invalid cases
            "let x: i32 = 1000; let y: i16 = x;",  # Invalid narrowing
            "let x: f32 = 3.14; let y: i32 = x;",  # Invalid float to int
        ]
        
        # Valid cases should pass
        success, errors = self.analyze_code(test_cases[0])
        self.assertTrue(success, f"Valid widening failed: {errors}")
        
        success, errors = self.analyze_code(test_cases[1])
        self.assertTrue(success, f"Float widening failed: {errors}")
        
        # Invalid cases should fail
        success, errors = self.analyze_code(test_cases[2])
        self.assertFalse(success, "Invalid narrowing should fail")
        
        success, errors = self.analyze_code(test_cases[3])
        self.assertFalse(success, "Invalid float to int should fail")

    def test_operations(self):
        # Test arithmetic operations
        test_cases = [
            # Valid operations
            """
            let x: i32 = 10;
            let y: i32 = 20;
            let z: i32 = x + y;
            """,
            
            # String operations
            """
            let s1: string = "Hello";
            let s2: string = "World";
            let s3: string = s1 + s2;
            """,
            
            # Invalid operations
            """
            let x: string = "Hello";
            let y: i32 = 10;
            let z: string = x + y;
            """
        ]
        
        # Valid cases should pass
        success, errors = self.analyze_code(test_cases[0])
        self.assertTrue(success, f"Valid arithmetic failed: {errors}")
        
        success, errors = self.analyze_code(test_cases[1])
        self.assertTrue(success, f"Valid string concat failed: {errors}")
        
        # Invalid case should fail
        success, errors = self.analyze_code(test_cases[2])
        self.assertFalse(success, "Invalid string + int should fail")

    def test_type_inference(self):
        # Test type inference for literals
        test_cases = [
            "let x = 42;",           # Should infer i32
            "let x = 3.14;",         # Should infer f64
            "let x = true;",         # Should infer bool
            "let x = 'A';",          # Should infer char
            "let x = \"Hello\";",    # Should infer string
        ]
        
        for code in test_cases:
            success, errors = self.analyze_code(code)
            self.assertTrue(success, f"Type inference failed for {code}: {errors}")

if __name__ == '__main__':
    unittest.main() 