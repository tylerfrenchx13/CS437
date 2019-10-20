import time
import csv
import re
import pandas as pd
import string
from collections import Counter
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
words = set(nltk.corpus.words.words())
stopWords = set(stopwords.words('english'))
ps = PorterStemmer()
#table = str.maketrans({key: None for key in string.punctuation})
import sys
myStopwords = {"''", '``', '“', '”', '’', "'s"}
csv.field_size_limit(sys.maxsize)

NUM_DOCS = 100000
CHUNKSIZE = 1000
ITER_PROP = 1 / NUM_DOCS

def writeMetadata():
	with open('metadataFinal0.tsv', 'w', encoding='utf8') as fmeta:
		for num in range(0, 17):
			with open('tokens/tokens{0}.csv'.format(num), 'r', encoding='utf8') as ftokens:
				print("tokens{0}.csv".format(num))
				for index, row in enumerate(csv.reader(ftokens)):
					if not row:
						fmeta.write("\n")
						continue
					index = (index + 1) + (100000*num)
					wordCount = len(row)
					maxD = sorted(Counter(row).values(), reverse=True)[0]
					fmeta.write("{0}\t{1}\t{2}\n".format(index, wordCount, maxD))

def writeDocTermFreq():
	with open('doc_term_freqFinal0.tsv', 'w', encoding='utf8') as fdocterm:
		for num in range(0, 17):
			with open('tokens/tokens{0}.csv'.format(num), 'r', encoding='utf8') as ftokens:
				print("tokens{0}.csv".format(num))
				for index, row in enumerate(csv.reader(ftokens)):
					countFrequency = Counter(row)
					for index, key in enumerate(countFrequency):
						if index > 0:
							fdocterm.write("\t")
						fdocterm.write("{0}:{1}".format(key, countFrequency[key]))
					fdocterm.write("\n")

def writeTermDocFreq():

	tokenDict = {}

	for num in range(0, 17):
		print("Reading tokens{0}".format(num))
		with open('tokens/tokens{0}.csv'.format(num), 'r', encoding='utf8') as f:
			for row in csv.reader(f):
				for token in row:
					#token = ''.join(e for e in token if e.isalnum())
					token = re.sub('[^A-Za-z0-9]+', '', token)
					#print(token)
					if token != '' and token not in tokenDict:
						tokenDict[token] = 0
	tokenDict = sorted(tokenDict)
	
	"""
	with open('tokenList.csv', 'w', encoding='utf8') as f:
		for index, token in enumerate(tokenDict):
			f.write("{0}".format(token))
			if index < len(tokenDict) - 1:
				f.write(",")
	
	with open('tokenList.csv', 'r', encoding='utf8') as f:
		reader = csv.reader(f)
		tokens = next(reader)
		for token in tokens:
			tokenDict[token] = {}
	"""

	doneFlag = False
	while not doneFlag:
		idx = idx * 10000
		endIdx = idx + 10000
		if len(tokenDict) - idx < 10000:
			endIdx = len(tokenDict)
			doneFlag = True

		tokenDict = {k:tokenDict[k] for k in list(tokenDict)[idx:endIdx]}
		
		for num in range(0, 17):
			print("Reading tokens{0}".format(num))
			with open('tokens/tokens{0}.csv'.format(num), 'r', encoding='utf8') as f:
				for index, row in enumerate(csv.reader(f)):
					count = Counter(row)
					for c in count:
						if c in tokenDict:
							tokenDict[c][(index+1)+(100000*num)] = count[c]

		with open('term_doc_freqFinal0.tsv', 'w', encoding='utf8') as f:
			for token in tokenDict:
				f.write("{0}\t".format(token))
				for index, doc in enumerate(tokenDict[token]):
					if index > 0:
						f.write("\t")
					f.write("{0}:{1}".format(doc, tokenDict[token][doc]))
				f.write("\n")
	

def isEnglish(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True

def tokenize(fileNum):
	mid_time = time.time()
	TOT_TIME = 0

	headers = ['content', 'title', 'id']
	with open('splitWiki/wiki{0}.tsv'.format(fileNum), 'r', encoding='utf8') as src, open('tokens/tokens{0}.csv'.format(fileNum), 'w', encoding='utf8') as f:
		reader = csv.reader(src, delimiter='\t')

		for i, line in enumerate(reader):
			mid_time = time.time()

			lowered = line[1].lower()
			tokenized = word_tokenize(lowered)
			noStopwords = [token for token in tokenized if not token in stopWords and not token in myStopwords and token not in string.punctuation and isEnglish(token)]
			stemmed = [ps.stem(word) for word in noStopwords]
				
			for index, token in enumerate(stemmed):
				if index > 0:
					f.write(",")
				f.write("{0}".format(token))
			f.write("\n")

			pace = round(time.time() - mid_time, 3)
			TOT_TIME += pace
			AVG_PACE = (TOT_TIME/(i+1))
			print("Iteration took {0} seconds --- {1}% Done --- Time remaining: {2} minute(s)".format(pace, 100*round(i*ITER_PROP, 3), round((AVG_PACE * (NUM_DOCS - (i+1)))/60, 3)))

def main():
	
	"""
	for num in range(0, 17):
		start_time = time.time()
		tokenize(num)
		print("--- {0} seconds ---".format(round(time.time() - start_time, 3)))
	"""

	#combineMatrices()
	writeTermDocFreq()
	#writeDocTermFreq()
	#writeMetadata()

main()
