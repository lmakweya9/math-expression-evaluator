import re


class ExpressionEvaluator:
    """
    This class evaluates mathematical expressions
    using recursive descent parsing.

    It is designed to be easy to understand for beginners.
    """

    def __init__(self, expression: str, debug: bool = False):
        self.expression = expression
        self.tokens = []
        self.pos = 0
        self.debug = debug   # If True, shows step-by-step output

    # -------------------------------------------------
    # TOKENIZATION
    # -------------------------------------------------

    def tokenize(self):
        """
        Break the input string into small parts called tokens.

        Example:
        "3 + 4 * 2"
        → ['3', '+', '4', '*', '2']
        """

        # Remove spaces
        clean = self.expression.replace(" ", "")

        # Regex for numbers and operators
        pattern = r'\d+(?:\.\d+)?|[+*/()-]'

        self.tokens = re.findall(pattern, clean)

        # Check if everything was tokenized correctly
        if "".join(self.tokens) != clean:
            raise ValueError("Invalid characters found")

        if self.debug:
            print("Tokens:", self.tokens)

    # -------------------------------------------------
    # PARSER FUNCTIONS
    # -------------------------------------------------

    def parse_expression(self):
        """
        Handles addition and subtraction (+, -)

        Grammar:
        expression = term { (+|-) term }
        """

        result = self.parse_term()

        while self.pos < len(self.tokens) and self.tokens[self.pos] in ("+", "-"):
            operator = self.tokens[self.pos]
            self.pos += 1

            right = self.parse_term()

            if self.debug:
                print(f"Calculating: {result} {operator} {right}")

            if operator == "+":
                result += right
            else:
                result -= right

        return result

    def parse_term(self):
        """
        Handles multiplication and division (*, /)

        Grammar:
        term = factor { (*|/) factor }
        """

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
        """
        Handles numbers and parentheses

        Grammar:
        factor = number | '(' expression ')'
        """

        token = self.tokens[self.pos]
        self.pos += 1

        # If we find an opening bracket, solve what's inside
        if token == "(":

            if self.debug:
                print("Opening bracket found")

            result = self.parse_expression()

            # Skip closing bracket
            if self.tokens[self.pos] != ")":
                raise ValueError("Missing closing bracket")

            self.pos += 1

            if self.debug:
                print("Closing bracket found")

            return result

        # Otherwise, it must be a number
        if self.debug:
            print("Number found:", token)

        return float(token)

    # -------------------------------------------------
    # MAIN EVALUATION FUNCTION
    # -------------------------------------------------

    def evaluate(self):
        """
        Main function that runs the evaluation process
        """

        try:
            # Step 1: Convert input to tokens
            self.tokenize()

            # Step 2: Parse and calculate
            result = self.parse_expression()

            # Step 3: Check for extra tokens
            if self.pos < len(self.tokens):
                raise ValueError("Unexpected input")

            # Step 4: Format output nicely
            if result == int(result):
                return str(int(result))

            return str(round(result, 2))

        except Exception as e:
            return f"Invalid Expression: {e}"


# -------------------------------------------------
# RUN PROGRAM
# -------------------------------------------------

if __name__ == "__main__":

    print("=== Math Expression Evaluator ===")

    # Example input
    expression = "(3 + 3) * 42 / (6 + 1)"

    # Turn debug ON to see steps
    DEBUG_MODE = True

    calculator = ExpressionEvaluator(expression, debug=DEBUG_MODE)

    result = calculator.evaluate()

    print("\nExpression:", expression)
    print("Result:", result)
