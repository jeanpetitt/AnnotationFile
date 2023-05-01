
import requests
import csv,os, re, pandas as pd, numpy as np
from openapi import get_uri_cpa

path = f"{os.getcwd()}/dataset" 
"""
=============== wikida annotation=========================
"""
# get urls of wikidata of cea and cta
def openUrL(query):
	url = "https://www.wikidata.org/w/api.php"
	# verifier si la chaine contient des tirets ou des espace
	new_query = []
	for word in query.split():
		if '-' in word:
			new_query.append(word.split("-"))
		elif '' in word:
			new_query.append(word.split())
		else:
			new_query.append(word)
	print(new_query)
	query = max(new_query, key=len)
	print(query)
	
	params = {
      "action": "wbsearchentities",
      "language": "en",
      "format": "json",
      "search": query

    }
	uri = ""
	try:
		data = requests.get(url, params=params)
		uri = data.json()["search"][0]["concepturi"]
		print(uri)
	except:
		uri = "aucun resultat"
	return uri

# ==================== cea file ========================
def  openFilecsvCea(files_cea):
	# lister les fichiers dans le dataset
	dataset = os.listdir(path)
	# trier le dataset par ordre alphabetique
	dataset.sort(reverse=False)
	# creer l'entête des fichier cea
	header_cea = ["File", "Col", "Row", "URI"]
	# open output cea file to write inside 
	with open(files_cea, "w+") as csv_file:
		writer = csv.writer(csv_file, delimiter=",")
		writer.writerow(header_cea)
		# get filename from each file in dataset
		for filed in dataset:
			# read only csv file insie in dataset
			if filed.endswith(".csv"):
				
				# open current clean file in dataset with pandas dataframe
				_file = pd.read_csv(f"{path}/{filed}", header=None)
				# get total row and colums of each cleaned file csv
				total_rows = len(_file.axes[0])
				total_cols=len(_file.axes[1])

				# parcourit chaque cellule de chaque colonne en effectuant la recherche sur
				# wikidata
				list_uri = []
				cells_firs_line = [cell for cell in _file.loc[0]]
				print(cells_firs_line)
				
				for cols in _file.columns:
					for i, line in _file.iterrows():
						
						if isinstance(line[cols], str):					
							if len(line[cols]) >=2:
								# we built rejex that verify if our charter contains number
								rejex = re.findall("[0-9]", line[cols])
								if len(rejex) > len(line[cols])-len(rejex):
									list_uri.append("NIL")
								# make search with this cell on wikidata
								else:	
									a = openUrL(line[cols])
									# a = "bonjour"
									# verify if we have result of the search query
									if a == "aucun resultat":
										list_uri.append("NIL")
									else:
										list_uri.append(a)
							# rejex if len of word <=2
							else:
								list_uri.append("NIL")
						# verify if cell is empty by default in dataframe all empty cell called
						#  nan
						if type(line[cols]) == type(np.nan):
							list_uri.append("NIL")
				print(len(list_uri))
				# get name of cleaned file
				filename = filed.split("clean.")[0]
				print("fichier:", filename, "nbre de ligne: ", total_rows, " nombre de col: ", total_cols)
				filetotalrowcol = total_rows * total_cols
				row = 0
				col = 0
				uri_n =0
				# creer la structure d'un fichier cea
				while row < filetotalrowcol:
					# for cell in total_cols:

					if row < total_rows:
						if list_uri[uri_n] == "NIL":
							row += 1
							uri_n +=1
						else:
							writer.writerow([filename, col, row, list_uri[uri_n]])
							row += 1
							uri_n +=1
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
	data_cea =_test_cea.loc[0:]
	print(data_cea)


