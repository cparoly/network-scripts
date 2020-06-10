import openpyxl

book = openpyxl.load_workbook('devices.xlsx')

sheet = book.active

devices = []
count = 2
for column in sheet['A']:
	count = 2
	devices.append(column.value)
	cell = sheet.cell(row= count, column = count)
	cell.value = "success"
	count += 1
	print("test" + str(count))
ips = iter(devices)
next(ips)

print(' '.join(ips))
book.save('devices.xlsx')


