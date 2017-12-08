import os
import math
import operator
import shutil

import re

from bs4 import BeautifulSoup

CORPUS_DIR = "../Project Input/cacm/"
UPDATED_CORPUS = "Corpus/"
QUERY_FILE = "queriesRedefined.txt"
BM25_SCORE_DIR = "BM25 Scores"
CACM_REL = "cacm.rel.txt"
STOP_WORD_FILE = "common_words.txt"


def regenerate_corpus():
    for file in os.listdir(CORPUS_DIR):
        output = open(CORPUS_DIR +file)
        fName = file.split(".html")[0]
        soup = BeautifulSoup(output, "html.parser")
        all_text = ''.join(soup.findAll(text=True))
        all_text = all_text.lower()
        all_text = all_text.rstrip()
        all_text = all_text.lstrip()
        outputf = open("Corpus/" + fName + ".txt", "w")
        outputf.write(all_text)
        outputf.close()


def termQueryMatch(query, word):
    query = query.split()
    for i in query:
        if i==word:
            return True
    return False

def returnSignificanceScore(sentence, query):
    sentence = sentence.split()
    #print sentence
    min = 0
    max = 0
    count = 0
    #print stopWordList
    result = 0.0
    for word in sentence:
        if termQueryMatch(query, word) and word not in stopWordList:
            min = sentence.index(word)
            #print "first i"
            break
    for i in range(len(sentence)-1, 0, -1):
        if termQueryMatch(query, sentence[i]) and i not in stopWordList:
            max = i
            break
    for i in sentence[min: (max+1)]:
        if termQueryMatch(query, i) and i not in stopWordList:
            count+=1
    if(len(sentence[min:(max+1)])==0):
        result = 0
    else:
        result =  math.pow(count,2)/len(sentence[min:(max+1)])
    #print result
    return result


def returnSummary(queryId, queryDocumentResult, queryDict):
    query = queryDict[int(queryId)]
    resultFileForQuery = queryDocumentResult[queryId]
    for file in resultFileForQuery:
        file = open(UPDATED_CORPUS+file, "r")
        sentences = file.read().split("\n")
        count = 1
        snippets = {}
        summary = []
        for sentence in sentences:
            snippets[sentence] = returnSignificanceScore(sentence, query)
            #print returnSignificanceScore(sentence, query)
        for i in sorted(snippets, key=snippets.get, reverse=True):
            if count < 6:
                summary.append(str(i))
                count += 1
        print summary



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

#print queryDocumentResult
#regenerate_corpus()
returnSummary("1",queryDocumentResult, queryDict)
#something like {'1': ['CACM-1605.txt', 'CACM-1410.txt', 'CACM-1506.txt',







