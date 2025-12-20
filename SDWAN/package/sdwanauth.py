#Obtain JSESSIONID and XSRF token needed to authenticate future API calls. Cisco Catalyst SD-WAN hosted in Cisco's Always-On Sandbox
import requests
import json
from pprint import pprint

class Authentication:
    #staticmethod is a decorator that allows us to create a function without having to pass 'self' as it's not needed here
    @staticmethod
    def get_sessionid(vmanage_server,vmanage_port,un,pw):

        path = "/j_security_check"
        h = {"Content-Type": "application/x-www-form-urlencoded"}
        payload = {"j_username": un, "j_password": pw}

        #Make API Call. The 'verify' parameter is to ignore untrusted cert
        response = requests.post(url=f"https://{vmanage_server}:{vmanage_port}{path}", headers=h, data=payload, verify=False)
        ck = response.headers["Set-Cookie"].split(";")[0]

        return ck

    @staticmethod
    def get_token(cookie,vmanage_server,vmanage_port):
        path = "/dataservice/client/token"
        headers = {"Content-Type": "application/json",
                        "Cookie": cookie}

        response = requests.get(url=f"https://{vmanage_server}:{vmanage_port}{path}", headers=headers, verify=False)

        tk = response.text

        return tk