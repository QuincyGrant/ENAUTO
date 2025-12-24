# The Site API enables users to create a logical hierarchy of areas, buildings, and floors,
# assign devices to it, list devices within the hierarchy, and retrieve site health information.

# Documentation: https://developer.cisco.com/docs/dna-center/2-3-7-9/sites/#site-api
from dnacenterauth import dnacenterauth
from pprint import pprint
import requests
import json

token = dnacenterauth()
headers = {
    'Content-Type': 'application/json',
    'X-Auth-Token': token
}
base = 'https://sandboxdnac.cisco.com/dna/intent/api/v1'

#Site creation API
site_path = '/site'
area_payload = {
    "type":"area",
    "site":{
        "area":{"name":"Testing",
                "parentName":"Global"}

    }
}

# Forces synchronous response, since Site API is asynchronous by default
headers['__runsync'] = 'true'
headers['__runsynctimeout'] = '30'

#Create Area and grab site ID which will be used to assign devices to
response = requests.post(base+site_path,headers=headers,json=area_payload,verify=False)

area_id = response.json()['siteID']

site_building = {
    "type":"building",
    "site": {
        "building":{
            "name": "Test Building",
            "parentName": "Global/Testing",
            "latitude":"45.234324",
            "longitude":"-102.343332"
        }
    }
}

response = requests.post(base+site_path,headers=headers,json=site_building,verify=False)