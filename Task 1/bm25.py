import pickle
from os import listdir

import math

import re

from Index import Index


def clean_text(text):
    text = text.lower()
    text = re.sub('\[(.*?)\]', '', text)
    text = re.sub('[\"\(\)]', '', text)
    text = re.sub('(\'[a-zA-Z]+)', '', text)
    text = re.sub('[^\x00-\x7F]+', '', text)
    text = re.sub('[^a-zA-Z0-9]+$', '', text)
    if (not any(char.isdigit() for char in text)):
        text = re.sub('[^a-zA-Z0-9-]', '', text)
    text = re.sub('.*www.*|.*http.*', '', text)
    text = re.sub('^[~{}&\'*+-/].*', '', text)
    return text

def calculateBmi(unigramInvertedIndex, documentLengthMap, averageDocumentLength):
    B = 0.75
    K1 = 1.2
    K2 = 100.00
    linecount = 1
    with open("queriesRedefined.txt") as f:
        for line in f:
            query = line.split(" ")
            bmIndex = {}
            q = []
            for term in query[1:]:
                term = clean_text(term)
                print term
                q.append(term)
            print q
            for queryWord in q:
                #queryWord = queryWord.strip()
                index_list = unigramInvertedIndex[queryWord]
                # print len(index_list)
                # print queryWord
                for index in index_list:
                    dl = documentLengthMap[index.docId]
                    fi = index.frequency
                    bm = math.log(1 / ((len(index_list) + 0.5) / (1000 - len(index_list) + 0.5))) * (((K1 + 1) * fi) / (K1 * ((1 - B) + (B * (dl / averageDocumentLength))) + fi)) * ((K2 + 1) / (K2 + 1))
                    if (bmIndex.has_key(index.docId)):
                        returnedList = bmIndex[index.docId]
                        returnedList.append(bm)
                        bmIndex[index.docId] = returnedList
                    else:
                        returnedList = []
                        returnedList.append(bm)
                        bmIndex[index.docId] = returnedList
            finalMap = {}
            for key in bmIndex:
                val = bmIndex[key]
                bm25Val = 0.00
                for item in val:
                    bm25Val += item
                finalMap[key] = bm25Val
            fullyFinal = sorted(finalMap.items(), key=lambda kv: kv[1], reverse=True)
            fileName = "BM_" + line.rstrip() + ".txt"
            file = open("bm25results/"+fileName, "w")
            count = 1
            for key in fullyFinal[:100]:
                file.write(str(linecount) + " Q0 " + key[0].replace(".txt", "") + " " + str(key[1]) + " " + str(
                    count) + " " + "BM25")
                count += 1
                file.write("\n")
            file.close()
            linecount = linecount + 1


def localMapPutter(currentWord, localUnigram, file):
    if localUnigram.has_key(currentWord):
        index = localUnigram[currentWord]
        index.frequency = index.frequency + 1
        localUnigram[currentWord] = index
    else:
        id = file
        id = id.replace("_", "")
        newindex = Index(id, 1)
        localUnigram[currentWord] = newindex


def generateInvertedIndex(localUnigram, unigramInvertedIndex):
    for key, value in localUnigram.items():
        if unigramInvertedIndex.has_key(key):
            newIndex = unigramInvertedIndex[key]
            newIndex.append(value)
            unigramInvertedIndex[key] = newIndex
        else:
            newIndex = []
            newIndex.append(value)
            unigramInvertedIndex[key] = newIndex



def generatedictionary():
    dir = "./Corpus/"
    sumTokens = 0.00
    documentLengthMap = {}
    unigramInvertedIndex = {}
    for file in listdir(dir):
        fname = dir + file
        with open(fname) as f:
            ffiles = f.readline()
            localUnigram = {}
            wordsArray = ffiles.split(" ")
            documentLengthMap[file.replace("_", "")] = len(wordsArray)
            sumTokens += len(wordsArray)
            for currentWord in wordsArray:
                currentWord = currentWord.strip()
                localMapPutter(currentWord, localUnigram, file)
        generateInvertedIndex(localUnigram, unigramInvertedIndex)
    averageDocumentLength = sumTokens / 1000.0
    # save_obj(documentLengthMap,"documentLengthMap")
    # save_obj(unigramInvertedIndex, "unigramInvertedIndex")
    calculateBmi(unigramInvertedIndex, documentLengthMap, averageDocumentLength)


generatedictionary()
