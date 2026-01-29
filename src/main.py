import re
import tkinter as tk

# ==============================
# ExpressionEvaluator Class
# ==============================
class ExpressionEvaluator:
    """
    Evaluates mathematical expressions using recursive descent parsing.
    Includes debug/teaching mode to show step-by-step evaluation.
    """

    def __init__(self, expression: str, debug: bool = False):
        self.expression = expression
        self.tokens = []
        self.pos = 0
        self.debug = debug   # Show step-by-step output if True

    # ---------------- TOKENIZATION ----------------
    def tokenize(self):
        """
        Convert the input string into tokens (numbers and operators)
        Example: "3 + 4 * 2" -> ['3', '+', '4', '*', '2']
        """
        clean = self.expression.replace(" ", "")
        pattern = r'\d+(?:\.\d+)?|[+*/()-]'
        self.tokens = re.findall(pattern, clean)

        # Validate all characters
        if "".join(self.tokens) != clean:
            raise ValueError("Invalid characters found")

        if self.debug:
            print("Tokens:", self.tokens)

    # ---------------- PARSER FUNCTIONS ----------------
    def parse_expression(self):
        """Handles addition and subtraction"""
        result = self.parse_term()
        while self.pos < len(self.tokens) and self.tokens[self.pos] in ("+", "-"):
            operator = self.tokens[self.pos]
            self.pos += 1
            right = self.parse_term()
            if self.debug:
                print(f"Calculating: {result} {operator} {right}")
            result = result + right if operator == "+" else result - right
        return result

    def parse_term(self):
        """Handles multiplication and division"""
        result = self.parse_factor()
        while self.pos < len(self.tokens) and self.tokens[self.pos] in ("*", "/"):
            operator = self.tokens[self.pos]
            self.pos += 1
            right = self.parse_factor()
            if self.debug:
                print(f"Calculating: {result} {operator} {right}")
            if operator == "*":
                result *= right
            else:
                if right == 0:
                    raise ValueError("Division by zero")
                result /= right
        return result

    def parse_factor(self):
        """Handles numbers and parentheses"""
        token = self.tokens[self.pos]
        self.pos += 1

        if token == "(":
            if self.debug:
                print("Opening bracket found")
            result = self.parse_expression()
            if self.tokens[self.pos] != ")":
                raise ValueError("Missing closing bracket")
            self.pos += 1
            if self.debug:
                print("Closing bracket found")
            return result

        if self.debug:
            print("Number found:", token)

        return float(token)

    # ---------------- MAIN EVALUATION ----------------
    def evaluate(self):
        """Run tokenization, parsing, and return result"""
        try:
            self.tokenize()
            result = self.parse_expression()
            if self.pos < len(self.tokens):
                raise ValueError("Unexpected input")
            return str(int(result)) if result == int(result) else str(round(result, 2))
        except Exception as e:
            return f"Invalid Expression: {e}"


# ==============================
# CLI TEST (Optional)
# ==============================
if __name__ == "__main__" and False:  # Change False to True if you want CLI mode
    test_expr = "(3 + 3) * 42 / (6 + 1)"
    calc = ExpressionEvaluator(test_expr, debug=True)
    print("Expression:", test_expr)
    print("Result:", calc.evaluate())


# ==============================
# Tkinter GUI with History
# ==============================

def evaluate_expression():
    expr = entry.get()

    if not expr.strip():
        return

    debug = debug_var.get()
    evaluator = ExpressionEvaluator(expr, debug=debug)
    result = evaluator.evaluate()

    result_label.config(text=f"Result: {result}")

    # Save to history
    history_list.insert(tk.END, f"{expr} = {result}")


def clear_history():
    history_list.delete(0, tk.END)


def use_history(event):
    selected = history_list.curselection()

    if selected:
        value = history_list.get(selected)
        expression = value.split("=")[0].strip()
        entry.delete(0, tk.END)
        entry.insert(0, expression)


# Create main window
root = tk.Tk()
root.title("Math Expression Evaluator")

# Input
tk.Label(root, text="Enter Expression:").grid(row=0, column=0, padx=5, pady=5)

entry = tk.Entry(root, width=30)
entry.grid(row=0, column=1, padx=5, pady=5)

# Debug
debug_var = tk.BooleanVar()

tk.Checkbutton(
    root,
    text="Show Debug",
    variable=debug_var
).grid(row=1, column=0, columnspan=2)

# Buttons
tk.Button(
    root,
    text="Evaluate",
    command=evaluate_expression
).grid(row=2, column=0, columnspan=2, pady=5)


tk.Button(
    root,
    text="Clear History",
    command=clear_history
).grid(row=3, column=0, columnspan=2, pady=3)

# Result
result_label = tk.Label(root, text="Result: ", font=("Arial", 14))
result_label.grid(row=4, column=0, columnspan=2, pady=10)

# History Panel
tk.Label(root, text="History").grid(row=0, column=2, padx=10)

history_list = tk.Listbox(root, width=30, height=12)
history_list.grid(row=1, column=2, rowspan=4, padx=10)

history_list.bind("<<ListboxSelect>>", use_history)

# Run app
root.mainloop()