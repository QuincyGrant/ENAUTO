from package import sdwanauth
import requests
import json
from pprint import pprint

vs = "10.10.20.90"
vp = "443"
username = "admin"
password = "C1sco12345"
base = f"https://{vs}:{vp}/dataservice"

auth = sdwanauth.Authentication()

JSESSIONID = auth.get_sessionid(vs,vp,username,password)
XSRFTOKEN = auth.get_token(JSESSIONID,vs,vp)

header = {"Content-Type": "application/json",
          "X-XSRF-TOKEN":XSRFTOKEN,
          "Cookie":JSESSIONID}

#First get device IDs for our devices
response = requests.get(url=base+"/device", headers=header, verify=False)
devices = json.loads(response.text.encode('utf8'))['data']

#Create a subset dictionary list that contains only the device name and system IP for easier viewing.
device_id=[]
for device in devices:
    idx = devices.index(device)
    device_id.append({k: devices[idx][k] for k in ('host-name','deviceId')})

#Get control connections for each device (not super easy to read as is). Each device forms a mesh with the other devices in the fabric. So we get a dictionary (individual connection) nested within a list (all connections for a specific device) within another list (contains all connections for each device)
controldata =[]
for d in device_id:
    response = requests.get(url=base + "/device/control/synced/connections?deviceId={0}".format(d['deviceId']),headers=header, verify=False)
    controldata.append(json.loads(response.text.encode('utf8'))['data'])

#Grab system IP, control connection peer IPs and control status for easier viewing
control_status = [
    [
        {
            "vmanage-system-ip": item.get("vmanage-system-ip"),
            "system-ip": item.get("system-ip"),
            "state": item.get("state")
        }
        for item in group
    ]
    for group in controldata
    ]

pprint(control_status)
