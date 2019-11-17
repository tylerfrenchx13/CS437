
import nltk
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
stopWords = set(stopwords.words('english'))
ps = PorterStemmer()
myStopwords = {"''", '``', '“', '”', '’', "'s"}
import pandas as pd
import string
import math
import csv
import sys
from nltk.tokenize import TweetTokenizer
tknzr = TweetTokenizer()
#csv.field_size_limit(sys.maxsize)
csv.field_size_limit(2**31-1)

class SnippetGenerator:

	def __init__(self):
		pass

	def numSentHaveWord(self, sentences, word):
		count = 0
		for sentence in sentences:
			if word in sentence:
				count += 1

		return count

	def tokenize(self, myString):
		tokenized = myString.lower()
		tokenized = tknzr.tokenize(tokenized)
		#tokenized = [token for token in tokenized if isEnglish(token)]
		tokenized = [token for token in tokenized if not token in string.punctuation]
		tokenized = [token for token in tokenized if not token in stopWords]
		tokenized = [ps.stem(word) for word in tokenized]
		return tokenized

	def getDocuments(self, documentList):
		#print("A")
		documents = []
		
		for doc in documentList:
			with open('text_processing/steam-clean.csv', 'r', encoding='utf8') as src:
				reader = csv.reader(src)
				next(reader)
				for line in reader:
					#print(line[0])
					#print(doc)
					if int(line[0]) == doc:
						print("FOUND: {0}".format(doc))
						title = line[1]
						content = line[2]
						documents.append([title, content])
						break

		#print(documents)
		#print("B")
		return documents

	def getSnippets(self, query, documentList):
		q = self.tokenize(query)

		documents = self.getDocuments(documentList)
		titles = [d[0] for d in documents]
		documents = [d[1] for d in documents]
		origSentences = [sent_tokenize(d) for d in documents]
		#origSentences = [s[1:] if len(s) > 1 else s for s in origSentences]
		#print(origSentences)
		#for x, doc in enumerate(origSentences):
			#for y, sent in enumerate(doc):
				#if '\n' in sent:
					#sentSplit = sent.split('\n')
					#print(sent)
					#if 'may refer to' in sent:
						#print(sent)
						#print(sentSplit)
					#	origSentences[x][y] = sentSplit[0]
					#else:
					#	origSentences[x][y] = sentSplit[len(sentSplit)-1]
		#origSentences = [y.split('\n')[0] for y in [x for x in origSentences]]
		#origSentences = [sents[len(sents)-1] for d in sentences]

		#for sent in origSentences:
		#	print(sent)

		#print(origSentences)

		workSentences = origSentences
		tokdocuments = []
		for document in workSentences:
			sentences = []
			for sentence in document:
				#print(sentence)
				sentences.append(self.tokenize(sentence))
			#print(sentences)
			if len(sentences) > 1:
				sentences = sentences[1:]
			#print(sentences)
			tokdocuments.append(sentences)
		

		#print(tokdocuments)

		cosSims = []
		for document in tokdocuments:
			#print(document)
			cosSimSent = []
			for sentence in document:
				if len(sentence) < 2:
					cosSimSent.append(0)
					continue

				sentVector = []
				queryVector = []
				
				for word in q:
					#print(len(document))
					#print(self.numSentHaveWord(document, word)+1)
					idf = math.log(len(document)+1/(self.numSentHaveWord(document, word)+1), 2)
					tfSent = sentence.count(word)/len(sentence)
					#print(tfSent)
					#print(idf)
					sentVector.append(tfSent*idf)
					tfQuery = query.count(word)/len(q)
					queryVector.append(tfQuery*idf)

				#print(sentVector)
				#print(queryVector)
				top = sum([sentVector[i]*queryVector[i] for i in range(len(q))])
				sqrSent = sum([tok**tok for tok in sentVector], 0)
				sqrQuery = sum([tok**tok for tok in queryVector], 0)
				#print(sqrSent)
				#print(sqrQuery)
				bot = math.sqrt(sqrSent*sqrQuery)
				cosSimSent.append(top/bot)
			cosSims.append(cosSimSent)

		finalSnippets = []
		for i, doc in enumerate(cosSims):
			first = [0, 0]
			second = [1, 0]

			for index, sim in enumerate(doc):
				#print(index, sim)
				if sim > first[1]:
					second = first
					first = [index, sim]
				elif sim > second[1]:
					second = [index, sim]
			
			sentence1 = ""
			sentence2 = ""
			
			if len(origSentences[i]) > 0:
				sentence1 = origSentences[i][first[0]]
			#print(origSentences[i])
			#print(i)
			#print(origSentences)
			#print(first)
			#print(second)
			#print(len(origSentences[i]))
			if len(origSentences[i]) > 1 and first[0] != second[0]:
				sentence2 = " {0}".format(origSentences[i][second[0]])

			#print(sentence1)
			#print(sentence2)
			snippetText = "{0}{1}".format(sentence1, sentence2)
			snippetObj = {"title": titles[i], "snippet": snippetText}
			finalSnippets.append(snippetObj)

		return finalSnippets

#sg = SnippetGenerator()
#print(sg.getSnippets('team', [0, 1, 2, 3, 4]))