from netmiko import ConnectHandler
from netmiko import NetMikoTimeoutException
from netmiko import NetMikoAuthenticationException
import re
import ipaddress
import getpass
from subprocess import Popen, PIPE


def router(x):
    # runs traceroute to find the router for dhcp configuration
    # will get the device from the hop before the last ip
    p = Popen(['traceroute', x, '-m 12'], stdout=PIPE)
    routes = []

    while True:
        line = p.stdout.readline()
        line = line.decode('utf-8')
        print(line)
        test = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', line)
        test = set(list(test))

        if len(test) > 0:
            routes.append(test)

        elif 'ms * *' in line:
            routes = routes[0]
            routes = "".join(routes)
            routes = routes.strip("''")
            break

        elif '* * *' in line:
            routes = routes[-1]
            routes = "".join(routes)
            routes = routes.strip("''")
            break
        else:
            continue

    return routes


dhcp_pool = 'show ip dhcp pool'
user = input("Username: ")
pwd = getpass.getpass()

while True:
    try:
        reserve = input("What is the IP address you are reserving?: ")
        IP = ipaddress.ip_address(reserve)
        break
    except ValueError:
        print("that is not a valid IP")
        continue

while True:
    try:
        MAC = input("What is the MAC Address of the device you want to reserve? (format xxxx.xxxx.xxxx): ")
        if re.match("^[0-9a-f\.]{5}[0-9a-f\.]{5}[0-9a-f]{4}$", MAC.lower()) is not None:
            break
        else:
            print('That is not the correct MAC ADDRESS format.')
            continue

    except Exception('That is not the correct MAC ADDRESS format.'):
        continue
device = router(reserve)

# Connect to device
input(f"The Device found is {device}, does this seem correct? (hit enter to continue or ctr+c to stop)")
print("Connecting to " + device)
cisco = {
    'device_type': 'cisco_ios',
    'host': device,
    'username': user,
    'password': pwd
}
try:
    net_connect = ConnectHandler(**cisco)
except NetMikoAuthenticationException:
    print("Username/password incorrect")

print(net_connect.find_prompt())
# clear the current binding for the ip address from the dhcp pool
clear = 'clear ip dhcp binding ' + str(IP)
output = net_connect.send_command(clear)
output = net_connect.send_command("show ip dhcp pool")

# Determines name of the new DHCP pool
counter = output.count("RESERVED")
counter += 1
# Determines the default router copying from the wired network
default_router = net_connect.send_command('show run | i default-router')
default_router = default_router.splitlines()
default_router = default_router[0]

# Send the commands to create the new reserved pool
# add in dns and domain
config_commands = ['ip dhcp pool RESERVED' + str(counter), 'host ' + str(IP), 'hardware-address ' + MAC,
                    default_router]
reserved = net_connect.send_config_set(config_commands)

print(reserved)
print(net_connect.send_command('show ip dhcp bind | i ' + str(IP)))
print(net_connect.send_command("wr"))
net_connect.disconnect()
input("Press Enter to exit")
