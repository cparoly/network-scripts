import openpyxl
from openpyxl import Workbook
import socket
from netmiko import ConnectHandler
from netmiko import NetMikoTimeoutException
from netmiko import NetMikoAuthenticationException
import re
import ipaddress
import getpass
from subprocess import Popen, PIPE
mac_regex = re.compile(r'[0-9a-f]{4}\.[0-9a-f]{4}\.[0-9a-f]{4}')
int_regex = re.compile(r'Fa{1}\S*\d/\S*\d{1,2}|Gi{1}\S*\d/\S*\d|Eth{1}\d/\S*\d{1,2}|Te{1}\S*\d/\S*\d')
int_po_regex = re.compile(r'Po{1}\d*')
int_regexes = [int_regex, int_po_regex]
description_regex = re.compile(r'Description: (.*)', re.MULTILINE)
access_vlan_regex = re.compile(r'switchport access vlan (\d*)', re.MULTILINE)

wb = Workbook()
ws = wb.active


ws['B1'] = 'IPs'
ws['C1'] = 'Interface'
ws['D1'] = 'Duplex'
ws['E1'] = 'Speed'

user = input("Tacacs username: ")
pwd = input("Tacacs password" )

while True:
	try:

		file = input("What is the path to the excel file?(full path) ")
		book = openpyxl.load_workbook(file)
		sheet = book.active
		break
	except ValueError:
		print("Wrong file path")
		continue

col = input("What column number are the hostnames? ")
try:
	distribution = input("What is the distribution switch that will have the ARP table for these? ")
	distribution = ipaddress.ip_address(distribution)
except ValueError:
	distribution = socket.gethostbyname(distribution)

hosts = []
ips = []
count = 2
for column in sheet["A"]:
	hosts.append(column.value)
	ws.cell(row=count, column=1, value=column.value)
	count += 1

hosts=iter(hosts)
next(hosts)

count = 2


def ConnectToDevice(host):
	print ("Connecting to " + host)
	cisco = {
		'device_type': 'cisco_ios',
		'host': host,
		'username': user,
		'password': pwd
	}
	try:
		net_connect = ConnectHandler(**cisco)
	except NetMikoAuthenticationException:
		print("Username/password incorrect")

	return net_connect

def GetMac(ip):
	net_connect = ConnectToDevice()
	arp = net_connect.send_command("show ip arp " + ip)
	print(arp)
	mac = re.match("^[0-9a-f\.]{5}[0-9a-f\.]{5}[0-9a-f]{4}$", arp)
	return mac

def GetNextSwitch(ip, mac):
	net_connect = ConnectToDevice(ip)
	po = net_connect.send_command("show mac address-table address " + mac)
	po = re.search(int_po_regex, po)
	interface = net_connect.send_command("show run int " + str(po))
	for description in interface.splitlines():
		if 'Description:' in description:
			next_switch = description.split(':')[1].strip()

	return next_switch




def FindAttachedInterface(switch, mac):
	net_connect = ConnectToDevice(switch)
	interface = net_connect.send_command("show mac address-table address " + mac)
	int = re.search(int_regex, interface)
	summary = net_connect.send_command("show int " + str(int))
	for media in summary.splitlines():
		if 'media' in media:
			duplex = media.split(',')[0].strip()
			speed = media.split(',')[1].strip()

	return int, duplex, speed


for ip in hosts:

	ip = socket.gethostbyname(ip)

	ws.cell(row=count, column=2, value=ip)
	count += 1

	mac = GetMac(ip)
	next_switch = GetNextSwitch(ip, mac)

	print('The host is connected to ' + next_switch)
	interface, duplex, speed = FindAttachedInterface(next_switch, mac)
	ws.cell(row=count, column=3, value=interface)
	ws.cell(row=count, column=4, value=duplex)
	ws.cell(row=count, column=5, value=speed)

ws.save('host-interfaces.xlsx')
book.close()
