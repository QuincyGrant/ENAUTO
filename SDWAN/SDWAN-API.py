#Obtain JSESSIONID and XSRF token needed to authenticate future API calls. Cisco Catalyst SD-WAN Manager hosted in Cisco's Always-On Sandbox
import requests

base = "https://10.10.20.90:443"
sess_token_path = "/j_security_check"
sess_headers = {"Content-Type": "application/x-www-form-urlencoded"}
sess_payload = {"j_username":"admin","j_password":"C1sco12345"}

response = requests.post(base+sess_token_path,headers=sess_headers,data=sess_payload,verify=False)

session_cookie = response.headers["Set-Cookie"].split(";")[0]

XSRF_path = "/dataservice/client/token"
XSRF_headers  = {"Content-Type": "application/json",
                 "Cookie": session_cookie}

XSRF_url = base+XSRF_path

response = requests.get(url=XSRF_url,headers=XSRF_headers,verify=False)
token = response.text

print(response.headers)
print(session_cookie)
print(token)


headers = {"Content-Type": "application/json","Cookie":session_cookie,"X-XSRF-TOKEN":token}