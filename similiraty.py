import requests
import sys
from editdistance import eval


if __name__ == "__main__":
    resources = sys.argv[1:]
    print("ressoures wikidata", resources)
    output = []
    for resource in resources:
        params = {
            "action": "wbsearchentities",
            "language": "en",
            "format": "json",
            "search": resource

        }
        response = requests.get(
            f'https://www.wikidata.org/w/api.php', params=params)
        result = response.json()['search']
        best_result = sorted(result, key=lambda r: eval(resource, r['label']))[
            0] if len(result) > 0 else []

        # print(best_result)

        if best_result:
            uri = f"http://wikidata.org/entity/{best_result['id']}"
            output.append(
                f" - Input : {resource} \n\t-> id = {best_result['id']}, label = {best_result['label']}, link ={uri} ")
        else:
            output.append(f" - Input : {resource} \n\t-> ----Not Found----")

    for line in output:
        print(f"{line}")
