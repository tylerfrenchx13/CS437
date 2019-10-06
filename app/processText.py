import time
import csv
import pandas as pd
import string
from collections import Counter
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
stopWords = set(stopwords.words('english'))
ps = PorterStemmer()
#table = str.maketrans({key: None for key in string.punctuation})
myStopwords = {"''", '``', '“', '”', '’', "'s"}

NUM_DOCS = 100000
CHUNKSIZE = 1000
ITER_PROP = CHUNKSIZE / NUM_DOCS
NUM_ITERS = NUM_DOCS / CHUNKSIZE

def readCounts():
    gatheredIndexes = {}
    with open('tokens.csv', 'r', encoding='utf8') as f:
        for index, row in enumerate(csv.reader(f)):
            index += 1
            for token in row:
                if token not in gatheredIndexes:
                    gatheredIndexes.update({token: []})
                gatheredIndexes[token].append(index)

    invertedIndex = {}
    for word in sorted(gatheredIndexes.keys()):
        invertedIndex[word] = gatheredIndexes[word]

    with open('term_doc_freq.tsv', 'w', encoding='utf8') as f:
        for term in invertedIndex:
            f.write("{0}\t".format(term))
            countFrequency = Counter(invertedIndex[term])
            for index, key in enumerate(countFrequency):
                if index > 0:
                    f.write("\t")
                f.write("{0}:{1}".format(key, countFrequency[key]))
            f.write("\n")


def tokenize():
    mid_time = time.time()
    TOT_TIME = 0
    with open('tokens.csv', 'w', encoding='utf8') as f, open('../wikipedia_text_files.csv', 'r', encoding='utf8') as src:
        for i, chunk in enumerate(pd.read_csv(src, chunksize=CHUNKSIZE, nrows=NUM_DOCS)):
            mid_time = time.time()
            for row in chunk.itertuples():
                #title = row[2]
                index = row[3]
                content = row[1]
                content = content.lower()
                tokenized = word_tokenize(content)
                noStopwords = [token for token in tokenized if not token in stopWords and not token in string.punctuation and not token in myStopwords]
                stemmed = [ps.stem(word) for word in noStopwords]
                
                for index, token in enumerate(stemmed):
                    if index > 0:
                        f.write(",")
                    f.write("{0}".format(token))
                f.write("\n")
            pace = round(time.time() - mid_time, 3)
            TOT_TIME += pace
            AVG_PACE = (TOT_TIME/(i+1))
            print("Iteration took {0} seconds --- {1}% Done --- Time remaining: {2} minute(s)".format(pace, 100*round(i*ITER_PROP, 3), round((AVG_PACE * (NUM_ITERS - (i+1)))/60, 3)))

def main():
    #tokenize()
    #readCounts()

start_time = time.time()

main()
print("--- {0} seconds ---".format(round(time.time() - start_time, 3)))