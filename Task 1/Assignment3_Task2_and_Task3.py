from os import listdir
from os.path import isfile, join
from urllib.request import urlopen
from urllib.parse import *
from urllib.error import *
import time
import string
from bs4 import BeautifulSoup
import re
import os
import io
import nltk


class InvertedIndexes(object):
    def __init__(self):

        # Extracts all the file names in the directory when the object is made for this class.

        self.dirpath = "./Crawled_Files_Task1/Raw_Html_Task1"
        self.allFileNames = [f for f in listdir(self.dirpath) if isfile(join(self.dirpath, f))]

    def trigramInvertedIndex(self):

        # Generates Trigram Inverted Index.

        print("Generating Tri - Gram Inverted Index....")
        index_inverted = {}

        for file1 in self.allFileNames:
            file1Path = self.dirpath + "/" + file1
            with open(file1Path, 'r', encoding='utf8') as f:
                fileText = f.read()
                fileIndex = file1.split(".")[0]
                wordList = fileText.split()
                for k in range(len(wordList) - 2):
                    triGramWord = wordList[k] + " " + wordList[k + 1] + " " + wordList[k + 2]
                    if triGramWord in index_inverted:
                        temp_dict = index_inverted[triGramWord]
                        if fileIndex in temp_dict:
                            temp_dict[fileIndex] += 1
                        else:
                            temp_dict[fileIndex] = 1
                    elif triGramWord not in index_inverted:
                        index_inverted[triGramWord] = {fileIndex: 1}
            f.close()
        # print(index_inverted)
        return index_inverted

    def bigramInvertedIndex(self):

        # Generates Bigram Inverted Index.

        print("Generating Bi - Gram Inverted Index....")
        index_inverted = {}

        for file1 in self.allFileNames:
            file1Path = self.dirpath + "/" + file1
            with open(file1Path, 'r', encoding='utf8') as f:
                fileText = f.read()
                fileIndex = file1.split(".")[0]
                wordList = fileText.split()
                for k in range(len(wordList) - 1):
                    biGramWord = wordList[k] + " " + wordList[k + 1]
                    if biGramWord in index_inverted:
                        temp_dict = index_inverted[biGramWord]
                        if fileIndex in temp_dict:
                            temp_dict[fileIndex] += 1
                        else:
                            temp_dict[fileIndex] = 1
                    elif biGramWord not in index_inverted:
                        index_inverted[biGramWord] = {fileIndex: 1}
            f.close()
        # print(index_inverted)
        return index_inverted

    def inverted_Index_Into_File(self, index_inverted, n):

        # Writes the generated inverted index into a file.

        print("Writing " + str(n) + " - Gram Inverted Index into File....")
        fileName = "Inverted_Index" + str(n) + "_gram.txt"
        with open(fileName, 'w', encoding='utf8') as f:
            for k in index_inverted.keys():
                resultString = '{:30s} {:10s}'.format(str(k) + ' : ', str(index_inverted[k]))
                f.write(resultString)
                f.write("\n")
        f.close()

    def termFrequencyGenerator(self, invertedIndex):

        # Generates Term Frequency table from Inverted Index.

        print("Generating Term Frequency....")
        term_freq_dict = {}

        for i in invertedIndex.keys():
            freq_counter = 0
            temp_dict = invertedIndex[i]
            for j in temp_dict.keys():
                freq_counter = freq_counter + temp_dict[j]
            term_freq_dict[i] = freq_counter

        term_freq_sorted = sorted(term_freq_dict.items(), key=lambda x: x[1], reverse=True)

        return term_freq_sorted

    def term_Frequency_Into_File(self, term_freq_sorted, n):

        # Writes generated term frequency into table.

        print("Writing " + str(n) + " - Gram Term Frequency into File....")
        fileName = "Table_Term_Frequency_" + str(n) + "_gram.txt"
        with open(fileName, 'w', encoding='utf8') as f:
            for k, v in term_freq_sorted:
                resultString = '{:50s} {:10s}'.format(str(k) + ' : ', str(v))
                f.write(resultString)
                f.write("\n")
        f.close()

    def document_Frequency_Generator(self, invertedIndex):

        # Generates Document Frequency table from Inverted Index.

        print("Generating Document Frequency....")
        document_freq_dict = {}
        for i in invertedIndex.keys():
            list_of_documents = []
            temp_dict = invertedIndex[i]
            for j in temp_dict.keys():
                list_of_documents.append(j)
            document_freq_dict[i] = list_of_documents
        document_freq_sorted = sorted(document_freq_dict.items(), key=lambda x: x[0], reverse=False)
        return document_freq_sorted

    def document_Frequency_Into_File(self, document_freq_sorted, n):

        # Writes generated Document Frequency table into file.

        print("Writing " + str(n) + " - Gram Document Frequency into File....")
        fileName = "Table_Document_Frequency_" + str(n) + "_gram.txt"
        with open(fileName, 'w', encoding='utf8') as f:
            for k, v in document_freq_sorted:
                resultString = '{:70s} {:70s} {:10s}'.format(str(k) + ' : ', str(v), str(len(v)))
                f.write(resultString)
                f.write("\n")
        f.close()

    def unigramInvertedIndex(self):

        # Generated Unigram Inverted Index.

        print("Generating Uni - Gram Inverted Index....")
        wordCountDoc = {}
        index_inverted = {}
        for file1 in self.allFileNames:
            file1Path = self.dirpath + "/" + file1
            with open(file1Path, 'r', encoding='utf8') as f:
                fileText = f.read()
                fileIndex = file1.split(".")[0]
                wordList = fileText.split()
                wordCountDoc[fileIndex] = len(wordList)
                for w in wordList:
                    if w in index_inverted:
                        temp_dict = index_inverted[w]
                        if fileIndex in temp_dict:
                            temp_dict[fileIndex] += 1
                        else:
                            temp_dict[fileIndex] = 1
                    elif w not in index_inverted:
                        index_inverted[w] = {fileIndex: 1}
            f.close()
        return index_inverted


