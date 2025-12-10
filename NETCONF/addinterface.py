#Practicing NETCONF RPCs using Cisco's IOS XE Always On Sandbox. Code examples taken from Cisco's free Devnet course "Exploring IOS XE YANG Data Models with NETCONF"
#Adding a loopback interface via NETCONF
from ncclient import manager

IETF_INTERFACE_TYPES = {
        "loopback": "ianaift:softwareLoopback",
        "ethernet": "ianaift:ethernetCsmacd"
    }

#8000v router
IOS_XE_1 = {
    "host":"10.10.20.48",
    "username":"developer",
    "password":"C1sco12345",
    "netconf_port":830,
    "restconf_port":443,
    "ssh_port":22
}
# Create an XML configuration template for ietf-interfaces
netconf_interface_template = """
    <config>
        <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface>
                <name>{name}</name>
                <description>{desc}</description>
                <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">
                    {type}
                </type>
                <enabled>{status}</enabled>
                <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip">
                    <address>
                        <ip>{ip_address}</ip>
                        <netmask>{mask}</netmask>
                    </addressű7cd`1450-p
                </ipv4>
            </interface>
        </interfaces>
    </config>"""

# Ask for the Interface Details to Add
new_loopback = {}
new_loopback["name"] = "Loopback" + input("What loopback number to add? ")
new_loopback["desc"] = input("What description to use? ")
new_loopback["type"] = IETF_INTERFACE_TYPES["loopback"]
new_loopback["status"] = "true"
new_loopback["ip_address"] = input("What IP address? ")
new_loopback["mask"] = input("What network mask? ")

# Create the NETCONF data payload for this interface
netconf_data = netconf_interface_template.format(
    name=new_loopback["name"],
    desc=new_loopback["desc"],
    type=new_loopback["type"],
    status=new_loopback["status"],
    ip_address=new_loopback["ip_address"],
    mask=new_loopback["mask"]
)

with manager.connect(
    host=IOS_XE_1["host"],
    port=IOS_XE_1["netconf_port"],
    username=IOS_XE_1["username"],
    password=IOS_XE_1["password"],
    hostkey_verify=False
    ) as m:

    #Execute config change, utilizing <edit-config>
    netconf_reply = m.edit_config(netconf_data, target='running')