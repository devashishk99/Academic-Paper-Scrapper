from string import punctuation  # gets the string of punctuations
from textblob import TextBlob as tb  # library for processing textual data
from nltk.corpus import stopwords  # gets stopwords from nltk library
import math

class Tfidf:
    """
    The Tfidf Class takes in the list of documents as 
    input in order to create the object instance. 
    """
    def __init__(self, docs):
        self.docs = docs # sets the docs variable with list of documents
    
    # the term frequency function
    def _tf(self, word, doc):
        lenOfDoc = len(doc.words) # gets length of documents which is a textblob i.e no of words
        if lenOfDoc < 1: 
            return 0
        else: 
            return doc.words.count(word) / lenOfDoc # calculates the frequency of the words in the document
        
    # function to check if document contains the word
    def _contains(self, word, docs):
        return sum(1 for doc in docs if word in doc.words) # checks if words is present in the document and returns the count of it

    # the inverse document frequency function
    def _idf(self, word, docs):
        docsCount = self._contains(word, docs) # stores the count of documents containing the given word
        if docsCount < 1: 
            return 0
        else: 
            return math.log(len(docs) / docsCount) # calculates log of length of documents divided by the documents containing the word

    # calculates the tf-idf 
    def tfidf(self):
        keyword_list = []
        for doc in self.docs: # iterating through the list of documents
            top5 = [] # list to store the top 5 keywords
            scores = {word: (self._tf(word,doc) * self._idf(word, self.docs)) for word in doc.words} # calculates the tf-idf score
            sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True) # sorts the list in descending order by the score obtained by tf-idf
            for word, score in sorted_words[:5]:
                top5.append(word) # adding keywords to the list for particular document
            keyword_list.append(top5) # list of keywords for different documents
        return keyword_list


def normalize_docs(doc_list):
    """ 
    Normalizes a list of text documents by:
    1. Removing Punctuations
    2. Removing Numbers
    3. Setting to Lowercase
    4. Removing Stopwords
    """
    normalized = []
    
    for doc in doc_list:
        # To remove punctuations
        doc = ''.join(c for c in doc if c not in punctuation)
        # To remove Numbers
        doc = ''.join(c for c in doc if not c.isdigit())
        # To set to lowercase
        doc = ''.join(c.lower() for c in doc)
        # To remove stopwords
        doc = ' '.join(word for word in doc.split() if word not in (stopwords.words('english')))
        # append to normalised list
        normalized.append(tb(doc))
        
    return normalized

def get_keywords(doc_list):
    """
    Based on the input document list returns
    the keywords based on the tf-idf algorithm.
    """
    doc_list = normalize_docs(doc_list) # cleans the data aka preprocessing step
    text_docs = Tfidf(doc_list) # initialzes the tfidf class object with list of documents
    keywords = text_docs.tfidf() # gets top 5 keywords for every document
    return keywords