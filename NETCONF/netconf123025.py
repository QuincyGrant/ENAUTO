from ncclient import manager
import xmltodict
import xml.etree.ElementTree as ET
from pprint import pprint
import xml.dom.minidom

host = {
    "host":"10.10.20.48",
    "username":"developer",
    "password":"C1sco12345",
    "netconf_port":830,
    "restconf_port":443,
    "ssh_port":22
}

#Filter for ACLs
filter = """
        <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
            <acl xmlns="http://openconfig.net/yang/acl">
			<acl-sets>
				<acl-set>
				    <acl-entries>
						<acl-entry></acl-entry>
					</acl-entries>
				</acl-set>
			</acl-sets>
			</acl>
		</filter>"""

with manager.connect(
    host = host['host'],
    username = host['username'],
    password = host['password'],
    port = host['netconf_port'],
    hostkey_verify = False
    ) as m:

    #Get ACL config
    config = m.get_config(source='running')
    acl = m.get_config(source='running',filter=filter)
    with open('acls.txt','w') as f:
        print(xml.dom.minidom.parseString(acl.xml).toprettyxml(),file=f)

    #Convert to dictionary and grab the ACL data only
    acl_dict = xmltodict.parse(acl.xml)['rpc-reply']['data']

    #Practice parsing the XML using xml.etree.ElementTree library
    root = ET.fromstring(acl.xml)

    #Grabbing ACL name?
    print(root[0][0][0][0][1].text)