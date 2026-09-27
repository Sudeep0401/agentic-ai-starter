import pytest
from app.tools.calculator import calculate


def test_add():
    assert calculate(2, 3, "add") == 5


def test_multiply():
    assert calculate(5, 4, "multiply") == 20


def test_divide_by_zero():
    with pytest.raises(ValueError):
        calculate(5, 0, "divide")
