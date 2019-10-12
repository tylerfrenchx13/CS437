from math import log
import csv

def findCandidates(file, query):
    fileReader = open(file, 'r', encoding="utf-8")
    fileReader = csv.reader(fileReader, delimiter='\t')
    queryArray = query.split()
    candidates = []
    wordOccurrence = {}
    foundOne = False
    for row in fileReader:
        for word in queryArray:
            if row[0] == word:
                wordOccurrence[word] = len(row)-1;
                newDocs = [];
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
    return [candidates,wordOccurrence]

def rankMeUpScotty(metadataFile,termDocFile, docTermFreq, query, collectionSize):
    candidates = findCandidates(termDocFile,query)
    rank = ranking(candidates, metadataFile, termDocFile, docTermFreq ,query,collectionSize)

def ranking(candidates, metadata, termDocFile, docTermFreq, query,collectionSize):
    candidateRank = {}
    queryList = query.split()
    for candidate in candidates[0]:
        summation = [];
        totalVal = 0
        for word in queryList:
            val = 0
            IDF = 0
            TF = 0;
            #This represents the IDF of the document.
            fractionalVal = collectionSize/candidates[1][word];
            IDF = log(fractionalVal,2);
            #This represents the TF of the document.
            summation.append(val)
        for val in summation:
            totalVal+=val;
        candidateRank[candidate] = totalVal;
    return candidateRank

rankMeUpScotty("app/metadata.tsv", "app/term_doc_freq.tsv", "temp", "aborigin 1992",100000)