# ================cta file ================================
def openFilecsvCta(files_cta):
	# lister les fichiers dans le dataset
	dataset = os.listdir(path)
	# trier le dataset par ordre alphabetique
	dataset.sort(reverse=False)
	# creer l'entête des fichier cta
	header_cta = ["File", "Col", "URI"]

	# open cta file file to write inside
	with open(files_cta, "w+") as csv_file:
		writer = csv.writer(csv_file, delimiter=",")
		writer.writerow(header_cta)


		for filed in dataset:
			# read only csv file insie in dataset
			if filed.endswith(".csv"):
				
				# open current clean file in dataset with pandas dataframe
				_file = pd.read_csv(f"{path}/{filed}", header=None)
				# get cell header of each column
				cells_firs_line = [cell for cell in _file.loc[0]]
				print(cells_firs_line)
				# get total row and colums of each cleaned file csv
				total_cols=len(_file.axes[1])
				filename = filed.split("clean.")[0]
				print("fichier:", filename, " nombre de col: ", total_cols)

				# format cell of header
				# ici aussi je dois traiter les entetes
				liste_header_uri = []
				for cell in cells_firs_line:
					if (type(cell) == type(np.nan)):
						liste_header_uri.append("NIL")
					elif openUrL(cell) == "aucun resultat":
						liste_header_uri.append("NIL")
					else:
						uri = openUrL(cell)
						liste_header_uri.append(uri)
					print(cell)

				# creer la structure d'un fichier cta
				col = 0
				while col < total_cols:
					# for cell in total_cols:
					if liste_header_uri[col] == "NIL":
						col += 1
					else:
						writer.writerow([filename, col, liste_header_uri[col]])
						col += 1
				# end structure cta.csv

		csv_file.close()
	print("============ data cta =============")
	_test_cta = pd.read_csv(files_cta)
	data_cta =_test_cta.loc[0:]
	print(data_cta)


# ======================== cpa file ===================
def openFilecsvCpa(files_cpa):
	# lister les fichiers dans le dataset
	dataset = os.listdir(path)
	# trier le dataset par ordre alphabetique
	dataset.sort(reverse=False)
	# creer l'entête des fichier cta
	header_cpa = ["File", "coli", "colj", "URI"]

	# open cpa file file to write inside
	with open(files_cpa, "w+") as csv_file:
		writer = csv.writer(csv_file, delimiter=",")
		writer.writerow(header_cpa)

		for filed in dataset:
			# read only csv file insie in dataset
			if filed.endswith(".csv"):
				
				# open current clean file in dataset with pandas dataframe
				_file = pd.read_csv(f"{path}/{filed}", header=None)
				# get cell header
				cells_firs_line = [cell for cell in _file.loc[0]]
				"""
					format  cell header to entity expression
				"""
				cells_firs_line_format = []
				for cell in cells_firs_line:
					if (type(cell) == type(np.nan)):
						cells_firs_line_format.append("aucresultat")
					else:
						cells_firs_line_format.append(cell)
				# end format cell header

				# get total colums of each cleaned file csv
				total_cols=len(_file.axes[1])
				filename = filed.split("clean.")[0]
				print("fichier:", filename, " nombre de col: ", total_cols)

				# list couples header
				result =[]
				for i in range(len(cells_firs_line_format)):
					for j in range(i+1, len(cells_firs_line_format)):
						result.append((cells_firs_line_format[i], cells_firs_line_format[j]))


				# creer les couples de relations entre les colone comme suit coli colj
				liste = [i for i in range(total_cols)]
				couples = []
				for coli in range(total_cols):
					for colj in range(coli+1, total_cols):
						couples.append((liste[coli], liste[colj]))
				
				# get couple relation uri 
				list_uri = []
				for entity in result:
					uri = get_uri_cpa(entity[0], entity[1])
					list_uri.append(uri)
				print(list_uri)

				# write in cpa file
				i = 0
				for couple in couples:
					if list_uri[i] == "aucun resultat":
						i += 1
					else:
						writer.writerow([filename, couple[0], couple[1], list_uri[i]])
						i += 1
				# end structure cpa.csv

		

		csv_file.close()
	print("============ data cpa =============")
	_test_cpa = pd.read_csv(files_cpa)
	data_cpa =_test_cpa.loc[0:]
	print(data_cpa)

# for word in query.split():
# 		if '-' in word:
# 			for w in word.split("-"):
# 				new_query.append(w)
# 		elif '' in word:
# 			new_query.append(word)
# 		else:
# 			new_query.append(word)


# execute function
openFilecsvCea("../wikidata/cea.csv")
openFilecsvCta("../wikidata/cta.csv")
openFilecsvCpa("../wikidata/cpa.csv")

# getUricpa("food", "feed")

# openUrL("name of document")
