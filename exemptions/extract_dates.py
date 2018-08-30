import en_core_web_sm
import re
import spacy
from spacy.matcher import Matcher



def get_term_date_and_phrase(text, output_dir):
    phrases = get_phrase_list(text)
    cats = get_p_cats(phrases, output_dir=output_dir)
    max_cat_loc, p_term = get_max_p_from_dict_list(cats)
    if max_cat_loc != -999:
        start_date = get_earliest_date(phrases[max_cat_loc])
        phrase = phrases[max_cat_loc]
    if max_cat_loc == -999:
        start_date = -999
        phrase = ''
        p_term = 0
    if start_date in range(2020, 2024):
        start_date -= 5
    return start_date, phrase, p_term

def get_finalize_month_year_phrase(text, output_dir):
    max_year_phrases = []
    years = []
    months = []
    phrases = get_phrase_list(text)
    year = -999
    month = ''
    date_phrase = ''
    if phrases:
        p_cats = get_p_cats(phrases, output_dir)
        narrowed_phrases = narrow_phrase_list(phrases_list= phrases, p_dict_list= p_cats)
        if narrowed_phrases:
            for phrase in narrowed_phrases:
                year, month = get_latest_month_year_pair(phrase)
                years.append(year)
                months.append(month)
            max_year = max(years)
            i = 0
            new_months = []
            for year in years:
                if year == max_year:
                    max_year_phrases.append(narrowed_phrases[i])
                    new_months.append(months[i])
                i = i + 1
            max_month = get_latest_month(new_months)
            date_phrase = max_year_phrases[new_months.index(max_month)]
    return year, month, date_phrase


def get_phrase_list(text, n_tokens_before=8, n_tokens_after=6):
    nlp = en_core_web_sm.load()
    doc = nlp(text)
    phrases = []
    for token in doc:
        bad_match = re.findall('\.', token.text)
        if not bad_match and len(token) == 4:
            date = re.findall('\d\d\d\d', token.text)
            if date:
                i = token.i
                start = i - n_tokens_before
                if start < 0:
                    start = 0
                while doc[start].ent_iob_ == 'I':
                    start = start - 1
                end = i + n_tokens_after
                if end >= len(doc):
                    end = len(doc) - 1
                while end < len(doc) and doc[end].ent_iob_ == 'I':
                    end = end + 1
                phrase = doc[start:end]
                phrases.append(phrase)
                phrases = [str(item) for item in phrases]
    return phrases

def get_p_cats(phrases_list, output_dir):
    nlp = spacy.load(output_dir)
    cats = []
    for phrase in phrases_list:
        doc = nlp(phrase)
        cats.append(doc.cats)
    return cats

def narrow_phrase_list(phrases_list, p_dict_list):
    new_p_list = []
    phrases_narrowed = []
    [new_p_list.append([float(value) for value in item.values()]) for item in p_dict_list]
    new_p_list = [item for sublist in new_p_list for item in sublist]
    for p, phrase in zip(new_p_list, phrases_list):
        if p > .55:
            phrases_narrowed.append(phrase)
    return phrases_narrowed

#TODO make more like narrow phrase_list - return phrase and probability
def get_max_p_from_dict_list(list):
    new_list = []
    if list:
        [new_list.append([float(value) for value in item.values()]) for item in list]
        new_list = [item for sublist in new_list for item in sublist]
        if new_list:
            max_p = max(new_list)
            max_loc = new_list.index(max_p)
    if not list:
        max_loc = -999  # TODO change to missing
        max_p = -999
    return max_loc, max_p


def get_earliest_date(phrase):
    nlp = en_core_web_sm.load()
    dates = []
    for token in nlp(phrase):
        date = re.findall('\d\d\d\d', token.text)
        if date and len(token.text) == 4:
            dates.append(date)
    dates = [int(item) for sublist in dates for item in sublist]
    start_date= min(dates)
    return start_date

def get_latest_date(phrase):
    nlp = en_core_web_sm.load()
    dates = []
    for token in nlp(phrase):
        date = re.findall('\d\d\d\d', token.text)
        if date and len(token.text) == 4:
            dates.append(date)
    dates = [int(item) for sublist in dates for item in sublist]
    final_date= max(dates)
    return final_date

def get_latest_month_year_pair(phrase):
    nlp = en_core_web_sm.load()
    max_year = -999
    month = ''
    doc = nlp(phrase)
    if doc.ents:
        for entity in doc.ents:
            year = get_years(str(entity))
            if year:
                year = int(year[0])
                if year > max_year:
                    max_year = year
                    month = get_latest_month(get_months(str(entity)))
    return max_year, month


def get_months(phrase):
    nlp = en_core_web_sm.load()
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
              'November', 'December', 'Spring', 'Fall', 'Winter', 'Summer']
    month_shape_patterns = [[{'ORTH': month}] for month in months]
    matcher = Matcher(nlp.vocab)
    matcher.add("month", None, *month_shape_patterns)
    doc = nlp(phrase)
    matches = matcher(doc)
    if matches:
        months = list(set([str(doc[i[1]:i[2]][0]) for i in matches]))
    if not matches:
        months = []
    return months

def get_latest_month(month_list):
    subs = {'January': 1, 'February':2, 'March':3, 'April': 4, 'May': 5, 'June': 6, 'July': 7, 'August': 8,
            'September': 9, 'October': 10, 'November': 11, 'December': 12,
            'Spring': 13, 'Summer': 14, 'Fall': 15, 'Winter': 16}
    value_list = []
    if month_list:
        for m in month_list:
            value_list.append(subs[m])
        loc = value_list.index(max(value_list))
        month = str(month_list[loc])
    if not month_list:
        month = ''
    return month

def get_years(phrase):
    nlp = en_core_web_sm.load()
    years = ['2015', '2016', '2017', '2018', '2019', '2020']
    year_shape_patterns = [[{'ORTH': year}] for year in years]
    matcher = Matcher(nlp.vocab)
    matcher.add("month", None, *year_shape_patterns)
    doc = nlp(phrase)
    matches = matcher(doc)
    return list(set([str(doc[i[1]:i[2]][0]) for i in matches]))
