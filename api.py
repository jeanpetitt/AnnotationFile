import requests
from dotenv import load_dotenv
import os
import re
import string

# Remplacez ces valeurs par celles de votre projet
load_dotenv()


def openURL(query):
    # use memory to translate data in english
    mymemory_url = "https://api.mymemory.translated.net/get"
    # params = {
    #     "q": query,
    #     "langpair": "de|en",
    #     "key": "7e97dfaf4f1758296020",
    # }
    # response = requests.get(mymemory_url, params=params)
    # translated_query = response.json()["responseData"]["translatedText"]

    # query translated search on google
    query = query + " - wikidata"
    print(query)
    api_key = os.environ["API_KEY"]
    search_engine_id = os.environ["SEARCH_ENGINE_ID"]

    url = "https://www.googleapis.com/customsearch/v1"

    # Définir les paramètres de recherche
    params = {
        "q": query,
        "key": api_key,
        "cx": search_engine_id,
    }

    # Effectuer la requête de recherche
    response = requests.get(url, params=params)
    results = response.json()

    # Afficher les résultats

    uri = ''
    i = 0
    stop = True
    if 'items' in results:
        for item in results['items']:
            for data in item['link'].split('/'):
                if data.endswith('wikidata.org') or data.startswith('d:'):
                    print("YES")
                    if data.startswith('d:'):
                        # retrieve only the wikidata id
                        data = data.split(':')[-1]
                        uri = f"http://www.wikidata.org/entity/{data}"
                        print("uri:", uri)
                    elif data.startswith('www.wikidata'):
                        # retrieve only the wikidata id
                        data = item['link'].split('/')[-1]
                        uri = f"http://www.wikidata.org/entity/{data}"
                        print("uri:", uri)
                    stop = False
                    break
                else:
                    uri = "No result"
                    i += 1
            if not stop:
                break

    return uri


def openUrl(query):
    url = "https://www.wikidata.org/w/api.php"
    params = {
        "action": "wbsearchentities",
        "language": "en",
        "format": "json",
        "search": query

    }
    uri = ""

    # check if query is a digit
    if query.isdigit():
        try:
            response = requests.get(url, params=params)
            results = response.json()["search"]
            for item in results:
                if item['description'] == "natural number" or item['description'] == "number":
                    uri = item['concepturi']
                    print(f"True Uri: {uri}")
                    break
                else:
                    uri = "No result"
                    print(
                        f"{query} be refert to natural number and not a", item['description'])
        except ValueError as e:
            print(e.ConnectionError())

    # check if query is not a digit but a decimal number
    elif bool(re.match(r'\d+\.\d+', query)):
        uri = "No result"
        print(
            f"{query} is a decimal number, it is not present in wikidata knowledge graph")
    elif query in string.punctuation:
        uri = "No result"
        print(
            f"{uri} because {query} is special character")
    else:
        try:
            response = requests.get(url, params=params)
            if response.json()["search"] != []:
                uri = response.json()["search"][0]['concepturi']
                print("String", uri)
            else:
                uri = "No result"
                print(uri)
                """ 
                    if the query search on wikdata have no data, then process using google
                    API
                """
                # query = query + " - wikidata"
                # api_key = os.environ["API_KEY"]
                # search_engine_id = os.environ["SEARCH_ENGINE_ID"]
                # url = "https://www.googleapis.com/customsearch/v1"
                # # Définir les paramètres de recherche
                # params = {
                #     "q": query,
                #     "key": api_key,
                #     "cx": search_engine_id,
                # }
                # # Effectuer la requête de recherche
                # response = requests.get(url, params=params)
                # results = response.json()
                # print(results)
                # i = 0
                # stop = True
                # if 'items' in results:
                #     for item in results['items']:
                #         for data in item['link'].split('/'):
                #             if data.endswith('wikidata.org') or data.startswith('d:'):
                #                 print("YES")
                #                 if data.startswith('d:'):
                #                     # retrieve only the wikidata id
                #                     data = data.split(':')[-1]
                #                     uri = f"http://www.wikidata.org/entity/{data}"
                #                     print("uri:", uri)
                #                 elif data.startswith('www.wikidata'):
                #                     # retrieve only the wikidata id
                #                     data = item['link'].split('/')[-1]
                #                     uri = f"http://www.wikidata.org/entity/{data}"
                #                     print("uri:", uri)
                #                 stop = False
                #                 break
                #             else:
                #                 uri = "No result"
                #                 i += 1
                #         if not stop:
                #             break
                # else:
                #     uri = "No result"
                #     print(uri)
        except ValueError as e:
            print("Internet connection error")

    return uri


# openUrl("-")
