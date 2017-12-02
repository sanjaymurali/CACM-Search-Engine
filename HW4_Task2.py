from urllib.request import urlopen
from urllib.parse import *
from urllib.error import *
import time
import string
from bs4 import BeautifulSoup
import re
import os
import io
import math
import ast
import nltk

INPUT_FILE_NAME = "Inverted_Index1_gram.txt"

input_file = open(INPUT_FILE_NAME, 'r', encoding='utf8')

queries_to_evaluate = ['hurricane isabel damage', 'forecast models', 'green energy canada', 'heavy rains',
                       'hurricane music lyrics', 'accumulated snow', 'snow accumulation', 'massive blizzards blizzard',
                       'new york city subway']

inverted_term_doc_dict = {}
if input_file:
    for line in input_file:
        first_parting_index = line.find(":")
        key_part = line[:first_parting_index]
        key_part = re.sub('[\/:*?"<>|%]', "", key_part)
        key_part = key_part.strip()
        value_part = line[first_parting_index + 1:]
        value_part = value_part.replace("\n", "")
        value_part = value_part.strip()
        value_part_str = str(value_part)
        value_part_dict = ast.literal_eval(value_part_str)
        inverted_term_doc_dict[key_part] = value_part_dict
    doc_length = {}
    for key in inverted_term_doc_dict.keys():
        temp_dict = inverted_term_doc_dict[key]
        for docs in temp_dict.keys():
            if docs in doc_length:
                doc_length[docs] += len(key) * temp_dict[docs]
            else:
                doc_length[docs] = len(key) * temp_dict[docs]

    average_doc_length = 0

    for doc in doc_length.keys():
        average_doc_length += doc_length[doc]

    average_doc_length = average_doc_length / float(len(doc_length.keys()))
    k2 = 100
    b = 0.75
    k1 = 1.2
    keys_List = list(inverted_term_doc_dict.keys())
    system_name = "Akshay Singh"
    query_id = 0
    for query in queries_to_evaluate:
        query_id += 1
        words_in_query = query.split(" ")
        related_docs = []
        for word in words_in_query:
            if word in keys_List:
                temp_doc_dict = inverted_term_doc_dict[word]
                for d in temp_doc_dict.keys():
                    if d not in related_docs:
                        related_docs.append(d)
        document_bm_25_score = {}
        for rdocs in related_docs:
            fraction_doc_length = doc_length[rdocs] / float(average_doc_length)
            K = k1 * ((1 - b) + (b * fraction_doc_length))
            processing_value_query_doc = 0
            for word2 in words_in_query:
                word_count_query = words_in_query.count(word2)
                r = 0
                R = 0
                numer = (r + 0.5) / float(R - r + 0.5)
                if rdocs in inverted_term_doc_dict[word2].keys():
                    temp_dict_count_word = inverted_term_doc_dict[word2]
                    word_count_in_doc = temp_dict_count_word[rdocs]
                else:
                    word_count_in_doc = 0
                numer2 = (k1 + 1) * word_count_in_doc
                numer3 = (k2 + 1) * word_count_query
                if word2 in inverted_term_doc_dict:
                    num_doc_word2 = len(inverted_term_doc_dict[word2])
                else:
                    num_doc_word2 = 0
                denom1_a = num_doc_word2 - r + 0.5
                total_Doc_count = len(doc_length)
                denom1_b = total_Doc_count - num_doc_word2 - R + r + 0.5

                denom1 = denom1_a / float(denom1_b)
                denom2 = K + word_count_in_doc
                denom3 = k2 + word_count_query

                temp_value = numer * numer2 * numer3 / float(denom1 * denom2 * denom3)
                if temp_value == 0:
                    processing_value_query_doc += 0
                else:
                    processing_value_query_doc += math.log(temp_value)
            document_bm_25_score[rdocs] = processing_value_query_doc

        sorted_document_bm_25_score = list(sorted(document_bm_25_score.items(), key=lambda x: x[1], reverse=True))[:100]

        rank = 1
        filename = "Assignment4_Task_2_query_" + str(query_id) + ".txt"
        for item1, item2 in sorted_document_bm_25_score:
            content = str(query_id) + " Q0 " + item1 + " " + ("%.2f" % round(item2, 2)) + " " + system_name
            if os.path.isfile(filename):
                with open(filename, 'a') as g:
                    g.write(content)
                    g.write("\n")
                    g.close()
            else:
                with open(filename, 'w') as h:
                    h.write(content)
                    h.write("\n")
                    h.close()
else:
    print("Input File does not Exist.")
