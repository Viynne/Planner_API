import pytest


def add(a: int, b: int) -> int:
    return a + b


def subtract(a: int, b: int) -> int:
    return a - b


def divide(a: int, b: int) -> int:
    return b // a


def test_add() -> None:
    assert add(3, 5) == 8


def test_subtract() -> None:
    assert subtract(7, 3) == 4


def test_divide() -> None:
    assert divide(20, 100) == 5
