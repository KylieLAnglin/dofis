from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
import gensim
from gensim import corpora


broad_stop_words = ['district', 'isd', 'innovation', 'tec', 'code', 'tec', 'state', 'local', '§', 'flexibility',
                    'education', 'texas', 'school', 'board', 'member']


stop = stopwords.words('english')
stop += broad_stop_words
exclude = set(string.punctuation)
lemma = WordNetLemmatizer()


def clean(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized

def get_dict_and_matrix(list_of_docs):
    # Creating the term dictionary of our courpus, where every unique term is assigned an index.
    dictionary = corpora.Dictionary(list_of_docs)

    # Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in list_of_docs]

    return dictionary, doc_term_matrix


def run_lda(matrix, num_topics, dictionary, passes):
    # Creating the object for LDA model using gensim library
    Lda = gensim.models.ldamodel.LdaModel

    # Running and Trainign LDA model on the document term matrix.
    ldamodel = Lda(matrix, num_topics, id2word=dictionary, passes=50)

    return ldamodel

