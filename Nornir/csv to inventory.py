import openpyxl

hosts = open(r'C:\Users\CParoly\PycharmProjects\work\Nornir\inventory\hosts.yaml', 'w')
hosts.write('---')
wb = openpyxl.load_workbook("network devices.xlsx")
ws = wb.active
count = 16
for row in ws.rows:

	device = ws.cell(row=count, column=3).value
	ip = ws.cell(row=count, column=5).value
	platform = ws.cell(row=count, column=2).value

	hosts.write("\n{0}:\n    hostname: {1}\n    groups:\n        - {2}\n"
				.format(device, ip, platform))
	count += 1

hosts.close()


