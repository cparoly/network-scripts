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
wb = openpyxl.load_workbook("MIT-s-r-done.xlsx")
ws = wb.active
ws["A1"] = "Hosts"
row = 2
MIT_router = nr.filter(site='MIT').filter(F(groups__contains='Router'))
MIT_switch = nr.filter(site='MIT').filter(F(groups__contains='Switch'))
MIT_asa = nr.filter(site='MIT').filter(type='ASA').filter(F(groups__contains='Firewall'))

for host in MIT_router:
    ws.cell(row=row, column=1, value=host)
    row += 1

for host in MIT_switch:
    ws.cell(row=row, column=1, value=host)
    row += 1

for host in MIT_asa:
    ws.cell(row=row, column=1, value=host)
    row += 1

wb.save("MIT-s-r-done.xlsx")