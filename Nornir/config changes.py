from netmiko import ConnectHandler
from nornir import InitNornir
from nornir.plugins.tasks import commands
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import netmiko_send_command
from nornir.plugins.tasks.networking import netmiko_send_config
from nornir.plugins.tasks.networking import napalm_configure


f = open("output.txt", "w")
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



results= nr.run(task=netmiko_send_config,
               config_file='config-file.txt')

show = nr.run(task=netmiko_send_command,
              command_string='show run | i snmp-server')
for host in show:
	f = open(f"{host}.txt", "w")
	f.write(show[host].result)






