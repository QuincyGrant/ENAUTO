from netmiko import ConnectHandler

router = {
    'device_type': 'cisco_ios',
    'ip': '10.10.20.48',
    'username':'developer',
    'password':'C1sco12345'
}

with ConnectHandler(**router) as connect:
    interfaces = connect.send_command("show ip int br")

    #Print and save backup config in txt file
    backupconfig = connect.send_command("show running-config")
    with open('backup.txt','w') as f:
        print(backupconfig)

    acl_cmds = ['ip access-list extended NETMIKO',
                'permit ip any any',
                'exit',
                'interface loopback 200',
                'ip access-group NETMIKO in'
        ]
    acl = connect.send_config_set(acl_cmds)
    print(acl)