from pathlib import Path
import pandas as pd
import spacy
from spacy import displacy
from spacy.matcher import Matcher
from functools import reduce
import re
import pickle
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import MultiLabelBinarizer
import en_core_web_sm

nlp = spacy.load('en_core_web_sm')
law_shapes = [i*'d' + '.' + j*'d' + k*'x' for i in range(1, 4) for j in range(3,5) for k in range(3)]
law_shape_patterns = [[{'SHAPE':shape}, {'ORTH':'%', 'OP':'!'}] for shape in law_shapes] # could add {'SHAPE':'§', 'OP':'*'},

matcher = Matcher(nlp.vocab)
matcher.add("ExplicitLaw", None, *law_shape_patterns)

def get_matches(string):
    doc = nlp(string)
    matches = matcher(doc)
    return list(set([doc[i[1]:i[2]][0] for i in matches]))

def get_laws(string):
    matches = get_matches(string)
    laws = []
    for match in matches:
        law = re.sub('[^0-9\.]','', match.text)
        laws.append(float(law))
    return laws