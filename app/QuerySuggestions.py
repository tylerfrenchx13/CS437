import pandas as pd
import pickle
from collections import Counter
import re
from nltk.corpus import stopwords
stopWords = set(stopwords.words('english'))

phrases = pickle.load(open("app/data/phrases.p", "rb"))
doc_freq = pickle.load(open("app/data/doc_freq.p", "rb"))
words = pickle.load(open("app/data/words.p", "rb"))
pciqt = pickle.load(open("app/data/pciqt.p", "rb"))
ppjci = pickle.load(open("app/data/ppjci.p", "rb"))

class QuerySuggestions:

    def __init__(self):
        pass

    def create_tokens(self, s):
        s = s.lower()
        s = re.sub(r'’', '\'', s)
        s = re.sub(r'[^a-zA-Z0-9\s\']', ' ', s)
        return [token for token in s.split(" ") if token != ""]

    def complete_words(self, s):
        return words[words['word'].str.startswith(s)]['word'].to_list()

    def remove_trailing_stopwords(self, tple):
        for i, e in reversed(list(enumerate(tple))):
            if e not in stopWords:
                break
        return tuple(list(tple)[:i+1])

    def PQcPi(self, Qc, Pi):
        if Qc not in doc_freq:
            return doc_freq[Pi]
        else:
            return doc_freq[Pi]/doc_freq[Qc]

    def GetCandidates(self, query=''):
        if len(query) < 3:
            return []
        query = query.lower()
        query = re.sub(r'’', '\'', query)
        query = re.sub(r'[^a-zA-Z0-9\s\']', ' ', query)
        candidates = {}
        tokens = self.create_tokens(query)
        orig_query = tuple(tokens)
        c_words = set()
        if not query.endswith(" "):
            partial_word = tokens[-1:]
            tokens = tokens[:-1]
            c_words = set(self.complete_words(partial_word[0]))
            c_words = c_words.difference(set(tokens)).union({partial_word[0]})
        tple = tuple(tokens)
        if len(tple) > 0:
            fixed_tple = self.remove_trailing_stopwords(tple)
        else:
            fixed_tple = tple
        st = set(tple)
        for k in phrases[phrases['join'].str.contains(query)]['word'].to_list():
            c = c_words & set(k)
            if st.issubset(k) and k!=orig_query and (len(c_words) == 0 or (c_words & set(k))):
                candidates[k] = self.PQcPi(fixed_tple,k) * ppjci[k]
                if len(c) > 0 and (list(c)[0],) in pciqt :
                    candidates[k] *= pciqt[(list(c)[0],)]
            
        sugs = Counter(candidates).most_common(10)
            
        return [' '.join(map(str, tup[0])) for tup in sugs]