import xlwt
import xlrd
import os


EXCEL_FILE_NAME = "TF-IDF_Scores_STEMMING_RESULTS"
RESULTS_FOLDER_NAME = "TF-IDF Scores"

if not os.path.isdir(RESULTS_FOLDER_NAME):
    print("The Directory with TF-IDF Scores doesnt exist!")


book = xlwt.Workbook()
sorted_files = sorted(os.listdir(RESULTS_FOLDER_NAME) , key= lambda x : int(x.split("Q")[1].split(".")[0]) )
for file in sorted_files:
    # print(file)
    name = file.strip().split(".")
    # print("name", name[0])
    ws = book.add_sheet(name[0])  # Add a sheet
    dir_path = os.path.dirname(__file__)
    rel_path = "/"+RESULTS_FOLDER_NAME+"/" + file
    filepath = dir_path + rel_path
    fd = open(filepath)
    data = fd.readlines()
    fd.close()
    for i in range(len(data)):
        line_data = data[i].split()
        print(line_data)
        for k in range(len(line_data)):
            ws.write(i, k, line_data[k])

if os.path.isfile(EXCEL_FILE_NAME+".xls"):
    os.remove(EXCEL_FILE_NAME+".xls")

book.save(EXCEL_FILE_NAME+".xls")