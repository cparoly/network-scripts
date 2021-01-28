from nornir import InitNornir
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import netmiko_send_config
from nornir.core.filter import F
import openpyxl
from tqdm import tqdm
import getpass


nr = InitNornir(core={"num_workers": 50},
                inventory={
                    "plugin": "nornir.plugins.inventory.simple.SimpleInventory",
                    "options": {
                        "host_file": "inventory/all-hosts2.yaml",
                        "group_file": "inventory/groups.yaml",
                        "default_file": "inventory/defaults.yaml"
                    }
                }
                )

username = input("Enter your tacacs username: ")
password = getpass.getpass(prompt="Enter your tacacs password: ")

nr.inventory.defaults.username = username
nr.inventory.defaults.password = password

while True:
    location = input('Which type of location is being updated (Remote, Hospital, or Datacenter)? ')
    if location.capitalize() == "Datacenter":
        print('The following will be updated ' + location)
        yesno = input("Press enter if that is correct entry. (Y/N)")
        if yesno.lower() == "n":
            continue
        else:
            location = nr.filter(F(building=location.capitalize()))
            break
    elif location.capitalize() == "Hospital":
        print('The following will be updated ' + location)
        yesno = input("Press enter if that is correct entry. (Y/N)")
        if yesno.lower() == "n":
            continue
        else:
            location = nr.filter(F(building=location.capitalize()))
            break
    elif location.capitalize() == "Remote":
        print('The following will be updated ' + location)
        yesno = input("Press enter if that is correct entry. (Y/N)")
        if yesno.lower() == "n":
            continue
        else:
            location = nr.filter(F(building=location.capitalize()))
            break

def
devices = location.filter(F(type="Cisco IOS - SSH Capable") | F(type="Cisco NX OS") | F(type="Telnet") | F(type="DMVPN") | F(type="ASA"))