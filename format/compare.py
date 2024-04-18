import csv

def compare_csv(csv1_file, csv2_file):
    with open(csv1_file, 'r') as file1, open(csv2_file, 'r') as file2:
        csv1_reader = csv.reader(file1)
        csv2_reader = csv.reader(file2)
        
        csv1_data = [row for row in csv1_reader]
        csv2_data = [row for row in csv2_reader]
        
        updated_csv2_data = []
        
        for row1 in csv1_data:
            match_found = False
            for row2 in csv2_data:
                if row1[:3] == row2[:3]:
                    match_found = True
                    updated_csv2_data.append(row2)
                    break
            
            if not match_found:
                print(f"Row {row2} removed from CSV2")
        
        with open('updated_csv2.csv', 'w', newline='') as updated_file:
            writer = csv.writer(updated_file)
            writer.writerows(updated_csv2_data)
        
        print("Comparison completed. Updated CSV2 saved as 'updated_csv2.csv'.")
        
cea1 = "format/WikidataTables2023/DataSets/Valid/gt/cea_gt.csv"
cea2 = 'format/WikidataTables2023/submission/cea/cea.csv'
# Appel de la fonction avec les noms des fichiers CSV en entrée
compare_csv(cea1, cea2)
