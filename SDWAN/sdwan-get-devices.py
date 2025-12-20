#import sdwanauth script to get JSESSIONID and XSRFTOKEN
from package import sdwanauth
import json
import requests

vs = "10.10.20.90"
vp = "443"
username = "admin"
password = "C1sco12345"

auth = sdwanauth.Authentication()

JSESSIONID = auth.get_sessionid(vs,vp,username,password)
XSRFTOKEN = auth.get_token(JSESSIONID,vs,vp)

#We now include the token and jsession ID in the header of our API calls
HEADER = {"Content-Type": "application/json",
          "X-XSRF-TOKEN":XSRFTOKEN,
          "Cookie":JSESSIONID}

#Get list of devices
response = requests.get(url=f"https://{vs}:{vp}/dataservice/device", headers=HEADER, verify=False)

devices = json.loads(response.text.encode('utf8'))['data']

for device in devices:
    print(device)