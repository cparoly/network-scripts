from netmiko import ConnectHandler
from nornir import InitNornir
from nornir.plugins.tasks import commands
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import netmiko_send_command
from nornir.plugins.tasks.networking import netmiko_send_config
from nornir.plugins.tasks.networking import napalm_configure
import openpyxl


book = openpyxl.load_workbook("network devices.xlsx")
sheet = book.active
sheet["F1"] = "System"
row = 16
nr = InitNornir(core={"num_workers": 50},
	inventory={
		"plugin": "nornir.plugins.inventory.simple.SimpleInventory",
		"options": {
			"host_file": "inventory/hosts.yaml",
			"group_file": "inventory/groups.yaml",
			"default_file": "inventory/defaults.yaml"
		}
	}
)



show = nr.run(task=netmiko_send_command,
              command_string='show version | i Software')
for host in show:
	f = open(f"{host}.txt", "w")
	print(host)
	IOS = (show[host][0].result)
	print(IOS)
	print("-"*20)
	if "Nexus" in IOS:
		sheet.cell(row=row, column=6, value="Nexus")
	elif "Internetwork" in IOS:
		sheet.cell(row=row, column=6, value="Internetwork")
	elif "IOS-XE" or "XE" in IOS:
		sheet.cell(row=row, column=6, value="IOS-XE")
	elif "Adaptive Security Appliance" in IOS:
		sheet.cell(row=row, column=6, value="ASA")
	elif "IOS" in IOS:
		sheet.cell(row=row, column=6, value="IOS")
	else:
		continue





