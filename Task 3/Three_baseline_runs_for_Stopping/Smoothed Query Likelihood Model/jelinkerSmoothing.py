import os
import math
import operator
import shutil

CORPUS_DIR = "../../Processed_stopped_corpus"
QUERY_FILE = "../../queriesRedefined.txt"
JELINEK_SCORES_DIR = "Jelinker Scores"
NUMBER_OF_DOCS = 0
LAMBDAVAL = 0.35


# for creating inverted index
FILENAMES_IN_CORPUS = []
INVERTED_INDEX = dict()
NK = dict()

def smoothed_query():

    queries = open(QUERY_FILE, "r")
    query = queries.readline()
    query_id = 1
    while query != "":
        score = calculate_jelinker(query.split())
        write_score(score, query_id)
        query_id += 1
        query = queries.readline()

def calculate_jelinker(query_words):

    TOTAL_WORDS_IN_COLLECTION = 374418

    doc_score = dict()
    for doc in FILENAMES_IN_CORPUS:

        length_of_doc = total_words(doc)

        score = 0
        for term in query_words:
            if term in INVERTED_INDEX:
                if doc in INVERTED_INDEX[term]:
                    firstTerm = float(1.0 - LAMBDAVAL)*(float(INVERTED_INDEX[term][doc])/float(length_of_doc))
                else:
                    firstTerm = 0.0
                secondTerm = float(LAMBDAVAL)*((float(calculate_cqi(term)))/float(TOTAL_WORDS_IN_COLLECTION))
                totalTerm = float(firstTerm + secondTerm)
                score += math.log(totalTerm)
        total_score = score
        doc_score.update({doc: total_score})

    doc_score = sorted(doc_score.items(), key=operator.itemgetter(1),reverse=True)  # sort them in descending order of score
    doc_score = doc_score[0:100]  # the assignment asks only top 100
    return doc_score

def calculate_cqi(term):
    count = 0
    list = INVERTED_INDEX[term]
    for item in list:
        count += INVERTED_INDEX[term][item]
    return count


def total_words_in_collection():
    count = 0
    for file in os.listdir(CORPUS_DIR):
        output = open(CORPUS_DIR +"/" + file)
        words = output.read().split()
        count = count + len(words)
        print file
    print count
    return count


def total_words(doc):
    file = open(CORPUS_DIR + "/"+doc, "r")
    words = file.read().split()
    return len(words)

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
    if os.path.exists(JELINEK_SCORES_DIR):
        shutil.rmtree(JELINEK_SCORES_DIR)
    os.mkdir(JELINEK_SCORES_DIR)


# write scores to files
def write_score(score, query_id):
    score_file = open(JELINEK_SCORES_DIR+"/Q" + str(query_id) +".txt", "w")
    builder = ""
    rank = 1 # from top to bottom
    for docid, score in score:
        builder += str(query_id) + "\tQ0\t" + docid + "\t" + str(rank) + "\t" + str(score) + "\tJELINEK_SCORES_DIR\n"
        rank += 1
    builder = builder[0: len(builder)-1] # delete the trailing "\n"
    score_file.write(builder)


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
    smoothed_query()

start()