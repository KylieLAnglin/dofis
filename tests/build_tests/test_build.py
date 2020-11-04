import pytest

from dofis.data_from_tea.library import build
from dofis.data_from_tea.library import start

import os

test_path = os.path.join(start.data_path, 'tea', 'teachers', 'certification_' + 'yr1718' + '/')


def test_concat_files():
    build.concat_files(path=test_path, pattern="CERTIFICATION_01.csv")
