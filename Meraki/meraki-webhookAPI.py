import requests,json

base = "https://api.meraki.com/api/v1"
API_KEY = "7ab189d8ac6147cf23f16d183007f3efe5ebb221"
ORG_ID =  "669910444571366502"

headers = {"Content-Type": "application/json",
           "X-Cisco-Meraki-API-Key": API_KEY}

payload = {"url":"https://webhook.site/62c00a9a-1736-416a-8c5c-0ce4535a771b",
           "payloadTemplate":"Meraki"}

url = base + "/networks/L_669910444571380405/webhooks/webhookTests"

#Send Webhook test
response = requests.post(url=url,headers=headers,data=json.dumps(payload))

print(response.text)