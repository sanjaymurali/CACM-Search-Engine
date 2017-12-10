import os

import operator

MODEL = "BM25_Proximity_Enabled"

INPUT_SCORES_DIR = "../Extra Credit/BM25/BM25 Scores"
OUTPUT_TEXT = MODEL+"_Precision_and_Recall.txt"
OUTPUT_PRECISION_20 = MODEL+"_Precision_at_20.txt"
OUTPUT_PRECISION_5 = MODEL+"_Precision_at_5.txt"
CACM_REL_PATH = "cacm.rel.txt"
SCORES_TO_CONSIDER = []
CACM_REL = dict()
RECALL = dict()
PRECISION = dict()
AVERAGE_PRECISIONS = []
RECIPROCAL_RANKS = []
PRECISION_AT_5 = dict()
PRECISION_AT_20 = dict()

def calculate_recall_precision():
    # there are 64 queries, so iterating through all of them
    global RECALL, PRECISION
    for i in range(1, 65):
        query_id = str(i)
        if CACM_REL.has_key(query_id):
            RECALL[query_id] = recall_query(query_id)
            PRECISION[query_id] = precision_query(query_id)


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
    recall = dict()
    length_A = len(A)
    for document in B:
        if document in A:
            AintersectionB += 1
        recall[document] = (float(AintersectionB)/float(length_A))
    return recall

def precision_query(query_id):
    A = CACM_REL[query_id]
    B = get_documents(query_id)
    AintersectionB = 0
    precision = dict()
    length_B = 0
    for document in B:
        length_B += 1
        if document in A:
            AintersectionB += 1
        precision[document] = (float(AintersectionB)/float(length_B))
    return precision

def average_precision(query_id):
    global AVERAGE_PRECISIONS
    if PRECISION.has_key(query_id):
        relevant_doc = CACM_REL[query_id]

        precisions = PRECISION[query_id]
        sum = 0
        counter = 0
        for every_precision in precisions:
            if every_precision in relevant_doc:
                counter += 1
                #print precisions[every_precision]
                sum += precisions[every_precision]
        if counter == 0:
            ap = 0
        else:
            ap = float(sum)/float(counter)
        AVERAGE_PRECISIONS.append(ap)
        return ap

def mean_average_precision():
    sum = 0
    counter = 0
    for ap in AVERAGE_PRECISIONS:
        counter += 1
        if ap != 0:
            sum += ap
    print counter
    map = float(sum)/float(counter)
    return map

def write_precision_recall():
    global RECIPROCAL_RANKS,PRECISION_AT_5, PRECISION_AT_20
    precision_recall_file_lines = ""

    for file in range(1,65):
        filename = "Q"+str(file)+".txt"
        query_id_outer = str(file)
        first_relevant_boolean = False
        rank = 0.0
        if CACM_REL.has_key(query_id_outer):
            query_file = open(INPUT_SCORES_DIR + "/" + filename, "r").read()
            opened_file = query_file.split("\n")
            line_number = 1
            for line in opened_file:
                words = line.split()
                document = words[2]
                rank_of_doc = int(words[3])
                document = document.split(".txt")[0]
                if rank_of_doc == 5:
                    PRECISION_AT_5[query_id_outer] = PRECISION[query_id_outer][document]
                if rank_of_doc == 20:
                    PRECISION_AT_20[query_id_outer] = PRECISION[query_id_outer][document]
                if relevant_or_not(query_id_outer, document):
                    type_of_document = "Relevant"
                    if first_relevant_boolean == False:
                        RECIPROCAL_RANKS.append(rank_of_doc)
                        rank = rank_of_doc
                        first_relevant_boolean = True
                else:
                    type_of_document = "Non-Relevant"
                precision_recall_file_lines += line + "\t" + type_of_document + "\t"
                precision_recall_file_lines += str(PRECISION[query_id_outer][document]) + "\t" + str(
                    RECALL[query_id_outer][document]) + "\n"
                line_number += 1
            precision_recall_file_lines += "\nAverage Precision of Query " + query_id_outer + ": "  + str(average_precision(query_id_outer)) + "\n"
            precision_recall_file_lines += "Reciprocal Rank of Query " + query_id_outer + ": "  + str(rank) + "\n\n"
        else:
            precision_recall_file_lines += "Query Q" + query_id_outer + " has no Relevant Terms. Precision: 0 and Recall: 0\n\n"

    precision_recall_file_lines += "Mean Average Precision: " + str(mean_average_precision()) + "\n"
    precision_recall_file_lines += "Mean Reciprocal Rank: " + str(mean_reciprocal_ranks())
    precision_recall_file_lines = precision_recall_file_lines.rstrip()
    new_file = open(OUTPUT_TEXT, "w")
    new_file.write(precision_recall_file_lines)

def write_precision_at_5():
    precision_at_5 = sorted(PRECISION_AT_5.items(),key= lambda x: int(x[0]))
    precision_at_5_lines = ""
    for one in precision_at_5:
        precision_at_5_lines += "Precision of Query " + one[0] + " at 5 is: " + str(one[1]) + "\n"
    precision_at_5_lines = precision_at_5_lines.rstrip()
    precision_at_5_file = open(OUTPUT_PRECISION_5, "w")
    precision_at_5_file.write(precision_at_5_lines)

def write_precision_at_20():
    precision_at_20 = sorted(PRECISION_AT_20.items(),key= lambda x: int(x[0]))
    precision_at_20_lines = ""
    for one in precision_at_20:
        precision_at_20_lines += "Precision of Query " + one[0] + " at 20 is: " + str(one[1]) + "\n"
    precision_at_20_lines = precision_at_20_lines.rstrip()
    precision_at_20_file = open(OUTPUT_PRECISION_20, "w")
    precision_at_20_file.write(precision_at_20_lines)

def mean_reciprocal_ranks():
    sum = 0
    print len(RECIPROCAL_RANKS)
    for rank in RECIPROCAL_RANKS:
        sum += float(1.0/float(rank))
    mrr = float(sum)/float(len(RECIPROCAL_RANKS))
    return mrr

def relevant_or_not(query_id, doc):
    if CACM_REL.has_key(query_id):
        if doc in CACM_REL[query_id]:
            return True
        else:
            return False

def start():

    process_cacm_rel() # process relevance judgement given to us
    read_dir() # sets the scores to consider for evaluation, disregard any query which has no relevance judgement
    calculate_recall_precision()
    write_precision_recall()
    write_precision_at_5()
    write_precision_at_20()
    # print mean_average_precision()
    # print mean_reciprocal_ranks()
start()