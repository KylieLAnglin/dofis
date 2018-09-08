from unittest import TestCase
from exemptions import extract_laws


class TestGet_laws(TestCase):
    def test_get_laws(self):
        text = 'Length of School Day (EC Legal) (TEC §25.082a) 21.111'
        laws = extract_laws.get_laws(text)
        self.assertEqual(len(laws), 2)
        self.assertEqual(laws[0], 25.082)
        self.assertEqual(laws[1], 21.111)

