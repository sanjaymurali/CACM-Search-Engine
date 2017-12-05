import os

import shutil
import urllib2

import re
from bs4 import BeautifulSoup
from os import listdir
from os.path import isfile, join
import os

DOWNLOADED_HTML_DIR = "../Project Input/cacm/"
GENERATED_CORPUS_DIR = "Corpus"
FILENAME_LIST = []
CASE_FOLDING = 1 # initially we do case_folding
PUNCTUATION_HANDLING = 1 # initially we handle punctuations

myPath =  "../Project Input/cacm/"
for file in listdir(myPath):
    output = open(myPath+file)
    soup = BeautifulSoup(output, "html.parser")
    all_text = ''.join(soup.findAll(text=True))
    all_text = all_text.lower()
    line = all_text
    fName =  file.split(".html")[0]
    outputf = open("Corpus/"+fName+".txt","w")
    outputf.write(line.strip("\n"))
    outputf.close()



        #soup = BeautifulSoup(fp)
        #print soup
    #all_text = ''.join(soup.findAll(text=True))
    #print all_text