from subprocess import Popen, PIPE
import re
def router(IP):
	p = Popen(['tracert', IP] , stdout=PIPE)
	routes = []


	while True:
		line = p.stdout.readline()
		line = line.decode('utf-8')
		test = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', line)

		if len(test) == 1:
			print(test)
			routes.append(test)
		elif 'complete' in line:
			routes = str(routes[-2])
			routes = routes.strip('[]')
			routes = routes.strip("''")
			break
		elif 'Request timed out' in line:
			routes = str(routes[-1])
			routes = routes.strip('[]')
			routes = routes.strip("''")
			break
		else:
			continue

	return routes

print (router('172.16.1.22'))










