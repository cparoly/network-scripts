from netmiko import ConnectHandler
from nornir import InitNornir
from nornir.plugins.tasks import commands
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import netmiko_send_command
from nornir.plugins.tasks.networking import netmiko_send_config
from nornir.plugins.tasks.networking import napalm_configure
from nornir.core.filter import F
import openpyxl


nr = InitNornir(core={"num_workers": 100},
                inventory={
                    "plugin": "nornir.plugins.inventory.simple.SimpleInventory",
                    "options": {
                        "host_file": "inventory/hosts.yaml",
                        "group_file": "inventory/groups.yaml",
                        "default_file": "inventory/defaults.yaml"
                    }
                }
                )
wb = openpyxl.load_workbook("HH-s-r-todo.xlsx")
ws = wb.active
ws["A1"] = "Hosts"
row = 2
HH_nexus = nr.filter(site='Huntington Hospital').filter(type='Cisco NX OS').inventory.hosts.keys()
HH_ios = nr.filter(site='Huntington Hospital').filter(type='Cisco IOS - SSH Capable').inventory.hosts.keys()
HH_inter = nr.filter(site='Huntington Hospital').filter(type='Internetwork').inventory.hosts.keys()

for host in HH_nexus:
    ws.cell(row=row, column=1, value=host)
    row += 1

for host in HH_ios:
    ws.cell(row=row, column=1, value=host)
    row += 1

for host in HH_inter:
    ws.cell(row=row, column=1, value=host)
    row += 1

wb.save("HH-s-r-todo.xlsx")