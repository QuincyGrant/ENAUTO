#Create Meraki Network using requests lib
import requests,json

base = "https://api.meraki.com/api/v1"
API_KEY = "7ab189d8ac6147cf23f16d183007f3efe5ebb221"
ORG_ID =  "669910444571366502"

headers = {"Content-Type": "application/json",
           "Accept": "application/json",
           "X-Cisco-Meraki-API-Key": API_KEY}

url = base +  f"/organizations/{ORG_ID}/networks"

#Create network named 'Lab' with firewall, switch and wireless
payload = {
        "name": "Lab",
        "productTypes": ["appliance","switch","wireless"],
        "timeZone": "America/New_York"}

response = requests.post(url=url,headers=headers,data = json.dumps(payload))

print(response)