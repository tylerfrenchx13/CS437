from math import log
import csv

import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import pickle

words = set([word.lower() for word in set(nltk.corpus.words.words())])
stopWords = set(stopwords.words('english'))
ps = PorterStemmer()

from collections import Counter

metaFile = "text_processing/metadataFinal.tsv"
termDocFile = "text_processing/term_doc_freqFinal.tsv"
docTermFile = "text_processing/doc_term_freqFinal.tsv"

docTermDict = {}
metaFileDict = {}
index = 1
print("creating dict")
with open(metaFile, 'r', encoding="utf-8") as f1, open(docTermFile, 'r', encoding='utf8') as f2:
	metaReader = csv.reader(f1, delimiter='\t')
	docTermReader = csv.reader(f2, delimiter='\t')
	for row1,row2 in zip(metaReader, docTermReader):
		metaFileDict[index] = row1
		docTermDict[index] = row2
		index += 1
		if index % 10000 == 0:
			print(index)
print("docTermDict Created")



termDocDict = {}
index = 0
with open(termDocFile, 'r', encoding='utf8') as f:
	fileReader = csv.reader(f, delimiter='\t')
	for row in fileReader:
		termDocDict[row[0]] = row[1:]
		index += 1
		if index % 10000 == 0:
			print(index)
print("termDocDict Created")
print('america' in words)
print('america' in termDocDict)

dcSize = 1662757

class RankMeUp:

	def __init__(self):
		pass

	def getTopN(self, ranks, n):
		print("Geting top n")
		return [i[0] for i in Counter(ranks).most_common(n)]

	def ranking(self, candidates, queryList):
		print("start ranking")
		#with open(metaFile, 'r', encoding="utf-8") as f1, open(docTermFile, 'r', encoding='utf8') as f2:
			#metaReader = csv.reader(f1, delimiter='\t')
			#docTermReader = csv.reader(f2, delimiter='\t')
		candidateRank = {}
		curLine = 0
		metaLine = None
		docTermLine = None

		for candidate in candidates[0]:
			# Iterate until we reach the right line!
			## THIS TAKES A WHILE- Iterating through both metadata and docTerm
			## to get to the right document number
			#---------------------------------------
			#while curLine != candidate:
			#	metaLine = next(metaReader)
			#	docTermLine = next(docTermReader)
			#	curLine += 1
			#---------------------------------------
			metaLine = metaFileDict[candidate]
			docTermLine= docTermDict[candidate]
			# Make sure we keep a running summation
			summation = 0

			# Calculations for future formula use
			maxD = int(metaLine[2])
			docLength = int(metaLine[1])

			# For every word in our query list, use the formula to calculate the ranking score for each candidate
			for word in queryList:
				#print("word "  + word)
				#print(candidates[1])
				#print(docTermLine)
				IDF = log(dcSize / candidates[1][word], 2)
				wordCount = [grp.split(':')[1] for grp in docTermLine if word == grp.split(':')[0]]
				if len(wordCount) == 0:
					wordCount = 0
				else:
					wordCount = int(wordCount[0])
				#print(wordCount)
				TF = (wordCount / docLength) / maxD
				summation += TF * IDF

			candidateRank[candidate] = summation
		
		#print(candidateRank)
		return candidateRank

	def findCandidates(self, queryList):
		print("Starting findCandidates")
		#with open(termDocFile, 'r', encoding='utf8') as f:
		#	fileReader = csv.reader(f, delimiter='\t')

			# Get candidates
		candidates = set()
		wordOccurrence = {}
		foundOne = False
		numFoundQueryWords = 0
			
			#for row in fileReader:
			#	if row[0] not in queryList:
			#		continue
			
		for word in queryList:
			#		if row[0] == word:
			#			print(row[0],row[1:5])
			#			numFoundQueryWords += 1
			wordOccurrence[word] = len(termDocDict[word])
			newDocs = []

			for doc in termDocDict[word]:
				newDocs.append(int(doc.split(':')[0]))

			newDocs = set(newDocs)
			if len(candidates) == 0:
				candidates.update(newDocs)
			else:
				candidates = candidates.intersection(newDocs)

		return [list(candidates), wordOccurrence]

	def rankMeUpScotty(self, query):
		print("starting rankMeUpScotty")
		# Tokenize the query into a list
		lowered = query.lower()
		tokenized = word_tokenize(lowered)
		noStopwords = [token for token in tokenized if not token in stopWords and token in words]
		#noStopwords = [token for token in tokenized if token not in stopWords]
		queryArray = [ps.stem(word) for word in noStopwords]
		print(queryArray)
		candidates = self.findCandidates(queryArray)
		print(candidates[1])
		ranks = self.ranking(candidates, queryArray)

		top5 = self.getTopN(ranks, 5)
		#print(top5)
		return top5