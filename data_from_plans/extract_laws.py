import re
from typing import List, Set

import spacy
from spacy.matcher import Matcher


nlp = spacy.load('en_core_web_sm')
law_shapes = [i * 'd' + '.' + j * 'd' + k * 'x' for i in range(2, 3) for j in range(3,5) for k in range(3)]
law_shapes.extend([shape + i * ')' +  m * '(' + n * 'X' + j * 'x' + k * 'd' for shape in law_shapes for i in range(2) for m in range(2) for n in range(2) for j in range(2) for k in range(2)])
law_shapes.extend([shape + i * '(' + j * 'x' + k * 'd' for shape in law_shapes for i in range(2) for j in range(2) for k in range(2)])
law_shapes.append('XXXdd.dddd')
law_shapes.append('xxxdd.dddd')
law_shapes.append('XXXdd.ddd')
law_shapes.append('xxxdd.ddd')
law_shapes.append('XXX§dd.ddd')
law_shapes.append('XXX§dd.dddd')
law_shapes.append('xxx§dd.ddd')
law_shapes.append('xxx§dd.dddd')
law_shapes.append('§dd.ddd')
law_shapes.append('§dd.dddd')
law_shapes.append('dd.ddd)(XXX')
law_shapes.append('dd.ddd)(XX')
law_shapes.append('dd.dddd)(XXX')
law_shapes.append('dd.dddd)(XX')
law_shapes.append('dd.ddd)(XXX')
law_shapes.append('dd.dddd)(XXX')



law_shape_patterns = [[{'SHAPE': shape}, {'ORTH': '%', 'OP': '!'}] for shape in law_shapes] # could add {'SHAPE':'§', 'OP':'*'},

matcher = Matcher(nlp.vocab)
matcher.add("ExplicitLaw", None, *law_shape_patterns)

def get_matches(string: str) -> List[Set[str]]:
    """
    Args:
        string:

    Returns:

    """
    doc = nlp(string)
    matches = matcher(doc)
    return list(set([doc[i[1]:i[2]][0] for i in matches]))

def get_laws(string: str) -> List[str]:
    """
    Extract the laws that match a pattern within a string.

    Args:
        string: The string in which to search

    Returns:
        A list of string laws matching in the text -- no more than 30!
    """
    matches = get_matches(string)
    laws = []
    for match in matches:
        law = re.sub('[^0-9\.]','', match.text)
        if law != '39.054':
            laws.append(float(law))
    if len(set(laws)) > 30: #unlikely just noting innovative laws if laws > 30. Better to add these manually.
        laws = []
    laws = list(set(laws))
    return laws
