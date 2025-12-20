#Creating a new network in Cisco's Meraki Enterprise Sandbox. The network created here won't have any network devices since we don't have any serial numbers to claim.
import requests
import json

API_KEY = 'b7dbb52843a90d68af734079a0e4d7334998b3cf'
base = "https://api.meraki.com/api/v1"
headers = {"Content-Type": "application/json",
           "Accept": "application/json",
           "X-Cisco-Meraki-API-Key": API_KEY}

get_org_response = requests.get(url=base+'/organizations',headers=headers,data=None)

#Convert encoded API response to a Python object. Without it the string has b' in front
orgs = json.loads(get_org_response.text.encode('utf8'))
#Grab ORG_ID
ORG_ID = orgs[0]['id']

#Get user inputs for network parameters
name = input("Enter name of network you want to create: ")
productTypes = input("Enter in the types of devices you want in this network separated by comma [appliance, switch, wireless, cellular gateway, sensor, camera]\n").split(',')

payload = {
    "name":name,
    "productTypes":productTypes,
    "timeZone":"America/New_York",
}

try:
    create_network_response = requests.post(url=base+f'/organizations/{ORG_ID}/networks',headers=headers,data=json.dumps(payload))
except requests.exceptions.Timeout as e:
    print("Failed due to Timeout")
except requests.exceptions.ConnectionError as e:
    print("Failed due to Connection Error")
else:
    if create_network_response.raise_for_status == 201:
        print(f"Network {name} has been created successfully")
    else:
        print("Something went wrong with creating the network. Status code:")
        print(create_network_response.status_code)