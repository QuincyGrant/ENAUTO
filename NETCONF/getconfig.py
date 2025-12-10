from ncclient import manager
import xmltodict
import xml.dom.minidom

host = {
    "host":"10.10.20.48",
    "username":"developer",
    "password":"C1sco12345",
    "netconf_port":830,
    "restconf_port":443,
    "ssh_port":22
}

with manager.connect(
        host=host['host'],
        username=host['username'],
        password=host['password'],
        port=host['netconf_port'],
        hostkey_verify=False
        ) as m:

        config = m.get_config('running')

        #Retrieve full running config from router in XML format and export it to a text file 'backup.txt'
        with open('backup.txt', 'w') as f:
            print(xml.dom.minidom.parseString(config.xml).toprettyxml(),file=f)


