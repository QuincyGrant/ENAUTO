#Get networks
import requests,json
from pprint import pprint

base = "https://api.meraki.com/api/v1"
API_KEY = "7ab189d8ac6147cf23f16d183007f3efe5ebb221"
ORG_ID =  "669910444571366502"

headers = {"Content-Type": "application/json",
           "Accept": "application/json",
           "X-Cisco-Meraki-API-Key": API_KEY}
payload = None
url = base + f"/organizations/{ORG_ID}/networks"

response = requests.get(url,headers=headers,data=payload)

r = response.text.encode('utf8')
d = r.decode('utf-8')
s = d.replace("'",'"')

print(s)