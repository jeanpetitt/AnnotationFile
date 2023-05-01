from SPARQLWrapper import SPARQLWrapper, JSON
import requests, json
import random


def openUrl(query):
    url = "https://www.wikidata.org/w/api.php"
    new_query = []
    for word in query.split():
        if '-' in word:
            new_query.append(word.split("-"))
        elif '' in word:
            new_query.append(word.split())
        else:
            new_query.append(word)

    params = {
      "action": "wbsearchentities",
      "language": "en",
      "format": "json",
      "search": query

    }

  # if query.split("-"):
	# 	query = query.split("-")
	# 	longest_word = max(query, key=len)
	# 	query = longest_word
	# 	print(query)

    uri = ""
    try:
      data = requests.get(url, params=params)
      uri = data.json()["search"][0]["id"]
      print(uri)
    except:
      uri = "aucun resultat"
    return uri

def get_uri_cpa(query1, query2):
    quer1 = openUrl(query1)
    quer2 = openUrl(query2)
    # Établissement de la connexion avec la base de données Wikidata
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

    property_uri = ""
    # Requête SPARQL pour récupérer l'URI de la propriété entre l'entité q1ument et l'entité de référence
    try:
       
      if (query1 != "aucun resultat" and query2 !="aucun resultat"):
        query = """
        SELECT DISTINCT ?property WHERE {{
          wd:{q1} ?property ?obj1 .
          wd:{q2} ?property ?obj2 .
          FILTER(STRSTARTS(str(?property),str(wdt:)))
        }}
        """.format(q1=quer1, q2=quer2)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        # Extraction de l'URI de la propriété
        result = random.choice(results["results"]["bindings"])
        property_uri = result["property"]["value"]
        p_uri = property_uri.split("/")[-1]
        property_uri = "http://wikidata.org/property/"+p_uri

      
        # verifier si deux entités on le meme id exemple feed et food
        if quer1 == quer2:
          property_uri = "http://wikidata.org/property/P1889"

    except:
      property_uri = "aucun resultat"
      print(property_uri)
    # Affichage de l'URI de la propriété
    # print("L'URI de la propriété entre les entités {q1} et {q2} est {prop}".format(    
    return property_uri

# ==============Foodon====================
def openUrL_f(query):
  ontology = "foodon"
  url = f"https://www.ebi.ac.uk/ols/api/search?q={query}&ontology={ontology}"
  try:
    response = requests.get(url)
    if response.status_code == 200:
      resultat = response.json()["response"]["docs"]
      print(resultat)
    else:
      print(f"Error {response.status_code}: {response.text}")
  except:
    resultat = "aucun resultat"
  return resultat

def get_uri_cpa_foodon(query1, query2):
  # Effectuer une recherche
  response1 = requests.get('https://www.ebi.ac.uk/ols/api/search?q={query1}&ontology=foodon')
  response2 = requests.get('https://www.ebi.ac.uk/ols/api/search?q={query2}&ontology=foodon') 
  # Analyser les données
  data1 = response1.json()["response"]
  data2 = response2.json()["response"]
  # Parcourir les résultats data1
  query1_id = ""
  query2_id=""
  for result in data1['response']['docs']:
    if result['label'] == 'Food':
        query1_id = result['obo_id']
        break
  # Parcourir les résultats data2
  for result in data2['response']['docs']:
    if result['label'] == 'Feed':
        query2_id = result['obo_id']
        break
    
  # Vérifier la relation
  relationships = requests.get(f'https://www.ebi.ac.uk/ols/api/ontologies/foodon/individuals/{query1_id}/hierarchicalParents')
  data = relationships.json()["response"]
  if any(parent['obo_id'] == query2_id for parent in data['response']['docs']):
    print(f'{query1} is a parent of {query2}')
  else:
    print(f'{query1} is not a parent of {query2}')
      
  


  pass

# get_uri_cpa("Document", "Reference")


# get_uri_cpa_foodon("food", "feed")
# openUrL_f("food")