#Testing various Meraki API calls in a lab environment hosted in Cisco's Always On Sandbox 

import meraki
import requests
import sys
import json
import csv
from pprint import pprint

API_KEY = os.environ.get("API_KEY")
ORG_ID = "669910444571366285"
baseurl = "https://api.meraki.com/api/v1"
headers = {"Content-Type": "application/json",
           "Accept": "application/json",
           "X-Cisco-Meraki-API-Key": API_KEY,}
#Get networks using Meraki API library
dashboard = meraki.DashboardAPI(API_KEY)
networks = dashboard.organizations.getOrganizationNetworks(ORG_ID)
NETWORK_IDs = []
for network in networks:
    NETWORK_IDs.append(network['id'])

#Get device list for all of the Org
serial = []
devices = dashboard.organizations.getOrganizationDevices(ORG_ID,total_pages= 'all')

#
switches =[]
for device in devices:
    serial.append(device['serial'])
    if device['productType'] == 'switch':
        switches.append(device['serial'])

pprint(devices)

switchports = []
for switch in switches:
    switchports = dashboard.switch.getDeviceSwitchPorts(switch)

pprint("Ports before: \n"
       "=================")
pprint(switchports)

#Update switchports
for port in switchports:
    if port['vlan'] == 5:
        try:
            dashboard.switch.updateDeviceSwitchPort(switches[0],port['portId'],type = 'access')
        except:
            print (f"Port {port['portId']} on switch {serial[0]} update failed")
        else:
            print (f"Port {port['portId']} on switch {serial[0]} updated successfully")

pprint("Ports after: \n"
       "===================")
pprint(switchports)

#Create network named 'Test' with a switch and appliance using Meraki API
#dashboard.organizations.createOrganizationNetwork(ORG_ID,'Test',['switch','appliance'])

#Get org details using requests library instead of Meraki API library
'''
payload = None

response = requests.request("GET", baseurl + "/organizations", headers=headers, data=payload)

print(response.text.encode('utf8'))
'''

#Create network using requests library
'''
url = baseurl + f"/organizations/{ORG_ID}/networks"
payload = {"name":"Test Network3",
           "productTypes": ["appliance", "switch"],
           "tags":["",""],
           "timeZone":"America/New_York",
           "copyFromNetworkID": NETWORK_ID
           }
response = requests.request("POST", url, headers=headers,data = json.dumps(payload))
print(url)
print("Creating network...")
print(response.text.encode('utf8'))
'''
#DELETE NETWORKS EXCEPT FOR L_669910444571379799
'''
for i in NETWORK_IDs:
    if i == 'L_669910444571379799':
        continue
    url = baseurl + f"/networks/{i}"
    response = requests.request("DELETE", url, headers=headers,data = None)
    print("Deleted network " + i)
'''





