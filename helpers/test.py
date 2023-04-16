import requests

# Remplacez "votre_query" par la chaîne de recherche que vous souhaitez effectuer sur Wikidata
query = "drink water"

# Encodez la chaîne de recherche pour être utilisée dans l'URL
encoded_query = requests.utils.quote(query)

# Construisez l'URL de l'API en utilisant les paramètres nécessaires
url = "https://www.wikidata.org/w/api.php?action=wbsearchentities&search={}&language=en&limit=10&continue=0&format=json&uselang=en&type=item".format(encoded_query)

# Effectuez la requête HTTP en utilisant la bibliothèque requests
response = requests.get(url)

# Obtenez les résultats de la réponse au format JSON
results = response.json()

# Faites quelque chose avec les résultats ici
print(results)