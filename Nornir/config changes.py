from netmiko import ConnectHandler
from nornir import InitNornir
from nornir.plugins.tasks import commands
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import netmiko_send_command
from nornir.plugins.tasks.networking import netmiko_send_config
from nornir.plugins.tasks.networking import napalm_configure
import openpyxl

wb = openpyxl.load_workbook("all devices Spectrum.xlsx")
ws = wb.active


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

def snmp_file(task):
	file_name = task.host.get('img')
	result = task.run(task=netmiko_send_config, config_file=file_name)
	return result

def results_file(results):
	for host in results:
		f = open(f"{host}.txt", "w")
		f.write(results[host].result)


def to_excel(device):
	for host in device:
		working = device[host][1].result
		for cell in ws['A']:
			if cell.value is not None:
				if host in cell.value:
					row = cell.row
		if "configure" in working:
			ws.cell(row=row, column=9, value="Completed")

		else:
			ws.cell(row=row, column=9, value="Failed")

MIT_nexus = nr.filter(site='MIT').filter(type='Cisco NX OS')

# Below checks all hosts are found
# print("---"*20)
# print("NEXUS")
# print(MIT_nexus.inventory.hosts)
MIT_ios = nr.filter(site='MIT').filter(type='Cisco IOS - SSH Capable')

# Below checks all hosts are found
# print("---"*20)
# print("IOS")
# print(MIT_ios.inventory.hosts)
# MIT_inter = nr.filter(site='Westbury').filter(type='Internetwork')
# Below checks all hosts are found
# print("---"*20)
# print("INTER")
# print(MIT_inter.inventory.hosts)

nexus = MIT_nexus.run(task=netmiko_send_config,
						config_file='nexus.txt')

to_excel(nexus)
results_file(nexus)

ios = MIT_ios.run(task=netmiko_send_config,
						config_file='ios.txt')


to_excel(ios)
results_file(ios)

# inter = MIT_inter.run(task=netmiko_send_config,
# 						config_file='internetwork.txt')
#
# to_excel(inter)
# results_file(inter)




wb.save('all devices Spectrum.xlsx')








