import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))  # Add src folder to path

import tkinter.messagebox as messagebox
from unittest.mock import MagicMock
# Mock the messagebox functions so no GUI pops up
messagebox.showwarning = MagicMock()
messagebox.showinfo = MagicMock()

import unittest
from main import MathEvaluator  # Adjust this if your main file is named differently

class TestMathEvaluatorFull(unittest.TestCase):
    def setUp(self):
        # Create instance without running Tkinter GUI
        self.calc = MathEvaluator.__new__(MathEvaluator)

        # Minimal attributes required for calculate() and memory
        self.calc.memory = 0
        self.calc.history = []
        self.calc.show_history = False

        # Mock entry widget
        self.calc.entry = type('', (), {})()
        self.calc.entry.text = ""
        self.calc.entry.get = lambda: self.calc.entry.text
        self.calc.entry.delete = lambda start, end: setattr(self.calc.entry, "text", "")
        self.calc.entry.insert = lambda index, value: setattr(self.calc.entry, "text", value)

        # Properly bind methods so 'self' works
        self.calc.evaluate_expression = MathEvaluator.evaluate_expression.__get__(self.calc)
        self.calc.validate_expression = MathEvaluator.validate_expression.__get__(self.calc)
        self.calc.calculate = MathEvaluator.calculate.__get__(self.calc)
        self.calc.memory_add = MathEvaluator.memory_add.__get__(self.calc)
        self.calc.memory_subtract = MathEvaluator.memory_subtract.__get__(self.calc)
        self.calc.memory_recall = MathEvaluator.memory_recall.__get__(self.calc)
        self.calc.memory_clear = MathEvaluator.memory_clear.__get__(self.calc)

    # ----------------------------
    # Helper function to simulate calculation
    # ----------------------------
    def run_calc(self, expr):
        self.calc.entry.text = expr
        self.calc.calculate()  # no extra self
        return self.calc.history[-1] if self.calc.history else None

    # ----------------------------
    # Expression Evaluation Tests
    # ----------------------------
    def test_simple_math(self):
        result = self.run_calc("2+3")
        self.assertEqual(result, "2+3 = 5")

    def test_power_operator(self):
        result = self.run_calc("2^3")
        self.assertEqual(result, "2^3 = 8")

    def test_functions(self):
        res_sqrt = self.run_calc("sqrt(16)")
        self.assertEqual(res_sqrt, "sqrt(16) = 4.0")
        res_log = self.run_calc("log(1)")
        self.assertEqual(res_log, "log(1) = 0.0")
        res_sin = self.run_calc("sin(0)")
        self.assertEqual(res_sin, "sin(0) = 0.0")
        res_fact = self.run_calc("factorial(5)")
        self.assertEqual(res_fact, "factorial(5) = 120")

    def test_constants(self):
        import math
        res_pi = self.run_calc("pi")
        self.assertEqual(res_pi, f"pi = {math.pi}")
        res_e = self.run_calc("e")
        self.assertEqual(res_e, f"e = {math.e}")

    # ----------------------------
    # Expression Validation Tests
    # ----------------------------
    def test_valid_expression(self):
        valid, msg = self.calc.validate_expression("2+3*(5-1)")
        self.assertTrue(valid)

    def test_invalid_characters(self):
        self.calc.entry.text = "2a+3"
        self.calc.calculate()
        self.assertEqual(len(self.calc.history), 0)

    def test_mismatched_parentheses(self):
        self.calc.entry.text = "(2+3"
        self.calc.calculate()
        self.assertEqual(len(self.calc.history), 0)

    def test_consecutive_operators(self):
        self.calc.entry.text = "2++3"
        self.calc.calculate()
        self.assertEqual(len(self.calc.history), 0)

    # ----------------------------
    # Memory Tests
    # ----------------------------
    def test_memory_add_recall_clear(self):
        # M+ adds
        self.calc.entry.text = "5"
        self.calc.memory_add()
        self.assertEqual(self.calc.memory, 5)

        # M- subtracts
        self.calc.entry.text = "2"
        self.calc.memory_subtract()
        self.assertEqual(self.calc.memory, 3)

        # MR recalls
        self.calc.entry.text = ""
        self.calc.memory_recall()
        self.assertEqual(self.calc.entry.text, "3")

        # MC clears
        self.calc.memory_clear()
        self.assertEqual(self.calc.memory, 0)

    # ----------------------------
    # History Tests
    # ----------------------------
    def test_history_append_clear(self):
        self.run_calc("1+1")
        self.assertEqual(len(self.calc.history), 1)
        self.calc.history.clear()
        self.assertEqual(len(self.calc.history), 0)


if __name__ == "__main__":
    unittest.main()
