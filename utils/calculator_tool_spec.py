from llama_index.core.tools.tool_spec.base import BaseToolSpec


class CalculatorToolSpec(BaseToolSpec):
    """Calculator tool spec."""
    spec_functions = ["multiply", "divide", "add", "exponential",
                      "subtract", "factorial", "is_prime", "modulus",
                      "gcd", "lcm"]

    def multiply(self, a: int, b: int) -> int:
        """Multiple two integers and returns the result integer"""
        return a * b

    def add(self, a: int, b: int) -> int:
        """Add two integers and returns the result integer"""
        return a + b

    def subtract(self, a: int, b: int) -> int:
        """Subtract two integers and returns the result integer"""
        return a - b

    def divide(self, a: int, b: int) -> int:
        """Divide two integers and returns the result integer"""
        return a / b if b != 0 else 0

    def exponential(self, a: int, b: int) -> int:
        """Calculate a raised to the power of b and return the result"""
        return a ** b

    def factorial(self, n: int) -> int:
        """Compute the factorial of given integer when encountering operation "!" and returns the result integer"""
        if (n == 0):
            return 1
        return n * self.factorial(n - 1)

    def is_prime(self, n: int) -> bool:
        """Check if the given integer is a prime number."""
        if n <= 1:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True

    def modulus(self, a: int, b: int) -> int:
        """Compute the modulus of two integers and return the result"""
        return a % b

    def gcd(self, a: int, b: int) -> int:
        """Compute the greatest common divisor of two integers and return the result"""
        while b:
            a, b = b, a % b
        return a

    def lcm(self, a: int, b: int) -> int:
        """Compute the least common multiple of two integers and return the result"""
        return abs(a * b) // self.gcd(a, b)

    def eval_expression(self, expression: str) -> int:
        """
        Evaluate the given arithmetic expression and return the result.

        This method supports the following operations:
        - Addition (+)
        - Subtraction (-)
        - Multiplication (*)
        - Division (/)
        - Parentheses for grouping expressions ()

        :param expression: A string containing the arithmetic expression to evaluate.
                           The expression should be a valid mathematical expression
                           containing integers and the operators +, -, *, /, and ().
        :return: The result of evaluating the arithmetic expression as an integer.

        Example:
            calculator = ArithmeticCalculator()
            result = calculator.calculate("3+(2*2)")
            print(result)  # Output: 7
        """
        num = 0
        op = "+"
        stack = []

        def helper(op, num):
            if op == "+":
                stack.append(num)
            elif op == "-":
                stack.append(-num)
            elif op == "*":
                stack.append(stack.pop() * num)
            elif op == "/":
                stack.append(int(stack.pop() / num))

        for i, char in enumerate(expression):
            if char.isdigit():
                num = num * 10 + int(char)
            elif char == '(':
                stack.append(op)
                num = 0
                op = "+"
            elif char in '+-*/)' or i == len(expression) - 1:
                helper(op, num)

                if char == ")":
                    num = 0
                    while isinstance(stack[-1], int):
                        num += stack.pop()
                    op = stack.pop()
                    helper(op, num)

                num = 0
                op = char
        helper(op, num)

        return sum(stack)
