from llama_index.core.tools.tool_spec.base import BaseToolSpec


class CalculatorToolSpec(BaseToolSpec):
    """Calculator tool spec."""
    spec_functions = ["multiply", "divide", "add", "subtract", "factorial"]

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
        return a // b if b != 0 else 0

    def exponential(self, a: int, b: int) -> int:
        """Calculate a raised to the power of b and return the result"""
        return a ** b

    def factorial(self, n: int) -> int:
        """Compute the factorial of given integer and returns the result integer"""
        if (n == 0):
            return 1
        return n * self.factorial(n - 1)