# Functions called to generate results.

print("Processing Uni - Grams ...")
invertedIndexObject1 = InvertedIndexes()
UniGramInvertedIndex = invertedIndexObject1.unigramInvertedIndex()
invertedIndexObject1.inverted_Index_Into_File(UniGramInvertedIndex, 1)
invertedIndexObject1.term_Frequency_Into_File(
    invertedIndexObject1.termFrequencyGenerator(UniGramInvertedIndex), 1)
invertedIndexObject1.document_Frequency_Into_File(
    invertedIndexObject1.document_Frequency_Generator(UniGramInvertedIndex), 1)

print("Processing Bi - Grams ...")
invertedIndexObject2 = InvertedIndexes()
BigramInvertedIndex = invertedIndexObject2.bigramInvertedIndex()
invertedIndexObject2.inverted_Index_Into_File(BigramInvertedIndex, 2)
invertedIndexObject2.term_Frequency_Into_File(
    invertedIndexObject2.termFrequencyGenerator(BigramInvertedIndex), 2)
invertedIndexObject2.document_Frequency_Into_File(
    invertedIndexObject2.document_Frequency_Generator(BigramInvertedIndex), 2)

print("Processing Tri - Grams ...")
invertedIndexObject3 = InvertedIndexes()
TriGramInvertedIndex = invertedIndexObject3.trigramInvertedIndex()
invertedIndexObject3.inverted_Index_Into_File(TriGramInvertedIndex, 3)
invertedIndexObject3.term_Frequency_Into_File(
    invertedIndexObject3.termFrequencyGenerator(TriGramInvertedIndex), 3)
invertedIndexObject3.document_Frequency_Into_File(
    invertedIndexObject3.document_Frequency_Generator(TriGramInvertedIndex), 3)
