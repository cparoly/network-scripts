from netmiko import ConnectHandler
from netmiko import NetMikoTimeoutException
from netmiko import NetMikoAuthenticationException

device = input('What is the IP of the device we are looking at? ')
cisco = {
        'device_type': 'cisco_ios',
        'host': device,
        'username': 'cparoly',
        'password': 'blackbird.1'
    }

net_connect = ConnectHandler(**cisco)

mac_address = net_connect.send_command('show mac address-table', use_genie=True )
ip_arp = net_connect.send_command('show ip arp', use_genie=True)

print(mac_address)
print(ip_arp)
