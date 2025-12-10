#Use Meraki API library to create a network in always on sandbox
import meraki

API_KEY = '98d5870f065366e8cb0530bc710971976d17bde7'
ORG_ID ='549236'

base_url = 'https://api.meraki.com/api/v1'

dashboard = meraki.DashboardAPI(API_KEY)

networks = dashboard.organizations.getOrganizationNetworks(ORG_ID)

new = {"name": "Lab",
       "productTypes": ["appliance","switch","wireless"],
       "timeZone": "America/New_York"}

dashboard.organizations.createOrganizationNetwork(ORG_ID,**new)
