import en_core_web_sm
import re
import spacy


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

def get_finalize_date_and_phrase(text, output_dir):
    phrases = get_phrase_list(text)
    cats = get_p_cats(phrases, output_dir=output_dir)
    max_cat_loc, p_term = get_max_p_from_dict_list(cats)
    if max_cat_loc != -999:
        finalize_date = get_latest_date(phrases[max_cat_loc])
        phrase = phrases[max_cat_loc]
    if max_cat_loc == -999:
        finalize_date = -999
        phrase = ''
        p_term = 0
    if finalize_date == 2020 or finalize_date == 2021 or finalize_date == 2022 or finalize_date == 2023:
        finalize_date = finalize_date - 5
    return finalize_date, phrase, p_term


# TODO change number of tokens to sentence
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