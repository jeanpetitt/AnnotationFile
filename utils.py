import csv
import os
import re
import requests
import pandas as pd
import numpy as np
from api import openUrl

# wikidata cea annotation


def annotateCea(path_folder):
    files_cea = 'cea.csv'
    # lister les fichiers dans le dataset
    dataset = os.listdir(path_folder)
    # trier le dataset par ordre alphabetique
    dataset.sort(reverse=False)
    # creer l'entête des fichier ce
    header_cea = ["tab_id", "col_id", "row_id", "entity"]
    # open output cea file to write inside
    with open(files_cea, "w+") as csv_file:
        writer = csv.writer(csv_file, delimiter=",")
        writer.writerow(header_cea)
        # get filename from each file in dataset
        for filed in dataset:
            # read only csv file insie in dataset
            if filed.endswith(".csv"):
                print(filed)
                # open current clean file in dataset with pandas dataframe
                _file = pd.read_csv(f"{path_folder}/{filed}")
                # get total row and colums of each cleaned file csv
                total_rows = len(_file.axes[0])
                total_cols = len(_file.axes[1])

                # parcourit chaque cellule de chaque colonne en effectuant la recherche sur
                # wikidata
                list_uri = []
                cells_firs_line = [cell for cell in _file.loc[0]]
                print(cells_firs_line)

                for cols in _file.columns:
                    for i, line in _file.iterrows():
                        if isinstance(line[cols], str):
                            result = openUrl(line[cols])
                            # verify if we have result of the search query
                            if result == "No result":
                                list_uri.append("NIL")
                            else:
                                list_uri.append(result)
                        # verify if cell is empty by default in dataframe all empty cell called nan
                        elif type(line[cols]) == type(np.nan):
                            list_uri.append("NIL")
                print(len(list_uri))
                # get name of cleaned file
                filename = filed.split(".")[0]
                print("fichier:", filename, "nbre de ligne: ",
                      total_rows, " nombre de col: ", total_cols)
                filetotalrowcol = total_rows * total_cols
                row = 0
                col = 0
                uri_n = 0
                # creer la structure d'un fichier cea
                while row < filetotalrowcol:
                    # for cell in total_cols:
                    if row < total_rows:
                        if list_uri[uri_n] == "NIL":
                            writer.writerow(
                                [filename, col, row, list_uri[uri_n]])
                            row += 1
                            uri_n += 1
                        else:
                            writer.writerow(
                                [filename, col, row, list_uri[uri_n]])
                            row += 1
                            uri_n += 1
                    else:
                        row = 0
                        filetotalrowcol -= total_rows
                        col += 1
                        # end structure cea.csv
            else:
                print("it is not csv file")

    csv_file.close()

    # read output cea csv file
    print("============cea=============")
    _test_cea = pd.read_csv(files_cea)
    data_cea = _test_cea.loc[0:]
    print(data_cea)


annotateCea('clean_table_en/tables_WD')
