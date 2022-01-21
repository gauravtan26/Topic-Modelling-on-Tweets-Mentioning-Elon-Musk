import pandas as pd
import unicodedata
import re
import contractions
import nltk
import string
import spacy

#Gensim
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel

#spacy
import spacy
from nltk.corpus import stopwords

#vis
import pyLDAvis
import pyLDAvis.gensim_models


def load_data(file):
    return pd.read_csv(file)

def get_number_of_links(documents):
    print("{:.2f}% of documents contain links".format(sum(documents.apply(lambda x:x.find('http'))>0)/len(documents)*100))

def to_lowercase(text):
    return text.lower()

def remove_accented_chars(text):
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')

def remove_link(text):
    return re.sub(r'https?:\/\/\S*', '', text, flags=re.MULTILINE)

def expand_contractions(text):
    expanded_words = []    
    for word in text.split():
        expanded_words.append(contractions.fix(word))   
    return ' '.join(expanded_words)

def remove_mentions_and_tags(text):
    text = re.sub(r'@\S*', '', text)
    return re.sub(r'#\S*', '', text)


def keep_only_alphabet(text):
    return re.sub(r'[^a-z]', ' ', text)


def remove_stopwords(text,nlp,custom_stop_words=None,remove_small_tokens=True,min_len=2):
    if custom_stop_words:
        nlp.Defaults.stop_words |= custom_stop_words
    filtered_sentence =[] 
    doc=nlp(text)
    for token in doc:
        lexeme = nlp.vocab[token.text]    
        if lexeme.is_stop == False: 
            if remove_small_tokens:
                if len(token.text)>min_len:
                    filtered_sentence.append(token.text)
            else:
                filtered_sentence.append(token.text)
            
    return " ".join(filtered_sentence) if len(filtered_sentence)>0 else None


def lemmatize(text, nlp):
    doc = nlp(text)
    lemmatized_text = []
    for token in doc:
        lemmatized_text.append(token.lemma_)
    return " ".join(lemmatized_text)

def generate_tokens(tweet):
    words=[]
    for word in tweet.split(' '):
        if word!='':
            words.append(word)
    return words


def create_dictionary(tweets_df):
    return corpora.Dictionary(tweets_df.words)


def create_document_matrix(tokens,id2word):
    corpus = []
    for text in tokens:
        new = id2word.doc2bow(text)
        corpus.append(new)
    return corpus

