
import nltk
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
words = set(nltk.corpus.words.words())
stopWords = set(stopwords.words('english'))
ps = PorterStemmer()
myStopwords = {"''", '``', '“', '”', '’', "'s"}
import pandas as pd
import string
import math
import csv

NUM_DOCS = 10
CHUNKSIZE = 1

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
		noStopwords = [token for token in tokenized if not token in stopWords and not token in string.punctuation and not token in myStopwords and token in words]
		stemmed = [ps.stem(word) for word in noStopwords]
		myString = stemmed
		return myString

	def getDocuments(self):
		documents = []

		with open('wikipedia_text_files.csv', 'r', encoding='utf8') as src:
			for i, chunk in enumerate(pd.read_csv(src, chunksize=CHUNKSIZE, nrows=NUM_DOCS)):
				for row in chunk.itertuples():
					title = row[2]
					content = row[1]
					documents.append([title, content])
		return documents

	def getSnippets(self, query):
		q = self.tokenize(query)

		documents = self.getDocuments()
		titles = [d[0] for d in documents]
		documents = [d[1] for d in documents]
		origSentences = [sent_tokenize(d) for d in documents]
		#print(origSentences)
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
					idf = math.log(len(document)/(self.numSentHaveWord(document, word)+1), 2)
					tfSent = sentence.count(word)/len(sentence)
					sentVector.append(tfSent*idf)
					tfQuery = query.count(word)/len(q)
					queryVector.append(tfQuery*idf)

				top = sum([sentVector[i]*queryVector[i] for i in range(len(q))])
				sqrSent = sum([tok**tok for tok in sentVector], 0)
				sqrQuery = sum([tok**tok for tok in queryVector], 0)
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
			
			snippetText = "{0} {1}".format(origSentences[i][first[0]].replace("\n", ""), origSentences[i][second[0]].replace("\n", ""))
			snippetObj = {"title": titles[i].replace("_", " "), "snippet": snippetText}
			finalSnippets.append(snippetObj)
			#print("Title: {0}\n{1} {2}\n\n".format(titles[i], origSentences[i][first[0]].replace("\n", ""), origSentences[i][second[0]].replace("\n", "")))
		return finalSnippets


"""
	[
		{
			title: ...,
			snippet: ...
		}
	]
	"""