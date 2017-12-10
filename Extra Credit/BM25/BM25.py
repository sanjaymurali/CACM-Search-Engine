import json
import os
import math
import operator
import shutil

import itertools

CORPUS_DIR = "../Processed_stopped_corpus"
QUERY_FILE = "../queriesRedefined.txt"
BM25_SCORE_DIR = "BM25 Stopped Scores"
CACM_REL = "cacm.rel.txt"

# for creating inverted index
FILENAMES_IN_CORPUS = []
INVERTED_INDEX = dict() # looks like this: {term1 => {docidx: {count: xx, positions: []}}, term2 => {docidx: {count: xx, positions: []}} ...}
REL_INFO = dict()

# part of calculating BM25 score
LENGTH_OF_DOC = dict() # contains the length of each document in the corpus
AVERAGE_LENGTH_OF_DOC = 0 # average length of a document in the corpus "AVDL"

# read the query file, calculate BM25 score for each query and write them on to disk
def BM25():
    queries = open(QUERY_FILE, "r")
    query = queries.readline()
    query_id = 1
    while query != "":
        score = calculate_BM25(query.split(), query_id)
        write_score(score, query_id)
        query_id += 1
        query = queries.readline()

# The actual BM25 formula.
def BM25_Formula(n, qf, f, dl, R, r):
    N = len(LENGTH_OF_DOC) # total number of documents
    k1 = 1.2
    k2 = 100
    b = 0.75
    K = k1*((1-b) + b*(float(dl)/float(AVERAGE_LENGTH_OF_DOC)))
    first_part = math.log(((r + 0.5)/(R - r + 0.5))/((n - r + 0.5)/(N - n - R + r + 0.5)))
    second_part = ((k1 + 1)*f)/(K + f)
    third_part = ((k2 + 1) * qf)/(k2 + qf)
    total = first_part*second_part*third_part
    return total

# given a array of Strings, it calculates the BM25 score for the given query
def calculate_BM25(query_words, query_id):
    doc_score = dict()
    query_term_frequency = dict()
    # term frequencies for each word in the given query
    for word in query_words:
        if not query_term_frequency.has_key(word):
            query_term_frequency.update({word: 1})
        else:
            query_term_frequency[word] += 1

    # building inverted index with only terms in the query
    query_inverted_index = dict()
    for term in query_term_frequency:
        if not INVERTED_INDEX.has_key(term):
            query_inverted_index.update({term: {}})
        else:
            query_inverted_index.update({term: INVERTED_INDEX[term]})


    query_pairs = form_query_pairs(query_words)
    qwi = dict()

    # to calculate initial scores RSVold
    for term in query_inverted_index:
        if INVERTED_INDEX.has_key(term):

            qwi[term] = calculate_qwi(term, query_term_frequency[term])

            n = len(INVERTED_INDEX[term]) # number of documents containing the term
            qf = query_term_frequency[term] # query frequency
            for doc_id in query_inverted_index[term]:
                f = INVERTED_INDEX[term][doc_id]['count'] # frequency of the term in the given document
                if LENGTH_OF_DOC.has_key(doc_id):
                    dl = LENGTH_OF_DOC[doc_id] # length of the document, given the docid
                if REL_INFO.has_key(str(query_id)):
                    R = len(REL_INFO[str(query_id)])
                    r = reverse_doc_search(term, query_id)
                else:
                    R = 0
                    r = 0
                score = BM25_Formula(n, qf, f, dl, R, r) # the actual BM25 score for the given term
                if doc_id in doc_score:
                    total_score = doc_score[doc_id] + score # query consists of several words, so total needs to be found
                    doc_score.update({doc_id: total_score})
                else:
                    doc_score.update({doc_id: score})

    TPSRV_intermediate = 0
    TPSRV = dict()

    for doc_id in doc_score:
        TPSRV_intermediate = 0
        for each_pair in query_pairs:
            first_part_tpsrv = calculate_wdi(doc_id, each_pair, qwi)
            if qwi.has_key(each_pair[0]) and qwi.has_key(each_pair[1]):
                second_part_tpsrv = min(qwi[each_pair[0]], qwi[each_pair[1]])
                TPSRV_intermediate += float(first_part_tpsrv) * float(second_part_tpsrv)
                if TPSRV.has_key(doc_id):
                    TPSRV.update({doc_id: TPSRV_intermediate})
                else:
                    TPSRV[doc_id] = TPSRV_intermediate

    for doc_id in doc_score:
        value = doc_score[doc_id]
        value += TPSRV[doc_id]
        doc_score[doc_id] = value

    doc_score = sorted(doc_score.items(), key=operator.itemgetter(1), reverse=True) # sort them in descending order of score
    doc_score = doc_score[0:100] # the assignment asks only top 100
    print doc_score
    return doc_score

