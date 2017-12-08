import os

INPUT_SCORES_DIR = "../Task 1/BM25/BM25 Scores"
CACM_REL_PATH = "cacm.rel.txt"
SCORES_TO_CONSIDER = []
CACM_REL = dict()

def read_dir():
    global SCORES_TO_CONSIDER
    for file in os.listdir(INPUT_SCORES_DIR):
        query_id = file.split('Q')
        query_id_in = query_id[1].split('.txt')
        if CACM_REL.has_key(query_id_in[0]):
            SCORES_TO_CONSIDER.append(file)

def process_cacm_rel():
    global CACM_REL
    cacm_rel_file = open(CACM_REL_PATH, "r").read()
    cacm_rel_info = [line for line in cacm_rel_file.split('\n') if line.strip() != '']

    for rel_info in cacm_rel_info:
        words = rel_info.split()
        query_id = words[0]
        document = words[2]
        if CACM_REL.has_key(query_id):
            CACM_REL[query_id].append(document)
        else:
            CACM_REL[query_id] = [document]

    #print CACM_REL

# Fetches the documents for a query from the Input score directory
def get_documents(query_id):
    construct_path = INPUT_SCORES_DIR + "/Q" + query_id + ".txt"
    document_list = []
    if os.path.exists(construct_path):
        query_file = open(construct_path, "r").read()
        opened_file = query_file.split("\n")
        for line in opened_file:
            words = line.split()
            filename = words[2].split(".txt")
            document_list.append(filename[0])
    return document_list

def recall_query(query_id):
    A = CACM_REL[query_id]
    B = get_documents(query_id)
    AintersectionB = 0
    recall = []
    length_A = len(A)
    for document in B:
        if document in A:
            AintersectionB += 1
        recall.append(float(AintersectionB)/float(length_A))
    return recall

def precision_query(query_id):
    A = CACM_REL[query_id]
    B = get_documents(query_id)
    AintersectionB = 0
    precision = []
    length_B = 0
    for document in B:
        length_B += 1
        if document in A:
            AintersectionB += 1
        precision.append(float(AintersectionB)/float(length_B))

    return precision


def start():
    print "hello"
    process_cacm_rel() # process relevance judgement given to us
    read_dir() # sets the scores to consider for evaluation, disregard any query which has no relevance judgement
    print recall_query("1")
    print precision_query("1")

start()