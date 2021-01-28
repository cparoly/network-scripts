from nornir import InitNornir
from nornir.plugins.tasks.networking import netmiko_send_command
from nornir.plugins.tasks.networking import netmiko_send_config
from openpyxl import Workbook
from nornir.plugins.functions.text import print_result, print_title
import ipdb

nr = InitNornir(core = {"num_workers": 50},
                inventory = {
	                "plugin": "nornir.plugins.inventory.simple.SimpleInventory",
	                "options": {
		                "host_file": "inventory/hosts.yaml",
		                "group_file": "inventory/groups.yaml",
		                "default_file": "inventory/defaults.yaml"
	                }
                }
                )
users = []


def add_user(task):
	task.run(task = netmiko_send_config,
	         config_commands = 'username testing priv 15 password test',
	         name = 'Add User')
	task.run(task = netmiko_send_command,
	         command_string = "show run | i username",
	         delay_factor = 3,
	         name = "VERIFYING USERNAMES")


def remove_config(task):
	usernames = task.run(task = netmiko_send_command,
	                     command_string = "show run | i username",
	                     delay_factor = 3,
	                     name = "FINDING USERNAMES")
	print(usernames.result)
	usernames = usernames.result
	usernames = usernames.split('\n')
	filter(None, usernames)
	for user in usernames:
		user = user.split(' ')
		print(user)
		try:
			user = user[1]
			task.run(task = netmiko_send_config,
			         config_commands = 'no username ' + user,
			         name = 'Removing Users')
		except IndexError:
			print("no username found for some reason")
			continue
	task.run(task=netmiko_send_config,
	         config_commands=['line vty 0 15', 'no password'],
	         delay_factor=3,
	         name="Remove password on VTY lines")
	task.run(task=netmiko_send_config,
	         config_commands=['line con 0', 'no password'],
	         delay_factor=3,
	         name="Remove password on Console")



def run_tasks(task):
	task.run(task = remove_config)
	task.run(task = add_user)


usernames = nr.run(task = run_tasks, name = "Standardizing Users")

# ipdb.set_trace()

print_result(usernames)
