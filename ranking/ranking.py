from math import log
import csv

def findCandidates(file, query):
    fileReader = open(file, 'r', encoding="utf-8")
    fileReader = csv.reader(fileReader, delimiter='\t')
    queryArray = query.split()
    candidates = []
    foundOne = False
    for row in fileReader:
        for word in queryArray:
            if row[0] == word:
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
    return candidates
findCandidates("app/term_doc_freq.tsv", "aborigin 1992")
