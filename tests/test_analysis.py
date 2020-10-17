from src.analysis.library import analysis
import pytest

def test_coef_with_stars():
    assert analysis.coef_with_stars(5, 5) == "5"

test_coef_with_stars()

def func(x):
    return x + 1

def test_answer():
    assert func(3) == 4

