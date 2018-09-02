from unittest import TestCase
import os
from exemptions import start
from exemptions import extract_dates



class TestGet_term_date_and_phrase(TestCase):
    def test_get_term_date_and_phrase(self):
        output_dir = os.path.join(start.data_path, 'date_term_classifier')
        test = 'ECISD District of Innovation Plan 1 I. Introduction House Bill 1842, passed during the 84th ' \
               'Legislative Session, permits Texas public school districts to become Districts of Innovation and to ' \
               'obtain exemption from certain provisions of the Texas Education Code. On February 21, 2017 the Ector ' \
               'County Independent School District’s Board of Trustees (“Board”) passed a resolution to initiate the ' \
               'Process of Designation as a District of Innovation in order to increase local control over District ' \
               'operations and to support innovation and local initiatives to improve educational outcomes for the ' \
               'benefit of students and the community. On February 28, 2017, the Board appointed an eighteen member ' \
               'District of Innovation Committee (“Committee”) comprised of district leaders, teachers, parents, ' \
               'and community members representing a variety of roles and responsibilities. The Committee met on ' \
               'March 2, 6, and 10, 2017, to discuss and draft this Local Innovation Plan (“Plan”). Based on ' \
               'direction provided by the Board and input from various District stakeholders, the Committee proposes ' \
               'this Plan. II. Term The term of the Plan will begin with the 2017-2018 school year and terminate at ' \
               'the end of the 2021-2022 school year, to include anything amended, rescinded, or renewed with the ' \
               'approval of the District of Innovation Committee (DOI), the District Continuous Improvement Team (' \
               'DCIT) and the Board of Trustees. The DOI committee will review the Plan annually, and as needed, ' \
               'to confirm consistent alignment with the needs of the District.'
        start_date, phrase, p = extract_dates.get_term_date_and_phrase(test, output_dir)
        self.assertEqual(2017, start_date)
        self.assertIsNotNone(phrase)
        self.assertLess(.5, p)

        test = 'hello'
        start_date, phrase, p = extract_dates.get_term_date_and_phrase(test, output_dir)
        self.assertEqual(-999, start_date)
        self.assertEqual('', phrase)
        self.assertEqual(0, p)

        test = 'ECISD District of Innovation Plan 1 I. Introduction House Bill 1842, passed during the 84th ' \
               'Legislative Session, permits Texas public school districts to become Districts of Innovation and to ' \
               'obtain exemption from certain provisions of the Texas Education Code. The plan will begin in 2017.'
        start_date, phrase, p = extract_dates.get_term_date_and_phrase(test, output_dir)
        self.assertEqual(2017, start_date)
        print(p)
        print(phrase)


