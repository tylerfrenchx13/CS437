import time
import csv
import pandas as pd
#import string
from collections import Counter
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
words = set(nltk.corpus.words.words())
stopWords = set(stopwords.words('english'))
ps = PorterStemmer()
#table = str.maketrans({key: None for key in string.punctuation})
#myStopwords = {"''", '``', '“', '”', '’', "'s"}

NUM_DOCS = 100000
CHUNKSIZE = 1000
ITER_PROP = CHUNKSIZE / NUM_DOCS
NUM_ITERS = NUM_DOCS / CHUNKSIZE

def writeMetadata():
	with open('metadataFinal.tsv', 'w', encoding='utf8') as fmeta:
		for num in range(0, 17):
			with open('tokens{0}.csv'.format(num), 'r', encoding='utf8') as ftokens:
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
	with open('doc_term_freqFinal.tsv', 'w', encoding='utf8') as fdocterm:
		for num in range(0, 17):
			with open('tokens{0}.csv'.format(num), 'r', encoding='utf8') as ftokens:
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

	"""
	for num in range(0, 17):
		print("Reading tokens{0}".format(num))
		with open('tokens{0}.csv'.format(num), 'r', encoding='utf8') as f:
			for row in csv.reader(f):
				for token in row:
					if token not in tokenDict:
						tokenDict[token] = 0
	tokenDict = sorted(tokenDict)
	"""

	"""
	with open('tokenList.csv', 'w', encoding='utf8') as f:
		for index, token in enumerate(tokenDict):
			f.write("{0}".format(token))
			if index < len(tokenDict) - 1:
				f.write(",")
	"""

	with open('tokenList.csv', 'r', encoding='utf8') as f:
		reader = csv.reader(f)
		tokens = next(reader)
		for token in tokens:
			tokenDict[token] = {}
	
	tokenDict = {k:tokenDict[k] for k in list(tokenDict)[60000:len(tokenDict)]}
	
	for num in range(0, 17):
		print("Reading tokens{0}".format(num))
		with open('tokens{0}.csv'.format(num), 'r', encoding='utf8') as f:
			for index, row in enumerate(csv.reader(f)):
				count = Counter(row)
				for c in count:
					if c in tokenDict:
						tokenDict[c][(index+1)+(100000*num)] = count[c]

	with open('term_doc_freqFinal0.tsv', 'a', encoding='utf8') as f:
		for token in tokenDict:
			f.write("{0}\t".format(token))
			for index, doc in enumerate(tokenDict[token]):
				if index > 0:
					f.write("\t")
				f.write("{0}:{1}".format(doc, tokenDict[token][doc]))
			f.write("\n")

def tokenize(fileNum):
	mid_time = time.time()
	TOT_TIME = 0

	headers = ['content', 'title', 'id']
	dtypes = {'content': 'str', 'title': 'str', 'id': 'float'}
	with open('../wikipedia_text_files.csv', 'r', encoding='utf8') as src, open('tokens{0}.csv'.format(fileNum), 'w', encoding='utf8') as f:
		for i, chunk in enumerate(pd.read_csv(src, header=None, names=headers, dtype=dtypes, chunksize=CHUNKSIZE, nrows=NUM_DOCS, skiprows=NUM_DOCS*fileNum)):
			mid_time = time.time()
			for row in chunk.itertuples():
				#title = row[2]
				#index = row[3]
				content = str(row[1])
				content = content.lower()
				tokenized = word_tokenize(content)
				noStopwords = [token for token in tokenized if not token in stopWords and token in words]
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
	"""
	for num in range(4, 17):
		start_time = time.time()
		tokenize(num)
		print("--- {0} seconds ---".format(round(time.time() - start_time, 3)))
	"""
	#combineMatrices()
	#writeTermDocFreq()
	#writeDocTermFreq()
	writeMetadata()

main()
