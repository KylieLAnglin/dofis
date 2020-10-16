from .. import analysis
import unittest

import pytest


def test_coef_with_stars():
    assert analysis.coef_with_stars(.111, .056) == "0.11"
    with pytest.raises(AssertionError):
        assert False

test_coef_with_stars()
