#Get Authorization token for CatalystCenter API calls. CatalystCenter hosted in Cisco's Always On Sandbox
import requests
import json
import base64

def dnacenterauth():
    un = "devnetuser"
    pw = "Cisco123!"

    #Need base64 encoded string of '{username}:{password}' to supply in header to obtain the token
    credentials = f"{un}:{pw}"
    b = credentials.encode('ascii')
    encoded = base64.b64encode(b)
    encoded_string = encoded.decode('ascii')

    headers = {
        "content-type": "application/json",
        "Authorization":"Basic " + encoded_string #Don't forget the space after 'Basic'. This indicates that Basic Auth is used
    }

    base = "https://sandboxdnac.cisco.com/dna/intent/api"
    tokenurl = "https://sandboxdnac.cisco.com/dna/system/api/v1/auth/token"

    response = requests.request("POST",url=tokenurl,headers=headers,verify=False)
    token = json.loads(response.text)['Token']

    return token