import os
import math
import operator
import shutil

import re

from bs4 import BeautifulSoup

CORPUS_DIR = "../Project Input/cacm/"
UPDATED_CORPUS = "Corpus/"
QUERY_FILE = "queriesRedefined.txt"
SCORE_DIR = "BM25 Scores"
CACM_REL = "cacm.rel.txt"
STOP_WORD_FILE = "common_words.txt"
stopWordList = []
queryDict = dict()


def generate_snippet():
    for i in range(1, 65):
        query_id = str(i)
        processed_score_file =  process_score_file(query_id)
        returnSummary(query_id, processed_score_file)


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
    pattern_to_remove = re.compile(r'[,.!\"();:<>-_+=@#]')
    pattern_word = pattern_to_remove.sub('', word)
    query = query.split()

    for i in query:
        if i == pattern_word:
            return True

    return False

def process_score_file(query_id):
    queryDocumentResult = dict()
    # extract result files for a particular
    QueryResult = open(SCORE_DIR + "/Q"+str(query_id)+".txt", "r")
    count = 0
    for resultLine in QueryResult.readlines():
        if count == 10:
            break
        else:
            resultLine = re.split(r'\t+', resultLine)
            # print re.split(r'\t+', resultLine)
            queryId = resultLine[0]
            documentId = resultLine[2]
            if queryId in queryDocumentResult:
                queryDocumentResult[queryId].append(documentId)
            else:
                queryDocumentResult[queryId] = [documentId]
        count += 1
    return queryDocumentResult

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
            break
    for i in range(len(sentence)-1, 0, -1):
        if termQueryMatch(query, sentence[i]) and sentence[i] not in stopWordList:
            max = i
            break
    for i in sentence[min: (max+1)]:
        if termQueryMatch(query, i) and i not in stopWordList:
            count+=1
    if(len(sentence[min:(max+1)])==0):
        result = 0
    else:
        result =  math.pow(count,2)/len(sentence[min:(max+1)])

    return result


def returnSummary(queryId, queryDocumentResult):
    query = queryDict[int(queryId)]
    resultFileForQuery = queryDocumentResult[queryId]
    output_file = open("Snippets/" +"Q"+queryId+".txt","w")
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
        output_file.write(file.name.split("/")[1].replace(".txt",""))
        output_file.write("\n")
        for snip in summary:
            words = snip.split()
            if len(words) != 0:
                for word in words:
                    if termQueryMatch(query, word):
                        words[words.index(word)] = word.upper()
                        output_file.write(word.upper())
                        output_file.write(" ")
                    else:
                        output_file.write(word+" ")
                output_file.write("\n")
        output_file.write("---------------------------------------------------------------")
        output_file.write("\n")
    output_file.close()


def process_stopwords():
    global stopWordList
    stopListFile = open(STOP_WORD_FILE, "r")
    # stoplist words
    for line in stopListFile.readlines():
        stopWordList.append(line.strip())
    stopListFile.close()


def query_list_processing():
    global queryDict
    queryFile = open(QUERY_FILE, "r")
    # query dict
    count = 1
    for query in queryFile.readlines():
        queryDict[count] = query
        count += 1

def start():
    process_stopwords()
    query_list_processing()
    generate_snippet()


start()