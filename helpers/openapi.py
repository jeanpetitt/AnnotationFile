from SPARQLWrapper import SPARQLWrapper, JSON
import requests
import random


def openUrl(query):
    url = "https://www.wikidata.org/w/api.php"
    params = {
      "action": "wbsearchentities",
      "language": "en",
      "format": "json",
      "search": query

    }
    uri = ""
    try:
      data = requests.get(url, params=params)
      uri = data.json()["search"][0]["id"]
    except:
      uri = "aucun resultat"
    return uri

def get_uri_cpa(query1, query2):
    quer1 = openUrl(query1)
    quer2 = openUrl(query2)
    # Établissement de la connexion avec la base de données Wikidata
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

    # Requête SPARQL pour récupérer l'URI de la propriété entre l'entité q1ument et l'entité de référence
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

    # Affichage de l'URI de la propriété
    # print("L'URI de la propriété entre les entités {q1} et {q2} est {prop}".format(
    #     q1=query1, q2=query2, prop=property_uri))
    
    return property_uri

# get_uri_cpa("Document", "Reference")