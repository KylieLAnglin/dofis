from unittest import TestCase
import pandas as pd
from dofis.merge_and_clean.library import clean_for_merge


class TestResolve_unicode_problems(TestCase):
    def test_resolve_unicode_problems(self):
        test = 'Bronte\xa0ISD'
        d = {'distname': [test, 'Abbott ISD']}
        df = pd.DataFrame(data=d)
        df = clean_for_merge.resolve_unicode_problems(df, 'distname')
        result = df[df.distname.str.startswith('Bronte')]['distname'].values[0]
        result2 = df[df.distname.str.startswith('Abbott')]['distname'].values[0]
        self.assertEqual('Bronte ISD', result)
        self.assertEqual('Abbott ISD', result2)

class TestStrip_distnum_parens(TestCase):
    def test_strip_distnum_parens(self):
        str_list = ['CENTERVILLE ISD (145902)',
                     'CENTERVILLE ISD (228904)',
                     'CHAPEL HILL ISD (225906)',
                     'EDGEWOOD ISD (015905)',
                     'EDGEWOOD ISD (234903)',
                     'HIGHLAND PARK ISD (057911)',
                     'HIGHLAND PARK ISD (188903)',
                     'HUBBARD ISD (019913)',
                     'HUBBARD ISD (109905)',
                     'MIDWAY ISD (161903)',
                     'NORTHSIDE ISD (244905)',
                     'WYLIE ISD (043914)',
                     'WYLIE ISD (221912)']
        result = clean_for_merge.strip_distnum_parens(str_list)
        self.assertEqual('CENTERVILLE ISD', result[0])

class TestSync_district_names(TestCase):
    def test_sync_district_names(self):
        d = {'distname': ['EAGLE MT-SAGINAW ISD']}
        df = pd.DataFrame(data=d)
        df = clean_for_merge.sync_district_names(df, 'distname')
        result = df[df.distname.str.startswith('E')]['distname'].values[0]
        self.assertEqual('EAGLE MOUNTAIN SAGINAW ISD', result)

class TestUppercase_column(TestCase):
    def test_uppercase_column(self):
        d = {'distname': ['Abbott ISD']}
        df = pd.DataFrame(data=d)
        df = clean_for_merge.uppercase_column(df, 'distname')
        result = df[df.distname.str.startswith('A')]['distname'].values[0]
        self.assertEqual('ABBOTT ISD', result)

