
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
		myString = myString.lower()
		tokenized = word_tokenize(myString)
		noStopwords = [token for token in tokenized if not token in stopWords and not token in string.punctuation and not token in myStopwords]
		stemmed = [ps.stem(word) for word in noStopwords]
		myString = stemmed
		return myString

	def getDocuments(self, documentList):
		documents = []
		print(documentList)
		documentList = sorted(documentList)

		for doc in documentList:
			newnum = doc//100000
			curLine = newnum * 100000
			with open('text_processing/splitWiki/wiki{0}.tsv'.format(newnum), 'r', encoding='utf8') as src:
				reader = csv.reader(src, delimiter="\t")
				docLine = next(reader)
				while curLine != doc:
					docLine = next(reader)
					curLine += 1

				print(curLine)
				title = docLine[2]
				content = docLine[1]
				documents.append([title, content])
				
		return documents

	def getSnippets(self, query, documentList):
		q = self.tokenize(query)

		documents = self.getDocuments(documentList)
		titles = [d[0] for d in documents]
		documents = [d[1] for d in documents]
		origSentences = [sent_tokenize(d) for d in documents]
		for x, doc in enumerate(origSentences):
			for y, sent in enumerate(doc):
				if '\n' in sent:
					sentSplit = sent.split('\n')
					if 'may refer to' in sent:
						origSentences[x][y] = sentSplit[0]
					else:
						origSentences[x][y] = sentSplit[len(sentSplit)-1]
		#origSentences = [y.split('\n')[0] for y in [x for x in origSentences]]
		#origSentences = [sents[len(sents)-1] for d in sentences]

		#for sent in origSentences:
		#	print(sent)

		tokdocuments = []
		for document in documents:
			sentences = []
			for sentence in sent_tokenize(document):
				sentences.append(self.tokenize(sentence))
			tokdocuments.append(sentences)

		cosSims = []
		for document in tokdocuments:
			cosSimSent = []
			for sentence in document:
				if len(sentence) < 1:
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
				if sim > first[1]:
					second = first
					first = [index, sim]
				elif sim > second[1]:
					second = [index, sim]
			
			sentence1 = ""
			sentence2 = ""
			
			if len(origSentences[i]) > 0:
				sentence1 = origSentences[i][first[0]]

			if len(origSentences[i]) > 1:
				sentence2 = " {0}".format(origSentences[i][second[0]])

			snippetText = "{0}{1}".format(sentence1, sentence2)
			snippetObj = {"title": titles[i].replace("_", " "), "snippet": snippetText}
			finalSnippets.append(snippetObj)

		return finalSnippets