def calculate_tpi(term1pos, term2pos):
    numerator = float(1.0)
    denominator = float(math.pow((term2pos - term1pos), 2))
    tpi = float(numerator)/float(denominator)
    return tpi

def allowed_query_pair(term1, term2):
    # term1 and term2 must be within 3 terms
    # representation : term1 => {'count': x, 'position': [x , y]}
    positions1 = term1['position']
    positions2 = term2['position']
    position_pairs = []
    for position1 in positions1:
        for position2 in positions2:
            distance = position2 - position1
            if distance > 0 and distance <= 3:
                position_pairs.append([position1, position2])
    return position_pairs


def calculate_wdi(doc_id, pair, qwi):
    try:
        term1 = INVERTED_INDEX[pair[0]].get(doc_id)
        term2 = INVERTED_INDEX[pair[1]].get(doc_id)
    except:
        return 0

    if term1 is None or term2 is None:
       return 0
    else:
        pairs_to_consider = allowed_query_pair(term1, term2) # for each docid and for given 2 terms
        if len(pairs_to_consider) == 0:
            return 0
        else:
            tpi = 0
            k1 = 1.2
            b = 0.75
            K = k1 * ((1 - b) + b * (float(LENGTH_OF_DOC[doc_id]) / float(AVERAGE_LENGTH_OF_DOC)))
            for each_pair in pairs_to_consider:
                tpi += calculate_tpi(each_pair[0], each_pair[1])
            first_part = float(k1 + 1.0)
            second_part_numerator = float(tpi)
            second_part_denominator = float(K + tpi)
            wd = float(first_part) * float(second_part_numerator/second_part_denominator)
            return wd

def calculate_qwi(term, term_frequency_in_query):
    first_part = float(term_frequency_in_query)/float(100.0 + term_frequency_in_query)
    DFI = float(len(INVERTED_INDEX[term]))
    second_part = math.log(float(3204 - DFI)/DFI)
    qwi = float(first_part * second_part)
    return qwi

def form_query_pairs(query_words):
    permuations = []
    for i in range(len(query_words)):
        for j in range(i+1, len(query_words)):
            if query_words[i] != query_words[j]:
                if not [query_words[i], query_words[j]] in permuations:
                    permuations.append([query_words[i], query_words[j]])
    return permuations

# Used in inverted index creation. Create inverted index from corpus
def process_corpus():
    global N_GRAM, INVERTED_INDEX
    retrieve_corpus()
    inverted_index = dict()
    for file_name in FILENAMES_IN_CORPUS:
        file_content = open(CORPUS_DIR + '/' + file_name, "r").read()
        inverted_index = generate_inverted_index_unigram(file_name, file_content, inverted_index)

    INVERTED_INDEX = inverted_index


# Used in inverted index creation. Generate the inverted index for unigram
def generate_inverted_index_unigram(docid, file_content, inverted_index):
    # split the document into each word separately
    global LENGTH_OF_DOC
    words = file_content.split()
    LENGTH_OF_DOC[docid] = len(words)
    position = 0 # initial pointer
    for word in words:
        position += 1
        inverted_index = create_inverted_index(word, docid, position, inverted_index)
    return inverted_index


