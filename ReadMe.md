Final Project:
Goal-> To design and build a CACM based information retrieval system based on different ranking algorithms and then
evaluate their performance
------------------------------------------------------------------------------------------------------------------------
Members:

Sanjay Murali
Chaitanya Kaul
Akshay Singh
------------------------------------------------------------------------------------------------------------------------

Environment: Mac/Windows
Programming Language: Python 2.7
Requirements: Lucene 4.7, PDF Reader
------------------------------------------------------------------------------------------------------------------------
This readme file consists of all the instructions required to setup, compile and run the python files given in the
project.

Installation Guide:

-> Download Python 2.7.x from https://www.python.org/download/releases/2.7/
-> Download Pycharm from https://www.jetbrains.com/pycharm
-> Open the project using Pycharm.
-> Install BeautifulSoup addon which is used to process the corpus from https://www.crummy.com/software/BeautifulSoup/
-> Install Java SDK from http://www.oracle.com/technetwork/java/javase/downloads
------------------------------------------------------------------------------------------------------------------------

General Instructions on Executing each of the Python Scripts:

Task 1:

Pre-Process->

1. In Task 1 folder navigate to Task 1/Pre-process directory
2. The directory contains three scripts: gen-cacm-corpus-text.py, InvertedIndex.py and queryBreakdown.py
3. Execute gen-cacm-corpus-text.py which processes the HTML based CACM corpus and outputs the results in
   Corpus/ directory as .txt files.
4. Execute queryBreakdown.py which processes the Query files and generates a txt file called as queriesRedefined.txt
5. Execute invertedIndex.py which generates a file called "Term Frequency for Unigram.txt"

BM25->

1. Goto Task 1/BM25 directory and execute BM25.py to generate query-by-query results in BM25 Scores directory.
2. If you would like to generate a txt->xls conversion for result files, execute BM25_txt_to_xls.py script

Lucene->

1. Goto Task 1/Lucene/src/Lucene/HW4.java directory and execute the .java file.
2. The results will be generated in "DOC List Rank Lucene" folder
3. If you would like to generate a txt->xls conversion for result files, execute Lucene_txt_to_xls.py


TF-IDF->

1. Goto Task 1/tf-idf and execute tf-idf.py script.
2. The results will be generated in "TF-IDF Scores" directory.

Smoothed Query Likelihood Model->

1. Goto Task 1/Smoothed Query Likelihood Model and execute Jelinek-Smoothing.py script
2. The result files will be generated in "Jelinek Scores" directory.
------------------------------------------------------------------------------------------------------------------------

Task 2:

BM25 with Pseudo Relevance Feedback(Rocchio's Algorithm)

1. Navigate to Task 2/BM25 and execute BM25.py script to generate score txt files in the directory "BM25 Pseudo Scores".
2. The BM25 scores which are previously generated used for getting the relevant and non relevant documents is in the
   directory "BM25 Scores".
3. If you would like to generate a txt->xls conversion for result files, execute BM25_txt_to_xls.py.
------------------------------------------------------------------------------------------------------------------------

Task 3:

1. Navigate to Task 3/Generate_Stopped_Stemmed_corpus.py and execute it, which generates a new corpus for baseline runs.
2. Task 3/Processed_stem_corpus contains the corpus which is stemmed, Task 3/Processed_stopped_corpus contains the
   corpus which has all the stop words removed.
3. Three_baseline_runs_for_stemming contains three folders each having the score files and scripts for BM25, Smoothed
   Query Likelihood Model and TF-IDF.
4. Three_baseline_runs_for_Stopping contains three folders each having the score files and python scripts for BM25,
   Smoothed Query Likelihood Model and   TF-IDF.
------------------------------------------------------------------------------------------------------------------------

Phase-2:

* Phase-2 contains the source code, score files and Corpus for generating the snippets.
1. Execute snippetGeneration.py to generate snippets for each of the queries.
2. The result is stored in Snippets/ directory.
------------------------------------------------------------------------------------------------------------------------

Evaluation Phase:

1. Navigate to Evaluation directory and execute Query-Evaluation.py to generate results for precision, recall, MAP and MRR.
2. Result files are generated as "Precision_and_Recall.txt", "Precision_at_5.txt", "Precision_at_20.txt" and similarly
   for stopped version as "Stopped_Precision_and_Recall.txt",
   "Stopped_Precision_at_5.txt"and "Stopped_Precision_at_20.txt".
------------------------------------------------------------------------------------------------------------------------

Extra-Credit Phase:

1. Navigate to Extra Credit/BM25 directory and generate the new scores by executing BM25.py python script.
2. It will generate new scores in two directories, "Extra Credit/BM25 Scores" and "Extra Credit/BM25 Stopped Scores"