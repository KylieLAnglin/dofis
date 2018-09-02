from unittest import TestCase
from exemptions import extract_dates
import os
from exemptions import start

class TestGet_finalize_month_year_phrase(TestCase):
    def test_get_finalize_month_year_phrase(self):
        output_dir = os.path.join(start.data_path, 'date_finalize_classifier')

        test = "District of Innovation - Wylie Independent School District PDF Links Curriculum & Instruction STAAR/EOC STAAR Test FAQ Early Childhood Guidelines TEKS for English Language Arts TEKS for Mathematics TEKS for Science TEKS for Social Studies TEKS for Health Education TEKS for Physical Education TEKS for Fine Arts TEKS for Technology Applications TEKS for Spanish Language Arts Health Services Immunization Requirements Medication at School Health and Athletic Forms Sick or Well?? Health Links Campus Screenings Human Resources Employment Information Information for Substitutes New Employee Videos Job Descriptions Student Services Notice of Intent to Destroy Texas Transition and Employment Guide Autism Strategy Guide  Immunization Requirements Medication at School H District of Innovation District of Innovation Wylie Independent School District 6251 Buffalo Gap RD, Abilene, TX 79606Phone (325) 692-4353 | Fax (325) 695-3438 Facebook Page Website by SchoolMessenger Presence. © 2018 West Corporation. All rights reserved."
        extract_dates.get_finalize_month_year_phrase(test, output_dir)


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
        year, month, phrase, p = extract_dates.get_finalize_month_year_phrase(test, output_dir)
        self.assertEqual(2017, year)
        self.assertEqual('March', month)
        self.assertLess(.5, p)

        test2 = 'District of Innovation Committee (“Committee”) comprised of district leaders, teachers, parents, ' \
                'and community members representing a variety of roles and responsibilities.'

        year, month, phrase, p = extract_dates.get_finalize_month_year_phrase(test2, output_dir)
        self.assertEqual(-999, year)
        self.assertEqual('', month)
        self.assertEqual('', phrase)
        self.assertEqual(0, p)

        test = ''
        year, month, phrase, p = extract_dates.get_finalize_month_year_phrase(test, output_dir)
        self.assertEqual(-999, year)
        self.assertEqual('', month)
        self.assertEqual('', phrase)
        self.assertEqual(0, p)

        test = '2017'
        year, month, phrase, p = extract_dates.get_finalize_month_year_phrase(test, output_dir)
        self.assertEqual(-999, year) # -999 because filtered out - unlikely to be doi plan
        self.assertEqual('', month)
        self.assertEqual(0, p)

        test = 'ECISD District of Innovation Plan 1 I. Introduction House Bill 1842, passed during the 84th ' \
               'Legislative Session, permits Texas public school districts to become Districts of Innovation and to ' \
               'obtain exemption from certain provisions of the Texas Education Code. The plan will begin in March of 2017.'
        year, month, phrase, p = extract_dates.get_finalize_month_year_phrase(test, output_dir)
        self.assertEqual(2017, year)
        self.assertEqual('March', month)

