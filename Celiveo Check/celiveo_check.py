import selenium
import requests
from requests.exceptions import ConnectTimeout, SSLError, ReadTimeout

import requests
from urllib3.exceptions import InsecureRequestWarning
from adapter import SSLAdapter

import shutil
import openpyxl
import csv

inventory_excel = "files\\inventario.xlsx"
inventory_csv = "files\\inventario.csv"

def copy_reports():

    shutil.copy("C:\\Users\\clsoportehp\\OneDrive - Enel Spa\\Reportes\\Inventario Completo ENEL.xlsx", "files\\inventario.xlsx")

def convert_excel_to_csv(input_file, output_file):

    newWorkbook = openpyxl.load_workbook(input_file)
    firstWorksheet = newWorkbook.active
    outputCsvFile = csv.writer(open(output_file, "w", encoding='utf-8'), delimiter=",")

    for eachrow in firstWorksheet.rows:
        row = [cell.value for cell in eachrow]
        outputCsvFile.writerow(row)

def set_inventory_array():

    inventory_array_pre = []

    with open(inventory_csv, encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            inventory_array_pre.append(row)

    inventory_array = [list(map(lambda a:a.strip(), x))[0:20] for x in inventory_array_pre if isinstance(x, list) and x != []]

    return inventory_array

def get_data_from_inventory(serial, key, inventory_array):

    print(serial)

    index_map = {
        'Serial': 0,
        'Etiqueta': 1,
        'SKU': 2,
        'Modelo': 3,
        'Dirección IP': 4,
        'Host Name': 5,
        'MAC Adress': 6,
        'Site': 7,
        'Building': 8,
        'Level': 9,
        'Referencia en el piso': 10,
        'Punto de red': 11,
        'Grid': 12,
        'Device Status': 13,
        'Contacto': 14,
        'Teléfono': 15,
        'Correo': 16,
        'Checkeada': 17,
        'En Movimiento': 18,
        'Observaciones': 19
    }

    # print('length of inventory array: %s' % str(len(inventory_array)))
    # print('second element of the array: %s' % str(inventory_array[1]))
    # print('serial: %s' % str(serial))
    # print('key: %s' % str(key))
    # print('field: %s' % str(index_map[key]))

    data_pre = [x[index_map[key]] for x in inventory_array if x[0] == serial]
    print('Data Pre: %s' % str(data_pre))
    data = data_pre[0]

    return data

def solution_is_installed(ip):

    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
    # requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += 'AES256-GCM-SHA384'

    url = "https://%s/hp/device/InternalPages/Index?id=ConfigurationPage" % ip

    try:
        r = requests.get(url, verify=False)
    except:
        try:
            s = requests.Session()
            s.mount('https://', SSLAdapter())
            print("Fetching through SSLv1")
            r = s.get(url, verify=False)
        except requests.exceptions.ConnectionError:
            return "SSLv1 Connection Error"

    if r.text == "" or r.text == None: return None
    elif "Celiveo Enabled" in r.text: return True
    elif len(r.text) < 15000: return "No guest EWS"

    return False

def check_solution(inventory_array):

    no_celiveo_array = []
    no_connection_array = []
    no_web_array = []
    no_connection_array_sslv1 = []
    no_guest_ews_array = []

    for row in inventory_array[1:]:

        serial = row[0]
        ip = row[4]
        site = row[7]
        model = row[3]
        hostname = row[5]

        print("\n\n-------------------------------------------------------------")
        print("IP: %s" % str(ip))

        try:
            r = requests.get("https://%s" % (ip), timeout=5)
            print("No exception!")
        except Exception as e:
            print(type(e))
            if type(e) == requests.exceptions.SSLError:
                pass
            elif type(e) == requests.exceptions.ConnectTimeout:
                no_connection_array.append("%s | %s | %s | %s | %s" % (serial, model, ip, hostname, site))
                continue
            elif type(e) == requests.exceptions.ConnectionError:
                no_connection_array.append("%s | %s | %s | %s | %s" % (serial, model, ip, hostname, site))
                continue
            elif type(e) == requests.exceptions.ReadTimeout:
                no_connection_array.append("%s | %s | %s | %s | %s" % (serial, model, ip, hostname, site))
                continue

        bool_v = solution_is_installed(ip)

        if bool_v == None: no_web_array.append("%s | %s | %s | %s | %s" % (serial, model, ip, hostname, site))
        elif bool_v == "No guest EWS": no_guest_ews_array.append("%s | %s | %s | %s | %s" % (serial, model, ip, hostname, site))
        elif bool_v == "SSLv1 Connection Error": no_connection_array_sslv1.append("%s | %s | %s | %s | %s" % (serial, model, ip, hostname, site))
        elif not bool_v: no_celiveo_array.append("%s | %s | %s | %s | %s" % (serial, model, ip, hostname, site))

    with open('no_celiveo_ips.txt', "w") as f:
        f.write('\n'.join(no_celiveo_array))
    
    with open("no_connection_ips.txt", "w") as f:
        f.write('\n'.join(no_connection_array))

    with open("no_web_ips.txt", "w") as f:
        f.write('\n'.join(no_web_array))

    with open("no_connection_sslv1.txt", "w") as f:
        f.write('\n'.join(no_connection_array_sslv1))

    with open("no_guest_EWS.txt", "w") as f:
        f.write('\n'.join(no_guest_ews_array))

if __name__ == "__main__":

    copy_reports()
    convert_excel_to_csv(inventory_excel, inventory_csv)
    inventory_array = set_inventory_array()
    check_solution(inventory_array)