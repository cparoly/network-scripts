from netmiko import ConnectHandler
from netmiko import NetMikoTimeoutException
from netmiko import NetMikoAuthenticationException
import re
import ipaddress
import getpass
from subprocess import Popen, PIPE

def router(x):
	p = Popen(['tracert', x], stdout=PIPE)
	routes = []

	while True:
		line = p.stdout.readline()
		line = line.decode('utf-8')
		test = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', line)

		if len(test) == 1:
			routes.append(test)
		elif 'complete' in line:
			routes = str(routes[-2])
			routes = routes.strip('[]')
			routes = routes.strip("''")

		elif 'Request timed out' in line:
			routes = str(routes[-1])
			routes = routes.strip('[]')
			routes = routes.strip("''")
		else:
			continue


	return routes






dhcp_pool = 'show ip dhcp pool'
user = input("Username: ")
pwd = getpass.getpass()




while True:
	try:
		reserve = input("What is the IP address you are reserving?: ")
		print(type(reserve))
		print(reserve)
		IP = ipaddress.ip_address(reserve)
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
device = router(reserve)
print(type(device))

clear = 'clear ip dhcp binding ' + str(IP)
# Connect to device
print ("Connecting to " + device)
cisco = {
	'device_type': 'cisco_ios',
	'host': device,
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