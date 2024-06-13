from utils.calculator_tool_spec import CalculatorToolSpec
import pytest

tool_spec = CalculatorToolSpec()


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (3, 4, 7),
        (5, 5, 10),
        (-1, 1, 0),
        (0, 0, 0),
    ],
)
def test_add(a, b, expected):
    """
    :param a: First integer
    :param b: Second integer
    :param expected: Expected result of adding a and b
    """
    actual = tool_spec.add(a, b)
    assert expected == actual


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (3, 4, -1),
        (5, 5, 0),
        (-1, 1, -2),
        (0, 0, 0),
    ],
)
def test_subtract(a, b, expected):
    """
    :param a: First integer
    :param b: Second integer
    :param expected: Expected result of subtracting b from a
    """
    actual = tool_spec.subtract(a, b)
    assert expected == actual


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (3, 4, 12),
        (5, 5, 25),
        (-1, 1, -1),
        (0, 0, 0),
    ],
)
def test_multiply(a, b, expected):
    """
    :param a: First integer
    :param b: Second integer
    :param expected: Expected result of multiplying a and b
    """
    actual = tool_spec.multiply(a, b)
    assert expected == actual


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (8, 4, 2),
        (5, 5, 1),
        (-1, 1, -1),
        (10, 2, 5),
        (3, 0, 0)
    ],
)
def test_divide(a, b, expected):
    """
    :param a: First integer
    :param b: Second integer
    :param expected: Expected result of dividing a by b
    """
    actual = tool_spec.divide(a, b)
    assert expected == actual


@pytest.mark.parametrize(
    "n, expected",
    [
        (0, 1),     # 0! = 1
        (1, 1),     # 1! = 1
        (2, 2),     # 2! = 2
        (3, 6),     # 3! = 6
        (4, 24),    # 4! = 24
        (5, 120),   # 5! = 120
        (6, 720),   # 6! = 720
    ],
)
def test_factorial(n, expected):
    """
    :param n: The number to compute the factorial of
    :param expected: Expected result of n!
    """
    actual = tool_spec.factorial(n)
    assert expected == actual


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (10, 3, 1),   # 10 % 3 = 1
        (20, 4, 0),   # 20 % 4 = 0
        (15, 6, 3),   # 15 % 6 = 3
        (7, 2, 1),    # 7 % 2 = 1
        (9, 3, 0),    # 9 % 3 = 0
        (13, 5, 3),   # 13 % 5 = 3
    ],
)
def test_modulus(a, b, expected):
    """
    :param a: The dividend
    :param b: The divisor
    :param expected: Expected result of a % b
    """
    actual = tool_spec.modulus(a, b)
    assert expected == actual


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (48, 18, 6),   # gcd(48, 18) = 6
        (20, 8, 4),    # gcd(20, 8) = 4
        (101, 10, 1),  # gcd(101, 10) = 1
        (56, 14, 14),  # gcd(56, 14) = 14
        (99, 27, 9),   # gcd(99, 27) = 9
        (270, 192, 6),  # gcd(270, 192) = 6
    ],
)
def test_gcd(a, b, expected):
    """
    :param a: The first integer
    :param b: The second integer
    :param expected: Expected result of gcd(a, b)
    """
    actual = tool_spec.gcd(a, b)
    assert expected == actual


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (4, 5, 20),    # lcm(4, 5) = 20
        (7, 3, 21),    # lcm(7, 3) = 21
        (12, 15, 60),  # lcm(12, 15) = 60
        (5, 10, 10),   # lcm(5, 10) = 10
        (9, 6, 18),    # lcm(9, 6) = 18
        (8, 14, 56),   # lcm(8, 14) = 56
    ],
)
def test_lcm(a, b, expected):
    """
    :param a: The first integer
    :param b: The second integer
    :param expected: Expected result of lcm(a, b)
    """
    actual = tool_spec.lcm(a, b)
    assert expected == actual


@pytest.mark.parametrize(
    "expression, expected",
    [
        ("3+2*2", 7),
        ("3+(2*2)", 7),
        ("10+(2*3)-3", 13),
        ("2*(5+5*2)/3+(6/2+8)", 21),
        ("1+1", 2),
        ("", 0),
    ],
)
def test_calculate(expression, expected):
    """
    Test the calculate method.
    :param expression: Arithmetic expression to evaluate
    :param expected: Expected result of the evaluation
    """
    actual = tool_spec.eval_expression(expression)
    assert actual == expected


@pytest.mark.parametrize(
    "n, expected",
    [
        (0, False),
        (1, False),
        (2, True),
        (3, True),
        (4, False),
        (17, True),
        (18, False),
    ],
)
def test_is_prime(n, expected):
    """
    Test the is_prime method.
    :param n: Integer to check for prime
    :param expected: Expected boolean result
    """
    actual = tool_spec.is_prime(n)
    assert actual == expected
