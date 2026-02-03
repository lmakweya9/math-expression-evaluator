import unittest
import math
import sys
import os

# Ensure the 'src' directory is in the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.main import CalculatorEngine

class TestMathEvaluator(unittest.TestCase):
    def setUp(self):
        self.calc = CalculatorEngine()

    def test_math_operations(self):
        self.assertEqual(self.calc.evaluate_expression("10 + 5 * 2"), 20)
        self.assertEqual(self.calc.evaluate_expression("2^3"), 8)
        self.assertEqual(self.calc.evaluate_expression("5!"), 120)

    def test_constants(self):
        self.assertAlmostEqual(self.calc.evaluate_expression("pi"), math.pi)
        self.assertAlmostEqual(self.calc.evaluate_expression("e"), math.e)

    def test_errors(self):
        with self.assertRaises(ZeroDivisionError):
            self.calc.evaluate_expression("1/0")
        with self.assertRaises(SyntaxError):
            self.calc.evaluate_expression("5 + (2 *")

    def test_memory_logic(self):
        self.calc.memory_add(50)
        self.assertEqual(self.calc.memory_recall(), 50)
        self.calc.memory_clear()
        self.assertEqual(self.calc.memory_recall(), 0)

if __name__ == "__main__":
    unittest.main()