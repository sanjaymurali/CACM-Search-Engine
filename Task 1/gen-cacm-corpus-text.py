import re
from bs4 import BeautifulSoup
from os import listdir

#using Sanjay's code

# handling punctuations before a word, such as -1.0 shouldnt be removed while: ".hello" should be removed
def handle_prefixed_punctuations(word):
    # dont remove punctuations in a negative and positive, decimal or float number
    if (re.match(r'^[\-]?[0-9]*\.?[0-9]+$', word)):
        return word
    elif (word[:1] == "-") or (word[:1] == ",") or (word[:1] == "."):
        return word[1:]
    else:
        return word

myPath =  "../Project Input/cacm/"
for file in listdir(myPath):
    output = open(myPath+file)
    soup = BeautifulSoup(output, "html.parser")
    all_text = ''.join(soup.findAll(text=True))
    all_text = all_text.lower()
    line = all_text
    fName =  file.split(".html")[0]
    temp_array = []
    # we need to remove trailing and pre-fixed "," , "." and "-" from the words
    for each_word in line.split():
        length = len(each_word)
        # removing trailing punctuations
        if (each_word[(length - 1): length] == "-") or (each_word[(length - 1): length] == ",") or (
            each_word[(length - 1): length] == "."):
            each_word = each_word[:(length - 1)]  # removing the punctuation
        # removing pre-fixed punctuations
        each_word = handle_prefixed_punctuations(each_word)
        temp_array.append(each_word)
    content_as_array = temp_array
    line = ' '.join(content_as_array)
    outputf = open("Corpus/"+fName+".txt","w")
    outputf.write(line)
    outputf.close()



        #soup = BeautifulSoup(fp)
        #print soup
    #all_text = ''.join(soup.findAll(text=True))
    #print all_text