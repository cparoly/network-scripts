from nornir import InitNornir
from nornir.plugins.tasks.networking import netmiko_send_command
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import tcp_ping



nr = InitNornir(
	core = {"num_workers": 10},
	inventory = {"plugin": "nornir.plugins.inventory.simple.SimpleInventory",
	             "options": {
		             "host_file": "inventory/hosts.yaml",
		             "group_file": "inventory/groups.yaml"

	             }
	    }
)

result = nr.run(task = tcp_ping

)
