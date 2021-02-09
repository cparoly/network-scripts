from netmiko import ConnectHandler
import getpass
from datetime import datetime

pwd = getpass.getpass()


cisco = {
	'device_type': 'cisco_ios',
	'host': "10.20.3.117",
	'username': "cparoly",
	'password': pwd
}
starttime_time = datetime.now()

net_connect = ConnectHandler(**cisco)
output = net_connect.send_command("show run | i username")
output = output.split('\n')
output.remove('aaa authentication username-prompt Username:')
print(output)

for user in output:
	user = user.split(' ')
	user = user[1]
	cmd = ['no username ' + user, '\n']
	prompt = net_connect.send_config_set(cmd, cmd_verify=False)
	print(prompt)


net_connect.send_config_set("username testing")


# import ipdb
# ipdb.set_trace()
