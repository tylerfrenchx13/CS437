import time
import csv
import re
import pandas as pd
import string
from collections import Counter
import matplotlib.pyplot as plt
import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import TweetTokenizer
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
words = set(nltk.corpus.words.words())
stopWords = set(stopwords.words('english'))
ps = PorterStemmer()
tknzr = TweetTokenizer()
#table = str.maketrans({key: None for key in string.punctuation})
import sys
myStopwords = {"--", "...", "’", "–", "”", "“", "…", "•", "—", "‘"}
zipfsWords = {
	"game", "play", "s", "world", "new", "use", "time", "featur", "player", "one",
	"level", "differ", "take", "get", "make", "way", "uniqu", "find", "enemi", "challeng"
}
#csv.field_size_limit(sys.maxsize)
csv.field_size_limit(2**31-1)

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

def createMetadata():
	with open("tokenDocNEW.csv", "r", encoding="utf8") as src, open("metadataP2.tsv", "w", encoding="utf8") as dest:
		for index, row in enumerate(csv.reader(src)):
			if not row:
				dest.write("\n")
				continue
			wordCount = len(row)
			maxD = sorted(Counter(row).values(), reverse=True)[0]
			dest.write("{0}\t{1}\t{2}\n".format(index, wordCount, maxD))

def createDocTerm():
	with open("tokenDocNEW.csv", "r", encoding="utf8") as src, open("docTermFreqP2.tsv", "w", encoding="utf8") as dest:
		for index, row in enumerate(csv.reader(src)):
			countFrequency = Counter(row)
			for index, key in enumerate(countFrequency):
				if index > 0:
					dest.write("\t")
				dest.write("{0}:{1}".format(key, countFrequency[key]))
			dest.write("\n")

def isEnglish(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True

def tokenize(content):
	tokenized = content.lower()
	tokenized = tknzr.tokenize(tokenized)
	tokenized = [token for token in tokenized if isEnglish(token)]
	tokenized = [token for token in tokenized if not token in string.punctuation]
	"""tokenized = word_tokenize(lowered)"""
	""" and not token in myStopwords and token not in string.punctuation and isEnglish(token)"""
	tokenized = [token for token in tokenized if not token in stopWords]
	tokenized = [ps.stem(word) for word in tokenized]
	"""final = [re.sub('[^A-Za-z0-9]+', '', token) for token in stemmed]"""
	"""final = [token for token in stemmed if not token in zipfsWords]"""
	return tokenized

def createTermDoc():
	with open("tokenDocNEW.csv", "r", encoding="utf8") as src:
		reader = csv.reader(src)

		termDoc = {}
		for index, row in enumerate(reader):
			print(index)
			count = Counter(row)
			for token in count:
				if token not in termDoc:
					termDoc[token] = {}
				termDoc[token][index] = count[token]

		with open("termDocFreqP2.tsv", "w", encoding="utf8") as dest:
			for token in termDoc:
				dest.write("{0}\t".format(token))
				for index, doc in enumerate(termDoc[token]):
					if index > 0:
						dest.write("\t")
					dest.write("{0}:{1}".format(doc, termDoc[token][doc]))
				dest.write("\n")

def tokenizeText():
	with open("steam-clean.csv", 'r', encoding='utf8') as src:
		reader = csv.reader(src)
		next(reader)

		with open("tokenDocNEW.csv", "w", encoding="utf8") as dest:
			for row in reader:
				appid = row[0]
				print(appid)
				description = row[2]
				tokenized = tokenize(description)
				found = False
				for token in tokenized:
					if token != '':
						if found:
							dest.write(",")
						dest.write("'{0}'".format(token))
						found = True
				dest.write("\n")

def cleanText():
	with open("../steam-store-games/steam.csv", 'r', encoding='utf8') as src1, open("../steam-store-games/steam_description_data.csv", 'r', encoding='utf8') as src2:
		df1 = pd.read_csv(src1)
		df2 = pd.read_csv(src2)

		documents = {}
		for row in df1.iterrows():
			appid = row[1][0]
			name = row[1][1]
			english = row[1][3]

			if english == 1:
				documents[appid] = name

		print("A")

		with open("steam-clean.csv", "w", encoding="utf8") as dest:
			dest.write("id,title,description\n")
			for index, row in enumerate(df2.iterrows()):
				appid = row[1][0]
				if appid in documents:
					description = row[1][1]
					htmlreg = re.compile('<.*?>')
					description = re.sub(htmlreg, ' ', description)
					urlreg = re.compile('((http|https|www\.)\S*(\.com)*)|((http|https|www\.)*\S*(\.com))', re.IGNORECASE)
					description = re.sub(urlreg, ' ', description)
					description = description.replace("\n", " ")
					description = description.replace("\t", " ")
					title = documents[appid]

					dest.write('{0},"{1}","{2}"\n'.format(index, title, description))

def createZipfs():
	with open("tokenDocNEW.csv", "r", encoding="utf8") as src:
		reader = csv.reader(src)

		tokenCounts = {}
		for index, row in enumerate(reader):
			print(index)
			count = Counter(row)
			for token in count:
				if token not in tokenCounts:
					tokenCounts[token] = 0
				tokenCounts[token] += 1

		tokenCounts = sorted(tokenCounts.items(), key = lambda kv:(kv[1], kv[0]), reverse=True)

		with open("zipfs.tsv", "w", encoding="utf8") as dest:
			for token in tokenCounts:
				dest.write("{0}\t{1}\n".format(token[0], token[1]))

def plotZipfs():
	frequencies = []
	with open('zipfs.tsv', 'r', encoding="utf8") as src:
		reader = csv.reader(src, delimiter='\t')
		for row in reader:
			frequencies.append(int(row[1]))
	plt.loglog(range(1, len(frequencies)+1), frequencies, 'bo', markersize=2.0)
	plt.ylabel("Frequency")
	plt.xlabel("Rank")
	plt.show()

def createHeaps():
	with open("tokenDocNEW.csv", "r", encoding="utf8") as src, open("heaps.tsv", "w", encoding="utf8") as dest:
		reader = csv.reader(src)

		tokens = {}
		vocabSize = 0
		for index, row in enumerate(reader):
			print(index)
			count = Counter(row)
			for token in count:
				if token not in tokens:
					tokens[token] = 0
					vocabSize += 1

			dest.write("{0}\n".format(vocabSize))

def plotHeaps():
	vocab = []
	with open('heaps.tsv', 'r', encoding="utf8") as f:
		reader = csv.reader(f, delimiter='\t')
		for row in reader:
			vocab.append(int(row[0]))

	plt.plot(range(1, len(vocab)+1), vocab, 'bo', markersize=2.0)

	plt.ylabel("Total Vocabulary")
	plt.xlabel("Document")
	plt.show()

def main():
	
	#cleanText()
	tokenizeText()
	
	createTermDoc()
	createDocTerm()
	createMetadata()
	
	createZipfs()
	#plotZipfs()

	createHeaps()
	#plotHeaps()

main()
