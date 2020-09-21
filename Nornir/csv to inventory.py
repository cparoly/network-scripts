import csv
import yaml

hosts = open(r'D:\Python stuff\scripts\work\Nornir\inventory\hosts.yaml', 'w')
hosts.write('---')
with open('devices.csv') as f:
	csv_2_yaml = csv.reader(f)
	next(csv_2_yaml)
	for row in csv_2_yaml:

		device = row[1]
		ip = row[2]
		platform = row[3]
		location = row[4]
		hosts.write("\n{0}:\n    hostname: {1}\n    groups:\n        - {2}\n"
			.format(device, ip, platform, location))


hosts.close()


