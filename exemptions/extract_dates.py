import en_core_web_sm
import re
nlp = en_core_web_sm.load()


def get_date_phrase_list(text, n_tokens_before = 8, n_tokens_after = 6):
    doc = nlp(text)
    dates_phrases = []
    for token in doc:
        bad_match = re.findall('\.', token.text)
        if not bad_match:
            print(token.text)
            date = re.findall('\d\d\d\d', token.text)
            if date:
                i = token.i
                start = i - n_tokens_before
                end = i + (n_tokens_after + 1)
                phrase = doc[start:end]
                dates_phrases.append((token.text, phrase))
    return dates_phrases

def get_phrase_list(text, n_tokens_before = 8, n_tokens_after = 6):
    doc = nlp(text)
    phrases = []
    for token in doc:
        bad_match = re.findall('\.', token.text)
        if not bad_match:
            date = re.findall('\d\d\d\d', token.text)
            if date:
                i = token.i
                start = i - n_tokens_before
                end = i + (n_tokens_after + 1)
                phrase = doc[start:end]
                phrases.append(phrase)
    return phrases
