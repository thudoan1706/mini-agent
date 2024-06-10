from utils import add, subtract, multiply, divide
import pytest


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
    actual = add(a, b)
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
    actual = subtract(a, b)
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
    actual = multiply(a, b)
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
    actual = divide(a, b)
    assert expected == actual
