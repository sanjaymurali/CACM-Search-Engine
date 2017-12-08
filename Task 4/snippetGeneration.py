import os
import math
import operator
import shutil

import re

CORPUS_DIR = "../Corpus"
QUERY_FILE = "queriesRedefined.txt"
BM25_SCORE_DIR = "BM25 Scores"
CACM_REL = "cacm.rel.txt"
STOP_WORD_FILE = "common_words.txt"

def returnSummary(queryId, queryDocumentResult, queryDict):
    query = queryDict[queryId]
    resultFileForQuery = queryDocumentResult[queryId]
    for file in resultFileForQuery:
        file = open(file, "r")



stopWordList = []
queryDict = {}

queryFile = open(QUERY_FILE,"r")
stopListFile = open(STOP_WORD_FILE, "r")




#stoplist words
for line in stopListFile.readlines():
    stopWordList.append(line.strip())
stopListFile.close()

#query dict
count = 1
for query in queryFile.readlines():
    queryDict[count] = query
    count+=1


queryDocumentResult = {}
#extract result files for a particular
firstQueryResult =  open(BM25_SCORE_DIR+"/Q1.txt","r")
for resultLine in firstQueryResult.readlines():
    resultLine = re.split(r'\t+', resultLine)
    #print re.split(r'\t+', resultLine)
    queryId = resultLine[0]
    documentId = resultLine[2]
    if queryId in queryDocumentResult:
        queryDocumentResult[queryId].append(documentId)
    else:
        queryDocumentResult[queryId] = [documentId]

print queryDocumentResult
returnSummary("1",queryDocumentResult, queryDict)
#something like {'1': ['CACM-1605.txt', 'CACM-1410.txt', 'CACM-1506.txt',







