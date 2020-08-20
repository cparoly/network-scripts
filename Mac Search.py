import socket
from netmiko import ConnectHandler
from netmiko import NetMikoTimeoutException
from netmiko import NetMikoAuthenticationException
import re
import ipaddress
import getpass


mac_regex = re.compile(r'[0-9a-f]{4}\.[0-9a-f]{4}\.[0-9a-f]{4}')
int_regex = re.compile(r'Fa{1}\S*\d/\S*\d{1,2}|Gi{1}\S*\d/\S*\d|Eth{1}\d/\S*\d{1,2}|Te{1}\S*\d/\S*\d')
int_po_regex = re.compile(r'Po{1}\d*')
int_regexes = [int_regex, int_po_regex]
description_regex = re.compile(r'Description: (.*)', re.MULTILINE)
access_vlan_regex = re.compile(r'switchport access vlan (\d*)', re.MULTILINE)

user = input("Tacacs username: ")
pwd = getpass.getpass("Tacacs password" )


try:
	distribution = input("What is the distribution switch that will have the ARP table for these? ")
	distribution = ipaddress.ip_address(distribution)
except ValueError:
	distribution = socket.gethostbyname(distribution)

while True:
	try:
		MAC = input("What is the MAC Address you are trying to find? (format xxxx.xxxx.xxxx): ")
		if re.match("^[0-9a-f\.]{5}[0-9a-f\.]{5}[0-9a-f]{4}$", MAC.lower()) is not None:
			break
		else:
			print('That is not the correct MAC ADDRESS format.')
			continue

	except Exception('That is not the correct MAC ADDRESS format.'):
		continue

cisco = {
	'device_type': 'cisco_ios',
	'host': distribution,
	'username': user,
	'password': pwd
}

try:
	dist_connect = ConnectHandler(**cisco)
except NetMikoAuthenticationException:
	print("Username/password incorrect")


def ConnectToDevice(host):
	print("Connecting to " + host)
	switch = {
		'device_type': 'cisco_ios',
		'host': host,
		'username': user,
		'password': pwd
	}
	try:
		net_connect = ConnectHandler(**switch)
	except NetMikoAuthenticationException:
		raise

	except NetMikoTimeoutException:
		raise

	return net_connect

def GetNextSwitch(mac):
	print('*' * 50)
	print ('Getting next switch')
	int = dist_connect.send_command("show mac address-table address " + mac, delay_factor=.1)
	po = re.search(int_po_regex, int)
	print(po)
	if po is None:
		po = re.search(int_regex, int)
		if po is None:
			return None
		else:
			po = po.group()
	else:
		po = po.group()

	print(po)
	interface = dist_connect.send_command("show run int " + str(po))
	print(interface)
	for description in interface.splitlines():
		if 'description' in description.lower():
			next_switch = description.split(' ')

	next_switch = [switch for switch in next_switch if 'ns-s' in switch]
	next_switch = str(next_switch)[1:-1]
	next_switch = next_switch.strip("'")



	return next_switch


def FindAttachedInterface(switch, mac):
	try:
		net_connect = ConnectToDevice(switch)
	except NetMikoAuthenticationException:
		return "Failed to Connect"
	except NetMikoTimeoutException:
		return "Failed to Connect"
	interface = net_connect.send_command("show mac address-table address " + mac)
	print(interface)
	int = re.search(int_regex, interface)

	if int is None:
		int = re.search(r'Po{1}\d*$', interface)
		if int is None:
			interface = 'unknown'
			duplex = 'unknown'
			speed = 'unknown'
			return interface, duplex, speed
		else:
			int = int.group()
	else:
		int = int.group()

	summary = net_connect.send_command("show int " + str(int))

	for media in summary.splitlines():
		if 'media' in media:
			duplex = media.split(',')[0].strip()
			speed = media.split(',')[1].strip()

	for errors in summary.splitlines():
		if 'CRC' in errors:
			error = errors.split(',')
			CRC = error[1]
			input_error = error[0]
			CRC = CRC.strip()
			CRC = CRC[0]
			input_error = input_error.strip()
			input_error = input_error[0]
	net_connect.disconnect()
	return int, duplex, speed, CRC, input_error

while True:

	switch = GetNextSwitch(MAC)
	if switch is not None:
		print("The mac address is connected to " + switch)
	else:
		print("Mac address not found!!")
		break

	if FindAttachedInterface(switch,MAC) is not None:
		interface, duplex, speed, CRC, input_error = FindAttachedInterface(switch, MAC)
		print("Mac address found")
		print(interface)
		print("Duplex: " + duplex)
		print("Speed: " + speed)
		print("CRC errors: " + CRC)
		print("Input_errors: " + input_error)
		break

	else:
		print('Mac address not found')
		break


input("Press Enter to Exit")
dist_connect.disconnect()
