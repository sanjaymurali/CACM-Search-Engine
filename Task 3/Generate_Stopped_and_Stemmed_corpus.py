import os
from os import listdir

CORPUS_DIRECTORY_PATH = "D:\IR_Project_CS6200\IR_Project\Task 1\Corpus"
PROCESSED_CORPUS_DIRECTORY_PATH = "D:\IR_Project_CS6200\IR_Project\Task 3\Processed_stopped_corpus"
PROCESSED__STEM_CORPUS_DIRECTORY_PATH = "D:\IR_Project_CS6200\IR_Project\Task 3\Processed_stem_corpus"
STEMMED_CORPUS_FILE= "cacm_stem.txt"
STOP_WORDS_FILENAME = "common_words.txt"




def remove_trailing_zeros(temp_text):
    integers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    first_int_index = 0
    for x in range(len(temp_text) - 1, -1, -1):
        if temp_text[x][0] in integers:
            continue
        else:
            first_int_index = x
            break
    return temp_text[:first_int_index + 1]


def process_corpus_stopping(corpus_path, proccessed_corpus_path , stopwords_file_name):
    if not os.path.exists(proccessed_corpus_path):
        os.makedirs(proccessed_corpus_path)

    files = listdir(corpus_path)
    stop_words_fd = open(stopwords_file_name ,"r")
    stop_words = stop_words_fd.read().strip().split("\n")
    stop_words_fd.close()

    for file in files:
        file_path = corpus_path+"\\"+file
        with open(file_path, "r") as g:
            temp_text  = g.read().strip().split(" ")
        g.close()

        processed_temp_text = remove_trailing_zeros(temp_text)

        processed_text = []

        for word in processed_temp_text:
            if word not in stop_words:
                processed_text.append(word)


        processed_corpus = " ".join(processed_text)

        processed_file_name = file
        processed_file_path = proccessed_corpus_path+"\\"+processed_file_name

        if os.path.isfile(processed_file_path):
            os.remove(processed_file_path)

        with open(processed_file_path, "w") as k:
            k.write(processed_corpus)
        k.close()

def remove_trailing_zero_stemmed_corpus(stem_corpus_path):
    files = listdir(stem_corpus_path)

    for file in files:
        file_path = stem_corpus_path + "\\" + file
        with open(file_path, "r") as g:
            temp_text = g.read().strip().split(" ")
        g.close()
        processed_temp_text = remove_trailing_zeros(temp_text)
        processed_corpus = " ".join(processed_temp_text)

        processed_file_name = file
        processed_file_path = stem_corpus_path + "\\" + processed_file_name

        if os.path.isfile(processed_file_path):
            os.remove(processed_file_path)

        with open(processed_file_path, "w") as k:
            k.write(processed_corpus)
        k.close()


def create_stemmed_corpus(stemmed_common_corpus_file , processed_stem_corpus_dir):
    if not os.path.exists(processed_stem_corpus_dir):
        os.makedirs(processed_stem_corpus_dir)
    file_num = ""
    with open(stemmed_common_corpus_file,"r") as h:
        for line in h:
            if line[0] == "#":
                split_line = line.strip().split(" ")
                file_num = split_line[1].strip().split("\n")[0]
                int_file_num = "%04d" % (int(file_num),)
                file_num = str(int_file_num)
            else:
                file_name = "CACM-" + file_num + ".txt"
                filePath = processed_stem_corpus_dir + "\\" + file_name
                if os.path.isfile(filePath):
                    with open(filePath,"a") as m:
                        processed_line = line.replace("\n", " ")
                        m.write(processed_line)
                    m.close()
                else:
                    with open(filePath,"w") as n:
                        processed_line = line.replace("\n", " ")
                        n.write(processed_line)
                    n.close()
    remove_trailing_zero_stemmed_corpus(processed_stem_corpus_dir)



process_corpus_stopping(CORPUS_DIRECTORY_PATH, PROCESSED_CORPUS_DIRECTORY_PATH, STOP_WORDS_FILENAME)
create_stemmed_corpus(STEMMED_CORPUS_FILE, PROCESSED__STEM_CORPUS_DIRECTORY_PATH)