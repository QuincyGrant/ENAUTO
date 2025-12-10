import requests,json
from pprint import pprint
base = "https://api.meraki.com/api/v1"
API_KEY = "7ab189d8ac6147cf23f16d183007f3efe5ebb221"
ORG_ID =  "669910444571366502"
serial =  "QBSB-DU4U-25UB"

headers = {"Content-Type": "application/json",
           "Accept": "application/json",
           "X-Cisco-Meraki-API-Key": API_KEY}

url = base+f"/devices/{serial}/switch/ports/1"

payload={"type":"access",
         "vlan":40}
#Get network devices
response = requests.put(url,headers=headers,data=json.dumps(payload))

print(response.text)

