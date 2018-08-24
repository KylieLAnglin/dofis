import en_core_web_sm
import re

nlp = en_core_web_sm.load()


def get_date_phrase_list(text, n_tokens_before=8, n_tokens_after=6):
    doc = nlp(text)
    dates = []
    phrases = []
    for token in doc:
        bad_match = re.findall('\.', token.text)
        if not bad_match:
            print(token.text)
            date = re.findall('\d\d\d\d', token.text)
            if date:
                i = token.i
                start = i - n_tokens_before
                if start < 0:
                    start = 0
                end = i + (n_tokens_after + 1)
                phrase = doc[start:end]
                dates.append(str(token.text))
                phrases.append(phrase)
    phrases = [str(item) for item in phrases]
    return dates, phrases

#TODO change number of tokens to sentence
def get_phrase_list(text, n_tokens_before=8, n_tokens_after=6):
    doc = nlp(text)
    phrases = []
    for token in doc:
        bad_match = re.findall('\.', token.text)
        if not bad_match:
            date = re.findall('\d\d\d\d', token.text)
            if date:
                i = token.i
                start = i - n_tokens_before
                if start < 0:
                    start = 0
                end = i + (n_tokens_after + 1)
                phrase = doc[start:end]
                phrases.append(phrase)
                phrases = [str(item) for item in phrases]  # move to function
    return phrases


def get_max_p_from_dict_list(list):
    new_list = []
    if list:
        [new_list.append([float(value) for value in item.values()]) for item in list]
        new_list = [item for sublist in new_list for item in sublist]
        max_loc = new_list.index(max(new_list))
    if not list:
        max_loc = -999 #TODO change to missing
    return max_loc
