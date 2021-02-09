from nornir import InitNornir
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import netmiko_send_config
from nornir.plugins.tasks.networking import netmiko_send_command
from nornir.core.filter import F
from openpyxl import Workbook
from tqdm import tqdm
import getpass
import ipdb

book = Workbook()
sheet = book.active
sheet['A1'] = "Usernames"

username = input("Enter your tacacs username: ")
password = getpass.getpass(prompt="Enter your tacacs password: ")

nr = InitNornir(core={"num_workers": 50},
                inventory={
                    "plugin": "nornir.plugins.inventory.simple.SimpleInventory",
                    "options": {
                        "host_file": "inventory/all-hosts3.yaml",
                        "group_file": "inventory/groups.yaml",
                        "default_file": "inventory/defaults.yaml"
                    }
                }
                )

nr.inventory.defaults.username = username
nr.inventory.defaults.password = password

users = []

testing = nr.filter(site="LIJ")


def get_username(task, progress):
    usernames = task.run(task=netmiko_send_command, command_string="show run | i username")
    progress.update()
    usernames = usernames.result
    usernames = usernames.split('\n')
    filter(None, usernames)
    usernames.remove('aaa authentication username-prompt Username:')
    filter(None, usernames)
    for user in usernames:
        user = user.split(' ')
        user = user[1]
        users.append(user)
        print(user)


with tqdm(total=len(nr.inventory.hosts), desc="Updating  ") as progress_bar:
    complete = nr.run(task=get_username, progress=progress_bar)
users = list(set(users))
print(users)

count = 2
for user in users:
    sheet.cell(row=count, column=1, value=user)
    count += 1

book.save("usernames.xlsx")
book.close()
