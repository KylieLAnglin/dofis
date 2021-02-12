from dofis.analysis.library import analysis
import pytest


def test_coef_with_stars():
    assert analysis.coef_with_stars(5, 5) == "5.0"
    assert analysis.coef_with_stars(5, 0.05) == "5.0*"
    assert analysis.coef_with_stars(2.45, 0.004, 1) == "2.45**"
    assert analysis.coef_with_stars(2.45, 0.05, 2) == "2.45"


def test_format_se():
    assert analysis.format_se(0.006) == "(0.01)"
    assert analysis.format_se(0.005) == "(0.01)"
    assert analysis.format_se(0.004) == "(0.0)"
    assert analysis.format_se(1.34) == "(1.34)"
