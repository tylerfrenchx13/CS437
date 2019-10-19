from math import log
import csv

import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
words = set(nltk.corpus.words.words())
stopWords = set(stopwords.words('english'))
ps = PorterStemmer()

from collections import Counter

metaFile = "text_processing/metadataFinal.tsv"
termDocFile = "text_processing/term_doc_freqFinal.tsv"
docTermFile = "text_processing/doc_term_freqFinal.tsv"
dcSize = 1662757

class RankMeUp:

	def __init__(self):
		pass

	def getTopN(self, ranks, n):
		return [i[0] for i in Counter(ranks).most_common(n)]

	def ranking(self, candidates, queryList):
		with open(metaFile, 'r', encoding="utf-8") as f1, open(docTermFile, 'r', encoding='utf8') as f2:
			metaReader = csv.reader(f1, delimiter='\t')
			docTermReader = csv.reader(f2, delimiter='\t')
			candidateRank = {}
			curLine = 0
			metaLine = None
			docTermLine = None

			for candidate in candidates[0]:
				# Iterate until we reach the right line!
				## THIS TAKES A WHILE- Iterating through both metadata and docTerm
				## to get to the right document number
				#---------------------------------------
				while curLine != candidate:
					metaLine = next(metaReader)
					docTermLine = next(docTermReader)
					curLine += 1
				#---------------------------------------

				# Make sure we keep a running summation
				summation = 0

				# Calculations for future formula use
				maxD = int(metaLine[2])
				docLength = int(metaLine[1])

				# For every word in our query list, use the formula to calculate the ranking score for each candidate
				for word in queryList:
					IDF = log(dcSize / candidates[1][word], 2)
					wordCount = int(docTermLine[[idx for idx, s in enumerate(docTermLine) if word in s][0]].split(':')[1])
					TF = (wordCount / docLength) / maxD
					summation += TF * IDF

				candidateRank[candidate] = summation

		return candidateRank

	def findCandidates(self, queryList):
		with open(termDocFile, 'r', encoding='utf8') as f:
			fileReader = csv.reader(f, delimiter='\t')

			# Get candidates
			candidates = []
			wordOccurrence = {}
			foundOne = False
			numFoundQueryWords = 0
			for row in fileReader:
				if row[0] not in queryList:
					continue

				for word in queryList:
					if row[0] == word:
						numFoundQueryWords += 1
						wordOccurrence[word] = len(row) - 1
						newDocs = []

						for doc in row[1:len(row) - 1]:
							candidates.append(int(doc.split(':')[0]))

						break
				if numFoundQueryWords == len(queryList):
					break

			return [candidates, wordOccurrence]

	def rankMeUpScotty(self, query):
		# Tokenize the query into a list
		lowered = query.lower()
		tokenized = word_tokenize(lowered)
		noStopwords = [token for token in tokenized if not token in stopWords and token in words]
		queryArray = [ps.stem(word) for word in noStopwords]
		print(queryArray)

		candidates = self.findCandidates(queryArray)

		ranks = self.ranking(candidates, queryArray)

		top5 = self.getTopN(ranks, 5)
		return top5