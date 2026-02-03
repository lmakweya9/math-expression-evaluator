import unittest
import math
import sys
import os

# Adjust path to find 'src' regardless of execution folder
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.main import CalculatorEngine

class TestMathEvaluator(unittest.TestCase):
    def setUp(self):
        self.calc = CalculatorEngine()

    def test_math_logic(self):
        """Tests basic and complex math evaluation."""
        self.assertEqual(self.calc.evaluate_expression("10 + 5 * 2"), 20)
        self.assertEqual(self.calc.evaluate_expression("2^3"), 8)
        self.assertEqual(self.calc.evaluate_expression("5!"), 120)
        self.assertAlmostEqual(self.calc.evaluate_expression("pi"), math.pi)

    def test_variable_storage(self):
        """Tests the variable storage and reuse feature."""
        self.assertEqual(self.calc.evaluate_expression("x = 10"), 10)
        self.assertEqual(self.calc.evaluate_expression("x + 5"), 15)
        self.assertEqual(self.calc.evaluate_expression("y = x * 2"), 20)
        self.assertEqual(self.calc.evaluate_expression("y / 4"), 5)

    def test_errors(self):
        """Tests that the engine catches and raises appropriate errors."""
        with self.assertRaises(ZeroDivisionError):
            self.calc.evaluate_expression("10 / 0")
        with self.assertRaises(SyntaxError):
            self.calc.evaluate_expression("5 + (2 *")  # Missing bracket
        with self.assertRaises(SyntaxError):
            self.calc.evaluate_expression("123 = x")   # Invalid assignment

    def test_memory(self):
        """Tests M+, MR, and MC logic."""
        self.calc.memory_add(50)
        self.assertEqual(self.calc.memory_recall(), 50)
        self.calc.memory_clear()
        self.assertEqual(self.calc.memory_recall(), 0)

if __name__ == "__main__":
    unittest.main()