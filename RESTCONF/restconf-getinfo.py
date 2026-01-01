import requests,json
from pprint import pprint

base = 'https://10.10.20.48/restconf/data'
headers = {'Content-Type': 'application/yang-data+json',
           'Accept': 'application/yang-data+json'}
auth = ("developer","C1sco12345")

cap_url = '/data/netconf-state/capabilities'
int_url = '/ietf-interfaces:interfaces'

#Get interfaces
response = requests.get(url=base+int_url,headers=headers,auth=auth,verify=False)
print("Get interfaces status: \n", response.status_code)
#Data for new loopback interface to be created
payload = {
    "ietf-interfaces:"
    "interface":{
        "name": "Loopback500",
        "description":"Configured via RESTCONF",
        "type":"iana-if-type:softwareLoopback",
        "enabled":True,
        "ietf-ip:ipv4":{
            "address":{
            "ip": "192.168.53.6",
            "netmask":"255.255.255.255"}
        }
        }
}

#Create interface
response = requests.post(url=base+int_url,json=payload,headers=headers,auth=auth,verify=False)
print("Create interface status: \n",response.status_code)

#Get interfaces again to verify change
response = requests.get(url=base+int_url,headers=headers,auth=auth,verify=False)
pprint(response.json())