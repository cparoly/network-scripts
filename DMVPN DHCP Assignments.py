from netmiko import ConnectHandler
from netmiko import NetMikoTimeoutException
from netmiko import NetMikoAuthenticationException
import re
import ipaddress
import getpass



dhcp_pool = 'show ip dhcp pool'
user = input("Username: ")
pwd = getpass.getpass()


while True:

	try:
		device = input("What is the IP of the device?: ")
		if "ns" or "nw" not in device:
			device = ipaddress.ip_address(device)
		else:
			continue

		break

	except ValueError:
		print("that is not a valid IP or hostname")
		continue

while True:
	try:
		IP = input("What is the IP address you are reserving?: ")
		IP = ipaddress.ip_address(IP)
		break
	except ValueError:
		print("that is not a valid IP")
		continue

while True:
	try:
		MAC = input("What is the MAC Address of the device you want to reserve? (format xxxx.xxxx.xxxx): ")
		if re.match("^[0-9a-f\.]{5}[0-9a-f\.]{5}[0-9a-f]{4}$", MAC.lower()) is not None:
			break
		else:
			print('That is not the correct MAC ADDRESS format.')
			continue

	except Exception('That is not the correct MAC ADDRESS format.'):
		continue

clear = 'clear ip dhcp binding ' + str(IP)

# Connect to device
print ("Connecting to " + str(device))
cisco = {
	'device_type': 'cisco_ios',
	'host': str(device),
	'username': user,
	'password': pwd
}
try:
	net_connect = ConnectHandler(**cisco)
except NetMikoAuthenticationException:
	print("Username/password incorrect")


print(net_connect.find_prompt())
# clear the current binding for the ip address from the dhcp pool
output = net_connect.send_command(clear)
output = net_connect.send_command("show ip dhcp pool")

# Determines name of the new DHCP pool
counter = output.count("RESERVED")
counter += 1
# Determines the default router copying from the wired network
default_router = net_connect.send_command('show run | i default-router')
default_router = default_router.splitlines()
default_router = default_router[0]

# Send the commands to create the new reserved pool
config_commands = ['ip dhcp pool RESERVED' + str(counter), 'host ' + str(IP), 'hardware-address ' + MAC,
                   'domain-name nslijhs.net', 'dns-server 10.140.185.225 10.170.78.225', default_router]
reserved = net_connect.send_config_set(config_commands)


print(reserved)
net_connect.disconnect()
input("Press Enter to exit")