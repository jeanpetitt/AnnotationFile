import pandas as pd, numpy as np
import os, csv

def openFolder(path_folder):
    list_file = os.listdir(path_folder)
    
    print(len(list_file))
    return list_file

def openCSVFile(path):
    df = pd.read_csv(path, header=None)
    
    col1 = df[0]
    cols = []
    cols_not = []
    for i in col1:
        # print(i)
        cols.append(i)
    
    # remove duplicate key
    for i in cols[0:]:
        if i not in cols_not:
            cols_not.append(i)
    print(cols_not)
    print(len(cols_not))
    
    return cols_not
    
    # print(col1)

def fileCea(files_cea, path, cea_target_path):
    dataset = openCSVFile(cea_target_path)
    header_cea = ["tab_id", "row_id", "col_id", "entity", 'context']
	# open output cea file to write inside 
    with open(files_cea, "w+") as csv_file:
        writer = csv.writer(csv_file, delimiter=",")
        # writer.writerow(header_cea)
		# get filename from each file in dataset
        for filed in dataset:
            filed += ".csv"
            if filed.endswith(".csv"):
                _file = pd.read_csv(f"{path}/{filed}")
                # get total row and colums of each cleaned file csv
                total_rows = len(_file.axes[0])
                total_cols=len(_file.axes[1])
                list_uri = []
                # cells_firs_line = [cell for cell in _file.loc[0]]
                # # print(cells_firs_line)
                for cols in _file.columns:
                    for i, row in _file.iterrows():
                        if type(row[cols]) == type(np.nan):	
                            list_uri.append(["NIL", row.values])
                        else:
                            list_uri.append([row[cols], row.values])
        
                print(len(list_uri))
                filename = filed.split(".")[0]
                print("fichier:", filename, "nbre de ligne: ", total_rows, " nombre de col: ", total_cols)
                filetotalrowcol = total_rows * total_cols
                print("File total size: ", filetotalrowcol)
                row = 0
                col = 0
                uri_n = 0
                while row < filetotalrowcol:
                        if row < total_rows:
                            writer.writerow([filename, row+1, col, list_uri[uri_n][0], list_uri[uri_n][1]])
                            row += 1
                            uri_n +=1
                        else:
                            row = 0
                            filetotalrowcol -= total_rows
                            col += 1
            else:
                print("it is not csv file")
                csv_file.close()
    
    print("============cea=============")
    _test_cea = pd.read_csv(files_cea)
    data_cea =_test_cea.loc[0:]
    print(data_cea)

cea_target = "format/WikidataTables2023/DataSets/Valid/gt/cea_gt.csv"
output_cea = 'format/WikidataTables2023/submission/cea/cea.csv'
dataset_path = "format/WikidataTables2023/DataSets/Valid/tables"

# openCSVFile(cea_target)
# openFolder("format/WikidataTables2023/DataSets/Valid/tables")
fileCea(files_cea=output_cea, path=dataset_path, cea_target_path=cea_target)