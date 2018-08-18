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

nlp = en_core_web_sm.load()