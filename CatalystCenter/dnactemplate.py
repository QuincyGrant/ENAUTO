#Creating a template in Catalyst Center using Template API
# https://developer.cisco.com/docs/dna-center/2-3-7-9/device-provisioning/#configuration-template-api

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

# First need to choose which project to put the template under.  Get list of projects first to view. We are going to use 'Onboarding Configuration'
TEMPLATE_URL = '/template-programmer/project'

response = requests.get(base+TEMPLATE_URL, headers=headers,verify=False)

projects = response.json()

#Grab the project ID of 'Onboarding Configuration'
for project in projects:
    if project['name'] == 'Onboarding Configuration':
        projectID = project['id']

#Template parameters - This template creates VLANs 100 and 200
template = {
    "name":"ENAUTO Lab",
    "description": "Template created for CCNP Exam",
    "tags":[],
    "deviceTypes": [
        {
        "productFamily": "Switches",
        "productSeries": "Cisco 9000 Series Catalyst Switches"
        }],
    "softwareType": "IOS-XE",
    "softwareVariant": "XE",
    "templateContent": "vlan $HRVLAN\nname HR\n!\nvlan $ACCTVLAN\nname Accounting\n!\n",
    "rollbackTemplateContent": "",
    "templateParams": [
        {
            "parameterName": "HRVLAN", #Set a variable 'HRVLAN' which will be assigned during template deployment
            "dataType": "STRING",
            "defaultValue": None,
            "description": None,
            "required": True,
            "notParam": False,
            "paramArray": False,
            "displayName": None,
            "instructionText": None,
            "group": None,
            "order": 1,
            "selection": {
                "selectionType": None,
                "selectionValues": {},
                "defaultSelectedValues": []
            },
            "range": [],
            "key": None,
            "provider": None,
            "binding": ""
        },
        {
            "parameterName": "ACCTVLAN",
            "dataType": "STRING",
            "defaultValue": None,
            "description": None,
            "required": True,
            "notParam": False,
            "paramArray": False,
            "displayName": None,
            "instructionText": None,
            "group": None,
            "order": 2,
            "selection": {
                "selectionType": None,
                "selectionValues": {},
                "defaultSelectedValues": []
            },
            "range": [],
            "key": None,
            "provider": None,
            "binding": ""
        }
    ],
    "rollbackTemplateParams": [],
    "composite": False,
    "containingTemplates": []
    }

#Create template then grab task ID. Use task ID and task API to grab response for the template creation call then grab template ID from that
TEMPLATE_URL = f'/template-programmer/project/{projectID}/template'
response = requests.post(base+TEMPLATE_URL, headers=headers,verify=False,json=template)
pprint(response.json())
task_id = response.json()['response']['taskId']

TASK_URL = f'/task/{task_id}'

response = requests.get(base+TASK_URL, headers=headers,verify=False)

#Grab template ID from the task API
template_id = response.json()['response']['data']

#Use template ID to create an initial version for the template
template_version = {
    "comments":"VLAN template initial version",
    "templateId":template_id
}
TEMPLATE_VERSION_URL ='/template-programmer/template/version'
response = requests.post(base+TEMPLATE_VERSION_URL, headers=headers,json=template_version,verify=False)
print(response)

#Deploy template to a device. Chose a hostname from the inventory list
device_name = 'sw1'
TEMPLATE_DEPLOY_URL='/template-programmer/template/deploy'

#Assign the variables 'HRVLAN' and 'ACCTVLAN' that were created during template creation
deployment_info = {
    "forcePushTemplate": False,
    "isComposite": False,
    "targetInfo": [
        {
            "hostName": device_name,
            "params": {
                "HRVLAN": "500",
                "ACCTVLAN": "100"
            },
            "type": "MANAGED_DEVICE_IP"
        }
    ],
    "templateId": template_id}

response=requests.post(base+TEMPLATE_DEPLOY_URL, headers=headers,json=deployment_info,verify=False)
print(response)