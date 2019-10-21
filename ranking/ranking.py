from math import log
import csv

def findCandidates(file, query):
    fileReader = open(file, 'r', encoding="utf-8")
    fileReader = csv.reader(fileReader, delimiter='\t')
    queryArray = query.split()
    candidates = []
    wordOccurrence = {}
    foundOne = False
    numFoundQueryWords = 0
    wordSize = len(query)
    for row in fileReader:
        for word in queryArray:
            if row[0] == word:
                numFoundQueryWords+=1
                wordOccurrence[word] = len(row)-1
                newDocs = []
                for i in range(len(row)-1):
                    if foundOne == False:
                        doc = row[i+1].split(':')
                        candidates.append(doc[0])
                    else:
                        doc = row[i+1].split(':')
                        newDocs.append(doc[0])
                if foundOne == True:
                    candidates = [value for value in candidates if value in newDocs]
                foundOne=True
    if(numFoundQueryWords != len(queryArray)):
        candidates = []

        
    return [candidates,wordOccurrence]

def rankMeUpScotty(metadataFile,termDocFile, docTermFreq, query, collectionSize):
    candidates = findCandidates(termDocFile,query)
    rank = ranking(candidates, metadataFile, termDocFile, docTermFreq ,query,collectionSize)
    return rank

def ranking(candidates, metadata, termDocFile, docTermFreq, query,collectionSize):
    candidateRank = {}
    queryList = query.split()
    for candidate in candidates[0]:
        summation = []
        totalVal = 0
        for word in queryList:
            val = 0
            IDF = 0
            TF = 0
            #This represents the IDF of the document.
            fractionalVal = collectionSize/candidates[1][word]
            IDF = log(fractionalVal,2)
            #This represents the TF of the document.
            #May be able to speed up by putting this in the intial method and making sure we access files sequentially
            fileReader = open(docTermFreq, 'r', encoding="utf-8")
            fileReader = csv.reader(fileReader, delimiter='\t')
            for i in range(int(float(candidate))-1):
                next(fileReader)
            interestedRow = next(fileReader)
            docLength = 0
            wordCount = 0
            largestOccurrence = 0
            for rowWord in interestedRow:
                result = rowWord.split(':')
                docLength += int(float(result[1]))
                if word == result[0]:
                    wordCount = int(float(result[1]))
                if largestOccurrence < int(float(result[1])):
                    largestOccurrence = int(float(result[1]))
            TF = wordCount/docLength
            TF = TF/largestOccurrence
            summation.append(TF*IDF)
        for val in summation:
            totalVal+=val
        candidateRank[candidate] = totalVal
    return candidateRank

rankMeUpScotty("text_processing/metadata.tsv", "text_processing/term_doc_freq.tsv", "text_processing/doc_term_freq.tsv", "hard indoor",50000)