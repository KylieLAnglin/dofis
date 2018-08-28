from unittest import TestCase
from exemptions import extract_dates


class TestGet_max_p_from_dict_list(TestCase):
    def test_get_max_p_from_dict_list(self):
        test_list = [{'TERM': 6.0811653384007514e-05},
                     {'TERM': 0.000637462770100683},
                     {'TERM': 0.7496848702430725},
                     {'TERM': 4.539787187241018e-05},
                     {'TERM': 4.539787187241018e-05},
                     {'TERM': 4.977573189535178e-05},
                     {'TERM': 0.9284722805023193},
                     {'TERM': 0.001019663061015308},
                     {'TERM': 0.0009384191362187266},
                     {'TERM': 0.00018428766634315252},
                     {'TERM': 0.0014342749491333961},
                     {'TERM': 0.0025924709625542164},
                     {'TERM': 0.9989855885505676},
                     {'TERM': 0.006762371398508549}]
        test_loc, test_p = extract_dates.get_max_p_from_dict_list(test_list)
        self.assertEqual(test_loc, 12)
        self.assertEqual(test_p, 0.9989855885505676)

        test_list = []
        test_loc, test_p = extract_dates.get_max_p_from_dict_list(test_list)
        self.assertEqual(test_loc, -999)
        self.assertEqual(test_p, 0)


