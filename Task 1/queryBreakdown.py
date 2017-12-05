import re
import operator



query_IDS = []
query_text = []
queries = {}
text = ''

def splitMe(temp):
    someText=''
    for i in range(len(temp)):
        someText = someText+temp[i]
        print someText.strip(" ")

with open('cacm.query.txt') as rawfile:
    for line in rawfile:
        if '</DOC>' in line:
            query_text.append(text)
            text = ''
            continue
        if '<DOC>' in line:
             continue
        if '<DOCNO>' in line:
            query_IDS.append(line)
            #print line
            continue
        else:
            text += line
counter = 1
file = open("queriesRedefined.txt","w")


for i in range(len(query_text)):
    list =  query_text[i].splitlines()
    text = ''
    for x in xrange(len(list)):
        text = text.lstrip()
        text = text + list[x]
        text= text + ' '
    thelist = ["_", ":", "/", "!", "?", "#", "^", "*", "~", "&", "(", ")", "[", "]", "{", "}", "'", ";", '"', "$",
               "%", "|", ]
    for punctuation in thelist:
        text = text.replace(punctuation, '')
    text = text.lower()
    text = text.replace('\t', '')
    text = text.replace(',','')
    text = text.replace('.','')
    query_IDS[i] = int(query_IDS[i].split()[1])
    #print query_IDS[i]
    result = str(query_IDS[i])  +' ' + text
    file.write(result)
    file.write("\n")



# for i in range(abc):
#     print "hello"





