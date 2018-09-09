import en_core_web_sm
import re
import spacy
from spacy.matcher import Matcher


def get_finalize_month_year_phrase(text, output_dir):
    max_year_phrases, max_year_months, years, months, narrowed_cats = [], [], [], [], []
    year, max_year = -999, -999
    max_p = 0
    month, date_phrase, max_month = '', '', ''
    phrases = get_phrase_list(text)
    if phrases:  # phrases not None --> means a document contains years
        narrowed_phrases, cats = narrow_phrase_list(phrases, output_dir)  # dates likely to be finalized TODO add cats
        if narrowed_phrases:

            # Append month and year from likely finalization dates to years and months
            for phrase in narrowed_phrases:
                year, month = get_latest_month_year_pair(phrase)  # gets most recent month + year
                years.append(year)
                months.append(month)
            max_year = max(years) # maximum year from narrowed phrases
            i = 0
            for year, month, p in zip(years, months, cats):
                if year == max_year: #just keep phrases and months with latest year
                    max_year_phrases.append(narrowed_phrases[i])
                    max_year_months.append(months[i])
                    narrowed_cats.append(p)
                i = i + 1
            if max_year_months:
                max_month = get_latest_month(max_year_months) # max month from phrases with max year
                date_phrase = max_year_phrases[max_year_months.index(max_month)]
                max_p = narrowed_cats[max_year_months.index(max_month)]
            if not max_year_months:
                date_phrase = max_year_phrases[max_year_phrases.index(max_year)]
    return max_year, month, date_phrase, max_p


def get_term_date_and_phrase(text, output_dir):
    start_date = -999
    p = 0
    phrase = ''
    phrases = get_phrase_list(text)
    if phrases:
        max_phrase, p = narrow_phrase_list(phrases, output_dir, just_max= True)
        p = p[0]
        if max_phrase:
            start_date = get_earliest_date(max_phrase[0])
            phrase = max_phrase[0]
    month = get_earliest_month_year_pair(phrase)
    return start_date, month, phrase, p


def get_phrase_list(text, n_tokens_before=8, n_tokens_after=6):
    nlp = en_core_web_sm.load()
    phrases = []
    if text:
        doc = nlp(text)
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
                        if start > 0:
                            start = start - 1
                    end = i + n_tokens_after
                    while end < len(doc)  and doc[end].ent_iob_ == 'I':
                        end = end + 1
                    phrase = doc[start:end]
                    phrase = doc[start:end]
                    phrases.append(phrase)
                    phrases = [str(item) for item in phrases]
    return phrases


def narrow_phrase_list(phrases_list, output_dir, just_max = False, min_p = .6):
    nlp = spacy.load(output_dir)
    cats = []
    phrases_narrowed, narrowed_cats, clean_cats = [], [], []
    for phrase in phrases_list:
        doc = nlp(phrase)
        cats.append(doc.cats)
    if cats:
        # cats is list of dictionaries, take values and turn to a single list
        [clean_cats.append([float(value) for value in item.values()]) for item in cats]
        clean_cats = [item for sublist in clean_cats for item in sublist]
        narrowed_cats = []
        if not just_max:
            for p, phrase in zip(clean_cats, phrases_list):
                if p > min_p:
                    phrases_narrowed.append(phrase)
                    narrowed_cats.append(p)
        if just_max:
            phrases_narrowed.append(phrases_list[clean_cats.index(max(clean_cats))])
            narrowed_cats.append(max(clean_cats))
    return phrases_narrowed, narrowed_cats


def get_earliest_date(phrase):
    nlp = en_core_web_sm.load()
    dates, years = [], []
    start_date = -999
    if phrase:
        for token in nlp(phrase):
            date = re.findall('\d\d\d\d', token.text)
            if date and len(token.text) == 4:
                dates.append(date)
        dates = [int(item) for sublist in dates for item in sublist]
        for year in dates:
            if year > 2014: #date can only be after 2014
                years.append(year)
            if years:
                start_date = min(years)
                if start_date == 2021 or start_date == 2022:
                    start_date = start_date - 5
    return start_date

def get_earliest_month_year_pair(phrase):
    min_year = 999
    month = ''
    years = get_years(phrase)
    months = get_months(phrase)
    if years and months:
        min_year = int(years[0])
        month = months[0]
    if len(years) > 1 or len(months) > 1:
        nlp = en_core_web_sm.load()
        if phrase:
            doc = nlp(phrase)
            if doc.ents:
                for entity in doc.ents:
                    year = get_years(str(entity))
                    if year:
                        year = int(year[0])
                        if year <= min_year:
                            min_year = year
                            new_months = get_months(str(entity))
                            for m in new_months:
                                months.append(m)
                    if months:
                        month = get_earliest_month(months)
    return min_year, month


def get_latest_month_year_pair(phrase):
    max_year = -999
    month = ''
    years = get_years(phrase)
    months = get_months(phrase)
    if years and months:
        max_year = int(years[0])
        month = months[0]
    if len(years) > 1 or len(months) > 1:
        nlp = en_core_web_sm.load()
        if phrase:
            doc = nlp(phrase)
            if doc.ents:
                for entity in doc.ents:
                    year = get_years(str(entity))
                    if year:
                        year = int(year[0])
                        if year >= max_year:
                            max_year = year
                            new_months = get_months(str(entity))
                            for m in new_months:
                                months.append(m)
                    if months:
                        month = get_latest_month(months)
    return max_year, month


def get_latest_month(month_list):
    month = ''
    subs = {'Spring': 1, 'Summer': 2, 'Fall': 3, 'Winter': 4,
            'January': 5, 'February': 6, 'March': 7, 'April': 8, 'May': 9, 'June': 10, 'July': 11,
            'August': 12, 'September': 13, 'October': 14, 'November': 15, 'December': 16}
    value_list = []
    if month_list:
        for m in month_list:
            value_list.append(subs.get(m, 0))
        loc = value_list.index(max(value_list))
        month = str(month_list[loc])
    return month


def get_earliest_month(month_list):
    month = ''
    subs = {'Spring': 1, 'Summer': 2, 'Fall': 3, 'Winter': 4,
            'January': 5, 'February': 6, 'March': 7, 'April': 8, 'May': 9, 'June': 10, 'July': 11,
            'August': 12, 'September': 13, 'October': 14, 'November': 15, 'December': 16}
    value_list = []
    if month_list:
        for m in month_list:
            value_list.append(subs.get(m, 0))
        loc = value_list.index(min(value_list))
        month = str(month_list[loc])
    return month


def get_months(phrase):
    nlp = en_core_web_sm.load()
    months = []
    month_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
              'November', 'December', 'Spring', 'Fall', 'Winter', 'Summer']
    month_shape_patterns = [[{'ORTH': month}] for month in month_list]
    matcher = Matcher(nlp.vocab)
    matcher.add("month", None, *month_shape_patterns)
    if phrase:
        doc = nlp(phrase)
        matches = matcher(doc)
        if matches:
            months = list(set([str(doc[i[1]:i[2]][0]) for i in matches]))
    return months


def get_years(phrase):
    years = []
    nlp = en_core_web_sm.load()
    year_shapes = ['2015', '2016', '2017', '2018', '2019', '2020']
    year_shape_patterns = [[{'ORTH': year}] for year in year_shapes]
    matcher = Matcher(nlp.vocab)
    matcher.add("month", None, *year_shape_patterns)
    if phrase:
        doc = nlp(phrase)
        matches = matcher(doc)
        years = list(set([str(doc[i[1]:i[2]][0]) for i in matches]))
    return years
