import csv
import re
from googletrans import Translator
import requests

# Créer un objet traducteur
translator = Translator()

# Définir une expression régulière pour correspondre aux chaînes qui ne contiennent que des nombres et des décimaux
number_pattern = re.compile(r'^-?\d+(\.\d+)?$')

# Ouvrir le fichier CSV en mode lecture
with open('8468806_0_4382447409703007384.csv', 'r') as f:
    # Lire le fichier CSV
    reader = csv.reader(f)
    header = next(reader)  # Extraire l'en-tête du fichier CSV
    # Traduire chaque ligne du fichier CSV
    mymemory_url = "https://api.mymemory.translated.net/get"

    with open('output.csv', 'w', newline='') as g:
        writer = csv.writer(g)
        writer.writerow(header)  # Écrire l'en-tête du fichier CSV
        for row in reader:
            translated_row = []
            for cell in row:
                if cell and not number_pattern.match(cell):
                    # Si la chaîne n'est pas vide et ne correspond pas au motif, la traduire
                    params = {
                        "q": cell,
                        "langpair": "de|en",
                        "key": "7e97dfaf4f1758296020",
                    }
                    response = requests.get(mymemory_url, params=params)
                    translated_cell = response.json(
                    )["responseData"]["translatedText"]
                else:
                    # Si la chaîne est vide ou correspond au motif, laisser tel quel
                    translated_cell = cell
                translated_row.append(translated_cell)
            writer.writerow(translated_row)  # Écrire la ligne traduite
