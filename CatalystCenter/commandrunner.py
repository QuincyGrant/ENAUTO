#Command runner API lets you execute commands on Catalyst Center managed devices. Only read-only commands are currently supported, not configuration.
#Following Cisco docs found here https://developer.cisco.com/docs/dna-center/2-3-7-9/command-runner/#task-api

# Steps:
#1) Authenticate against the Catalyst Center API.
#2) Obtain the IDs of the devices that you want to send the commands to.
#3) Execute the commands against a list of devices and obtain the task ID.
#4) Use the task ID to query the Task API for a result, if successful obtain the file ID of the result
#5) Retrieve the file contents from the file API.
from dnacenterauth import dnacenterauth
from dnacenterinventory import get_inventory
import requests
import json
from pprint import pprint

token = dnacenterauth()
inventory = get_inventory(token)

base = "https://sandboxdnac.cisco.com/dna/intent/api/v1"
headers = {
    "Content-Type": "application/json",
    "X-Auth-Token": token
}
#Get device IDs from inventory
devices=[]
for device in inventory:
    devices.append(device['id'])

print(devices)
#Commands to send
payload = {"commands": ["show version",
                        "show ip int br"],
           "deviceUuids":devices,
           "timeout":0}

#Endpoint for commands
cmdrunner_path = '/network-device-poller/cli/read-request'

#Make call then retrieve the Task ID associated with the executed commands
response = requests.post(base+cmdrunner_path,headers=headers,data=json.dumps(payload),verify=False)
task_id = response.json()['response']['taskId']

#Endpoint to retrieve task ID for the commands that were sent
task_id_path=f'/task/{task_id}'

#Use Task ID in Task API to retrieve file ID
response = requests.get(base+task_id_path,headers=headers,verify=False)
progress = json.loads(response.json()['response']['progress'])
file_id = progress['fileId']

#Use File ID in File API to retrieve command output.
file_path = f'/file/{file_id}'
response = requests.get(base+file_path,headers=headers,verify=False)
file_json=response.json()

#Write the show output to a text file
with open('show_ver_interface.txt','w') as f:
    pprint(file_json[0]['commandResponses'],stream=f)