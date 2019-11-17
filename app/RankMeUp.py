from math import log
import csv

import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
#mport pickle
import time
import string
import re
from itertools import combinations

#words = set([word.lower() for word in set(nltk.corpus.words.words())])
stopWords = set(stopwords.words('english'))
ps = PorterStemmer()

from collections import Counter

metaFile = "text_processing/metadataP2.tsv"
termDocFile = "text_processing/termDocFreqP2.tsv"
docTermFile = "text_processing/docTermFreqP2.tsv"

docTermDict = {}
metaFileDict = {}
index = 0
print("creating dict")
with open(metaFile, 'r', encoding="utf-8") as f1, open(docTermFile, 'r', encoding='utf8') as f2:
	metaReader = csv.reader(f1, delimiter='\t')
	docTermReader = csv.reader(f2, delimiter='\t')
	for row1,row2 in zip(metaReader, docTermReader):
		metaFileDict[index] = row1
		#docTermDict[index] = dict([(r.split(':')[0],int(r.split(':')[1])) for r in row2])
		#docTermDict[index] = row2
		docTermDict[index] = [row for row in row2 if len(row.split(':')[0]) < 12]
		index += 1
		if index % 10000 == 0:
			print(index)
f1.close()
f2.close()
docTermDict.update(dict(docTermDict))
#metaFileDict.update(dict(metaFileDict))
print("docTermDict Created", len(docTermDict))

print("creating dict")
termDocDict = {}
index = 0
with open(termDocFile, 'r', encoding='utf8') as f:
	fileReader = csv.reader(f, delimiter='\t')
	for row in fileReader:
		#print(row)
		if len(row) > 1 and len(row[0]) < 12 :#and row[0].isalpha():
			termDocDict[row[0][1:-1]] = [int(r.split(':')[0]) for r in row[1:]]
		index += 1
		if index % 10000 == 0:
			print(index)
f.close()
print("termDocDict Created", len(termDocDict))

dcSize = len(docTermDict)

class RankMeUp:

	def __init__(self):
		pass

	def getTopN(self, ranks, n):
		print("Geting top n")
		top5 = [i for i in Counter(ranks).most_common(n)]
		print(top5)
		return [i[0] for i in top5]

	def ranking(self, candidates, queryList):
		print("start ranking")
		#with open(metaFile, 'r', encoding="utf-8") as f1, open(docTermFile, 'r', encoding='utf8') as f2:
			#metaReader = csv.reader(f1, delimiter='\t')
			#docTermReader = csv.reader(f2, delimiter='\t')
		candidateRank = {}
		curLine = 0
		metaLine = None
		docTermLine = None
		tfidf_time = 0
		lines_time = 0

		print("amount of candidates: " + str(len(candidates[0])))
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
			start_time = time.time()
			metaLine = metaFileDict[candidate]
			docTermLine= docTermDict[candidate]
			lines_time += time.time() - start_time
			# Make sure we keep a running summation
			summation = 0

			# Calculations for future formula use
			maxD = int(metaLine[2])
			docLength = int(metaLine[1])

			# For every word in our query list, use the formula to calculate the ranking score for each candidate
			start_time = time.time()
			for word in queryList:
				#print("word "  + word)
				#print(candidates[1])
				#print(docTermLine)
				IDF = log(dcSize / candidates[1][word], 2)
				start_time = time.time()
				#wordCount = docTermLine[word]
				wordCount = [grp.split(':')[1] for grp in docTermLine if word == grp.split(':')[0][1:-1]]
				#print("word", word)
				#print("first item", docTermLine[0].split(':')[0][1:-1])
				#print("wordcount", wordCount)
				if len(wordCount) == 0:
					wordCount = 0
				else:
					wordCount = int(wordCount[0])
				tfidf_time += time.time()-start_time

				#print(wordCount)
				#TF = (wordCount / docLength) / maxD
				TF = wordCount / docLength
				3#print("tf", TF)
				#print("idf", IDF)
				summation += TF * IDF
			print("Candidate:", candidate,maxD,docLength, summation)
			candidateRank[candidate] = summation
		print("lines_Time", lines_time)
		print("tfidf_time", tfidf_time)
		
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
		print("querylist", queryList)
		print("termdocdict", termDocDict[queryList[0]])
		for word in queryList:
			#		if row[0] == word:
			#			print(row[0],row[1:5])
			#			numFoundQueryWords += 1
			wordOccurrence[word] = len(termDocDict[word])

			newDocs = termDocDict[word]
			print(word, ":", len(newDocs))
			newDocs = set(newDocs)
			if len(candidates) == 0:
				candidates.update(newDocs)
			else:
				candidates = candidates.intersection(newDocs)
		# Code to grab the combinations of the query
		print("len of candidates", len(candidates))
		gramSize = len(queryList) - 1
		while(len(candidates) <50 and gramSize != 0):
			newQueryList = combinations(queryList, gramSize)
			for wordsTuple in newQueryList:
				for word in wordsTuple:
					wordOccurrence[word] = len(termDocDict[word])

					newDocs = termDocDict[word]
					print(word, ":", len(newDocs))
					newDocs = set(newDocs)
					if len(candidates) == 0:
						candidates.update(newDocs)
					else:
						candidates = candidates.intersection(newDocs)
			gramSize-=1
			# End new code
		return [list(candidates), wordOccurrence]

	def rankMeUpScotty(self, query):
		print("starting rankMeUpScotty")
		# Tokenize the query into a list
		print("query", query)
		print("termdocdict for hellp", termDocDict['hello'])
		lowered = query.lower()
		tokenized = word_tokenize(lowered)
		tokenized = [ps.stem(word) for word in tokenized]
		noStopwords = [token for token in tokenized if not token in stopWords and token in termDocDict]
		#noStopwords = [token for token in tokenized if token not in stopWords]
		queryArray = [word for word in noStopwords]
		print("queryArray", queryArray)
		candidates = self.findCandidates(queryArray)
		print(candidates[1])
		ranks = self.ranking(candidates, queryArray)

		top5 = self.getTopN(ranks, 5)
		#print(top5)
		return top5