from netmiko import ConnectHandler
from netmiko import NetMikoTimeoutException
from netmiko import NetMikoAuthenticationException
from datetime import date
from datetime import datetime

devices = ["172.16.1.1", "172.16.1.2"]
commands = ['show ip int br', 'show environment']
date = date.today()
now = datetime.now()
today = date.strftime("%m/%d/%Y")
time = now.strftime("%I%p")

for device in devices:
	device = ''.join(device)
	print ("Connecting to " + device)
	cisco = {
		'device_type': 'cisco_ios',
		'host': device,
		'username': 'cisco',
		'password': 'cisco',
	}
	file = open(str(device.strip('\n'))+'.txt', 'a')
	try:
		net_connect = ConnectHandler(**cisco)
	except NetMikoAuthenticationException:
		print("Authentication Error")
		continue

	print(net_connect.find_prompt())

	for command in commands:
		for line in output.splitlines():
			if 'GigabitEthernet' in line and "0/0" in line:
				chunk = line.split()

				ip_address = chunk[1]
				interface = chunk[0]
				ip_address = ip_address.strip()
				print("The current ip address for " + interface + " is " + ip_address)
				file.write("\n4444 " + today  + " " + time + "pm - " + ip_address)
			elif 'All' in line:
				print(line)

	print (today + " " + time + "pm")
	file.close()
	net_connect.disconnect()
