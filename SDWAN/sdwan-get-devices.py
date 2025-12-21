# Cisco SD-WAN Sandbox, lab environment only.

#import sdwanauth script to get JSESSIONID and XSRFTOKEN
from package import sdwanauth
import json
import requests

#Ideally these would be in an environment file instead of here in plain text
vs = "10.10.20.90"
vp = "443"
username = "admin"
password = "C1sco12345"
base = f"https://{vs}:{vp}/dataservice"

auth = sdwanauth.Authentication()

JSESSIONID = auth.get_sessionid(vs,vp,username,password)
XSRFTOKEN = auth.get_token(JSESSIONID,vs,vp)

HEADER = {"Content-Type": "application/json",
          "X-XSRF-TOKEN":XSRFTOKEN,
          "Cookie":JSESSIONID}

#Get list of devices
response = requests.get(url=base+"/device", headers=HEADER, verify=False)

devices = json.loads(response.text.encode('utf8'))['data']

for device in devices:
    print(device)

#Create a subset dictionary list that contains only the device name and system IP for easier viewing
device_id=[]
for device in devices:
    idx = devices.index(device)
    device_id.append({k: devices[idx][k] for k in ('host-name','deviceId')})

print(device_id)