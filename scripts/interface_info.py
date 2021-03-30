from netmiko import ConnectHandler
from netmiko import NetMikoTimeoutException
from netmiko import NetMikoAuthenticationException
# from openpyxl import Workbook
# import openpyxl

# wb = Workbook()
# ws = wb.active
#file = input("What is the name of the file (include the .xlsx) " )
#book = openpyxl.load_workbook(f'./data_files/{file}')


#ip_line = input("What column are the IPs in? ")

ips = ['10.168.116.1']
#for column in sheet[ip_line]:
   # ips.append(column.value)


for ip in ips:
    cisco = {
        'device_type': 'cisco_ios',
        'host': ip,
        'username': 'cparoly',
        'password': 'blackbird.1'
    }

    net_connect = ConnectHandler(**cisco)

    interfaces = net_connect.send_command('show int', use_genie=True )
    count = 1
    for interface in interfaces:
        bandwidth = interfaces[interface]['bandwidth']
        duplex = interfaces[interface]['duplex_mode']
        speed = interfaces[interface]['port_speed']
        CRC = interfaces[interface]['counters']['in_crc_errors']
        input_errors = interfaces[interface]['counters']['in_errors']
        output_errors = interfaces[interface]['queues']['total_output_drop']
        
        # ws.cell(column=1, row=count, value=interface)
        # ws.cell(column=2, row=count, value=bandwidth)
        # ws.cell(column=3, row=count, value=duplex)
        # ws.cell(column=4, row=count, value=speed)
        # ws.cell(column=5, row=count, value=CRC)
        # ws.cell(column=6, row=count, value=input_errors)
        # ws.cell(column=7, row=count, value=output_errors)
        count += 1
        print('***' * 50)
        print(interface)
        print(f'Bandwidth {bandwidth}')
        print(f"Duplex {duplex}")
        print(f'CRC Errors {CRC}')
        print(f'Input Errors {input_errors}')
        print(f'Output Drops {output_errors}')

# wb.save('testing.xlsx')


