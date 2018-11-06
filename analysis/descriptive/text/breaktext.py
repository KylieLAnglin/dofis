import spacy
import en_core_web_sm
from spacy.matcher import Matcher

import sys
sys.path.append("../")
from library import regulations

nlp = spacy.load('en_core_web_sm')
law_shapes = [i*'d' + '.' + j*'d' + k*'x' for i in range(1, 4) for j in range(3,5) for k in range(3)]
law_shape_patterns = [[{'SHAPE':shape}, {'ORTH':'%', 'OP':'!'}] for shape in law_shapes] # could add {'SHAPE':'§', 'OP':'*'},

matcher = Matcher(nlp.vocab)
matcher.add("ExplicitLaw", None, *law_shape_patterns)

def get_phrase(text, regulation, include_similar = True):
    phrase = ''
    # Get location of regulation matches
    doc = nlp(text)
    matches = matcher(doc)
    locs = []
    for match in matches:
        locs.append(match[1])
    locs.append(len(doc) - 1)
    # Get phrases between one match and the next
    i = 0
    for loc in locs[0:-1]:
        token = doc[loc].text
        if token.startswith(regulation):
            start = locs[i]
            j = i + 1
            end = locs[j]
            if include_similar == True:
                while doc[end].text in regulations.similar[regulation]:
                    j = j + 1
                    end = locs[j]
            else:
                while doc[end].text == regulation:
                    j = j + 1
                    end = locs[j]
            phrase = phrase + "|" + str(doc[start:end])
        i = i + 1
    return phrase