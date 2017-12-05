import os
import math
import operator
import shutil

CORPUS_DIR = "../Corpus"
QUERY_FILE = "../queriesRedefined.txt"
TFIDF_SCORE_DIR = "TF-IDF Scores"
NUMBER_OF_DOCS = 0

# for creating inverted index
FILENAMES_IN_CORPUS = []
INVERTED_INDEX = dict()
NK = dict()

def tf_idf():
    calculate_nk()

    queries = open(QUERY_FILE, "r")
    query = queries.readline()
    query_id = 1
    while query != "":
        score = calculate_tfidf(query.split())
        write_score(score, query_id)
        query_id += 1
        query = queries.readline()

def calculate_tfidf(query_words):
    global NK
    nk = dict() #local
    reduced_inverted_index = dict() #local
    doc_score = dict()

    # doc_id => score

    query_term_frequency = dict()
    # term frequencies for each word in the given query
    for word in query_words:
        if not query_term_frequency.has_key(word):
            query_term_frequency.update({word: 1})
        else:
            query_term_frequency[word] += 1

    # building inverted index with only terms in the query
    for term in query_term_frequency:
        if not INVERTED_INDEX.has_key(term):
            reduced_inverted_index.update({term: {}})
        else:
            reduced_inverted_index.update({term: INVERTED_INDEX[term]})

    for word in query_words:
        if NK.has_key(word):
            number_of_docs = NK[word]
            nk[word] = number_of_docs

    for doc in FILENAMES_IN_CORPUS:
        length_of_doc = total_words(doc)
        for term in query_words:
            if term in INVERTED_INDEX and doc in INVERTED_INDEX[term]:
                tf = float(reduced_inverted_index[term][doc])/float(length_of_doc)
                idf = math.log(NUMBER_OF_DOCS/nk[term])
                score = tf*idf
                if doc in doc_score:
                    total_score = doc_score[doc] + score  # query consists of several words, so total needs to be found
                    doc_score.update({doc: total_score})
                else:
                    doc_score.update({doc: score})

    doc_score = sorted(doc_score.items(), key=operator.itemgetter(1),reverse=True)  # sort them in descending order of score
    return doc_score


def total_words(doc):
    file = open("../Corpus/"+doc, "r")
    words = file.read().split()
    return len(words)

def calculate_nk():
    global NK
    for key in INVERTED_INDEX:
        NK[key] = len(INVERTED_INDEX[key])



# Used in inverted index creation. Create inverted index from corpus
def process_corpus():
    global N_GRAM, INVERTED_INDEX, NUMBER_OF_DOCS
    retrieve_corpus()
    inverted_index = dict()
    for file_name in FILENAMES_IN_CORPUS:
        NUMBER_OF_DOCS += 1
        file_content = open(CORPUS_DIR + '/' + file_name, "r").read()
        inverted_index = generate_inverted_index_unigram(file_name, file_content, inverted_index)

    INVERTED_INDEX = inverted_index


# Used in inverted index creation. Generate the inverted index for unigram
def generate_inverted_index_unigram(docid, file_content, inverted_index):
    # split the document into each word separately
    global LENGTH_OF_DOC
    words = file_content.split()
    for word in words:
        inverted_index = create_inverted_index(word, docid, inverted_index)
    return inverted_index


# Used in inverted index creation. create the inverted index
def create_inverted_index(word, docid, inverted_index):
    # if the word doesnt exists, add it to the inverted index
    if not inverted_index.has_key(word):
        inverted_index[word] = {docid: 1}  # initial (docid, tf) format
    elif inverted_index[word].has_key(docid):
        # if the word and the docid exists, plus 1 to the term freq. for that docid
        doc_dict = inverted_index[word]
        term_freq_value = doc_dict.get(docid)
        term_freq_value = term_freq_value + 1
        doc_dict[docid] = term_freq_value
    else:
        # if word exists but the docid doesnt, append the current "docid" with initially term freq. of 1 to that word
        inverted_index[word].update({docid: 1})
    return inverted_index


# Used in inverted index creation. Gets all the file names in the given corpus
def retrieve_corpus():
    global FILENAMES_IN_CORPUS
    if os.path.exists(CORPUS_DIR):
        file_names = os.listdir(CORPUS_DIR)
        FILENAMES_IN_CORPUS = file_names

def delete_files():
    if os.path.exists(TFIDF_SCORE_DIR):
        shutil.rmtree(TFIDF_SCORE_DIR)
    os.mkdir(TFIDF_SCORE_DIR)


# write scores to files
def write_score(score, query_id):
    score_file = open(TFIDF_SCORE_DIR+"/Q" + str(query_id) +".txt", "w")
    builder = ""
    rank = 1 # from top to bottom
    for docid, score in score:
        builder += str(query_id) + "\tQ0\t" + docid + "\t" + str(rank) + "\t" + str(score) + "\tTFIDF\n"
        rank += 1
    builder = builder[0: len(builder)-1] # delete the trailing "\n"
    score_file.write(builder)


def write_file(content):
    file1 = open('sanjay.txt', "a")
    file1.write(str(content))


def start():
    global CORPUS_DIR, QUERY_FILE

    input_corpus = raw_input("Enter path to the Corpus directory generated from HW3-Task1 (Skip for Default): ")
    if input_corpus:
        CORPUS_DIR = input_corpus

    input_query = raw_input("Enter path to the query file (Skip for Default): ")
    if input_query:
        QUERY_FILE = input_query

    delete_files()
    process_corpus()  # this function generates the inverted index for unigram for the given corpus
    tf_idf()
    print NUMBER_OF_DOCS


start()