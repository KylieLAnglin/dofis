from src.analysis.library import analysis
import pytest


def test_coef_with_stars():
    assert analysis.coef_with_stars(5, 5) == "5"


def test_format_se():
    assert analysis.format_se(.006) == "(0.01)"
    assert analysis.format_se(.005) == "(0.01)"
    assert analysis.format_se(.004) == "(0.00)"

