from unittest import TestCase
from exemptions import extract_dates

class TestGet_months(TestCase):
    def test_get_months(self):
        test = "District of Innovation - Wylie Independent School District PDF Links Curriculum & Instruction STAAR/EOC STAAR Test FAQ Early Childhood Guidelines TEKS for English Language Arts TEKS for Mathematics TEKS for Science TEKS for Social Studies TEKS for Health Education TEKS for Physical Education TEKS for Fine Arts TEKS for Technology Applications TEKS for Spanish Language Arts Health Services Immunization Requirements Medication at School Health and Athletic Forms Sick or Well?? Health Links Campus Screenings Human Resources Employment Information Information for Substitutes New Employee Videos Job Descriptions Student Services Notice of Intent to Destroy Texas Transition and Employment Guide Autism Strategy Guide  Immunization Requirements Medication at School H District of Innovation District of Innovation Wylie Independent School District 6251 Buffalo Gap RD, Abilene, TX 79606Phone (325) 692-4353 | Fax (325) 695-3438 Facebook Page Website by SchoolMessenger Presence. © 2018 West Corporation. All rights reserved."
        list = extract_dates.get_months(test)
        print(list)

        text = 'and the community. On February 28, 2017, the Board appointed an eighteen members. March'
        list = extract_dates.get_months(text)
        self.assertIn('February', list)
        self.assertIn('March', list)

        text = 'local business owners. On January 17, 2017, the District Education Improvement Committee.'
        list = extract_dates.get_months(text)
        self.assertIn('January', list)
        self.assertEqual(1, len(list))

        text = 'and the community.'
        list = extract_dates.get_months(text)
        self.assertEqual(0, len(list))

        text = ''
        list = extract_dates.get_months(text)
        self.assertEqual(0, len(list))