# Used in inverted index creation. create the inverted index
def create_inverted_index(word, docid, position, inverted_index):

    # if the word doesnt exists, add it to the inverted index
    if not inverted_index.has_key(word):
        json = {
            docid: {
                'count': 1,
                'position': [position]
        }
        }
        inverted_index[word] =  json # initial (docid, tf) format
    elif inverted_index[word].has_key(docid):
        # if the word and the docid exists, plus 1 to the term freq. for that docid
        doc_dict = inverted_index[word]

        term_freq_value = doc_dict.get(docid).get('count')
        term_freq_value = term_freq_value + 1
        doc_dict[docid]['count'] = term_freq_value

        position_value = doc_dict.get(docid).get('position')
        position_value.append(position)
        doc_dict[docid]['position'] = position_value

        inverted_index[word][docid]['count'] = term_freq_value
        inverted_index[word][docid]['position'] = position_value
    else:
        # if word exists but the docid doesnt, append the current "docid" with initially term freq. of 1 to that word
        json = {
            docid: {
                'count': 1,
                'position': [position]
            }
        }
        inverted_index[word].update(json)
    return inverted_index


# Used in inverted index creation. Gets all the file names in the given corpus
def retrieve_corpus():
    global FILENAMES_IN_CORPUS
    if os.path.exists(CORPUS_DIR):
        file_names = os.listdir(CORPUS_DIR)
        FILENAMES_IN_CORPUS = file_names

# to get the average document length in the corpus
def get_average_length_of_doc():
    global AVERAGE_LENGTH_OF_DOC
    sum = 0
    for lengths in LENGTH_OF_DOC.values():
        sum += lengths
    avg = float(sum)/float(len(LENGTH_OF_DOC))
    AVERAGE_LENGTH_OF_DOC = avg

# write scores to files
def write_score(score, query_id):
    score_file = open(BM25_SCORE_DIR+"/Q" + str(query_id) +".txt", "w")
    builder = ""
    rank = 1 # from top to bottom
    for docid, score in score:
        builder += str(query_id) + "\tQ0\t" + docid + "\t" + str(rank) + "\t" + str(score) + "\tBM25\n"
        rank += 1
    builder = builder[0: len(builder)-1] # delete the trailing "\n"
    score_file.write(builder)

def relevance_info():
    global REL_INFO
    rel_file = open(CACM_REL, "r").read()
    lines = rel_file.split("\n")
    for line in lines:
        if len(line) != 0:
            words = line.split() # word[0] => query_id, word[2] => document_id
            if REL_INFO.has_key(words[0]):
                REL_INFO[words[0]].append(words[2])
            else:
                REL_INFO[words[0]] = [words[2]]

def reverse_doc_search(term, query_id):
    documents = INVERTED_INDEX[term]
    sum = 0
    for document in REL_INFO[str(query_id)]:
        document = document + ".txt"
        for inverted_document in documents:
            if inverted_document == document:
                sum = sum + 1
    return sum


def delete_files():
    if os.path.exists(BM25_SCORE_DIR):
        shutil.rmtree(BM25_SCORE_DIR)
    os.mkdir(BM25_SCORE_DIR)

# starter program
def start():
    global CORPUS_DIR, QUERY_FILE, CACM_REL

    # input_corpus = raw_input("Enter path to the Corpus directory generated from HW3-Task1 (Skip for Default): ")
    # if input_corpus:
    #     CORPUS_DIR = input_corpus
    #
    # input_query = raw_input("Enter path to the query file (Skip for Default): ")
    # if input_query:
    #     QUERY_FILE = input_query
    #
    # input_cacm = raw_input("Enter path to the REL file (Skip for Default): ")
    # if input_cacm:
    #     CACM_REL = input_cacm

    delete_files()

    process_corpus() # this function generates the inverted index for unigram for the given corpus
    get_average_length_of_doc() # this function helps in calculating "AVDL", average document length in the corpus
    relevance_info()
    BM25()


start()