import requests
import json
from pprint import pprint

def get_inventory(token):
    base = "https://sandboxdnac.cisco.com/dna/intent/api/v1"
    headers = {
        "Content-Type": "application/json",
        "X-Auth-Token": token
    }
    path = "/network-device"
    response = requests.get(base+path,headers=headers,verify=False)
    inventory = json.loads(response.text.encode('utf8'))['response']

    #Copy inventory to a file 'dnainventory.txt'
    with open('dnainventory.txt', 'w') as f:
        pprint(inventory,stream=f)

    return inventory