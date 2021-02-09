from socket import gethostbyaddr
import openpyxl

while True:
    try:

        file = input("What is the path to the excel file?(full path): ")
        input('The IP addresses must be in Column A (Press Enter to continue)')
        book = openpyxl.load_workbook(file)
        sheet = book.active
        break
    except ValueError:
        print("Wrong file path")
        continue


sheet["B1"] = "Hostname"

ipaddress = []

for ip in sheet["A"]:
    ipaddress.append(ip.value)

ipaddress = iter(ipaddress)
next(ipaddress)
count = 2

for ip in ipaddress:
    try:
        resolved = gethostbyaddr(ip)[0]
        sheet.cell(row=count, column=2, value=resolved)
        count += 1
    except:
        count += 1
        pass
print("Complete")
saved = input("Where do you want to save the file? (full path) or filename (will go in folder this script as ran from): ")
book.save(saved)
book.close()

input("Press any key to exit")