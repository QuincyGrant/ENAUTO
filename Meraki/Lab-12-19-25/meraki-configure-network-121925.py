#The sandbox environment seems to be bugged where there are no pre-licensed devices like there usually are so this will just be going through the motions
import requests
import json

from requests import HTTPError

API_KEY = 'b7dbb52843a90d68af734079a0e4d7334998b3cf'
base = "https://api.meraki.com/api/v1"
headers = {"Content-Type": "application/json",
           "Accept": "application/json",
           "X-Cisco-Meraki-API-Key": API_KEY}

get_org_response = requests.get(url=base+'/organizations',headers=headers,data=None)

#Convert encoded API response to a Python object. Without it the string has b' in front
j = json.loads(get_org_response.text.encode('utf8'))
#Grab ORG_ID
ORG_ID = j[0]['id']

#Get list of networks and then convert to Python object
get_networks_response = requests.get(url=base+f'/organizations/{ORG_ID}/networks',headers=headers,data=None)
networks = json.loads(get_networks_response.text.encode('utf8'))

#Present list of networks to user and get input to determine which to configure and grab its network ID
print("List of networks:")
network_names = []
for network in networks:
    idx = networks.index(network)
    network_names.append(networks[idx]['name'])
    print(f"{idx+1}. " + networks[idx]['name'])

i = input("Which network do you want to configure? (Enter in number):\n")

#Get ID of network user chose
network_id = networks[int(i)-1]['id']

#If I had real devices to claim
claim_payload = {
    "serial":["serial1, serial2, serial3"],
}

#Using raise_for_status method to determine if we get an error in return
try:
    requests.post(url=base+f'/networks/{network_id}/claim',headers=headers,data=json.dumps(claim_payload)).raise_for_status()
except HTTPError :
    print("Failed to claim devices")
else:
    print("Successfully claimed devices")

#Print network devices (not really since there are no devices today)
devices_response = requests.get(url=base+f'/networks/{network_id}/devices',headers=headers,data=None)
print(devices_response.text.encode('utf8'))
