#Practicing NETCONF RPCs using Cisco's IOS XE Always On Sandbox. Code examples taken from Cisco's free Devnet course "Exploring IOS XE YANG Data Models with NETCONF"
#This script will collect and list the interfaces of a router via NETCONF
from ncclient import manager
import xmltodict
import xml.dom.minidom

#8000v router
IOS_XE_1 = {
    "host":"10.10.20.48",
    "username":"developer",
    "password":"C1sco12345",
    "netconf_port":830,
    "restconf_port":443,
    "ssh_port":22
}

# Will be retrieving interface data
# A filter is needed to present only the ietf-interfaces YANG model. Without a filter we'll be returned output for ALL data models, meaning the full config

netconf_filter = """
<filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">    
  <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
    <interface></interface>
  </interfaces>
</filter>"""

# Open NETCONF session with the router
with manager.connect(
    host=IOS_XE_1["host"],
    port=IOS_XE_1["netconf_port"],
    username=IOS_XE_1["username"],
    password=IOS_XE_1["password"],
    hostkey_verify=False
    ) as m:

    # Router's NETCONF capabilities
    '''
    for capability in m.server_capabilities:
        print(capability)
    '''
    # Get running config but use filter to retrieve only the interfaces
    netconf_reply = m.get_config(source='running', filter=netconf_filter)

    #Print the above returned XML in a more readable format
    print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())

    #Convert XML to dictionary then grab the data in the RPC reply
    netconf_data = xmltodict.parse(netconf_reply.xml)["rpc-reply"]["data"]
    interfaces = netconf_data["interfaces"]["interface"]

    #Loop through and list all of the interfaces
    for interface in interfaces:
        print("Interface {} enabled status is {}".format(
            interface["name"],
            interface["enabled"]
        )
        )

print(netconf_reply)