import re
from typing import List

import spacy
from spacy.matcher import Matcher


nlp = spacy.load('en_core_web_sm')
law_shapes = [i * 'd' + '.' + j * 'd' + k * 'x' for i in range(1, 4) for j in range(3,5) for k in range(3)]
law_shapes.extend([shape + i * '(' + j * 'x' + k * 'd' for shape in law_shapes for i in range(2) for j in range(2) for k in range(2)])
law_shape_patterns = [[{'SHAPE': shape}, {'ORTH': '%', 'OP': '!'}] for shape in law_shapes] # could add {'SHAPE':'§', 'OP':'*'},

matcher = Matcher(nlp.vocab)
matcher.add("ExplicitLaw", None, *law_shape_patterns)

def get_matches(string):
    doc = nlp(string)
    matches = matcher(doc)
    return list(set([doc[i[1]:i[2]][0] for i in matches]))

def get_laws(string) -> List[str]:
    matches = get_matches(string)
    laws = []
    for match in matches:
        law = re.sub('[^0-9\.]','', match.text)
        laws.append(float(law))
    if len(laws) > 30: #unlikely just noting innovative laws if laws > 30. Better to add these manually.
        laws = []
    return laws