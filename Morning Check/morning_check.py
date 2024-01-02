import requests
from requests.exceptions import ConnectTimeout, SSLError, ReadTimeout

import requests
from urllib3.exceptions import InsecureRequestWarning
from adapter import SSLAdapter

import shutil
import openpyxl
import csv
import subprocess

from nrds import check_nrds, create_nrd_report

inventory_excel = "files\\inventario.xlsx"
inventory_csv = "files\\inventario.csv"
nrd_excel = "files\\export_nrd.xlsx"
nrd_csv = "files\\export_nrd.csv"
service_request_excel = "files\\service_requests_history.xlsx"
service_requests_csv = "files\\service_requests_history.csv"

def copy_reports():

    shutil.copy("C:\\Users\\clsoportehp\\OneDrive - Enel Spa\\Reportes\\Inventario Completo ENEL.xlsx", "files\\inventario.xlsx")
    shutil.copy("C:\\Users\\clsoportehp\\Documents\\Reportes DCC\\Enel Global MS Devices.xlsx", "files\\export_nrd.xlsx")
    shutil.copy("C:\\Users\\clsoportehp\\Documents\\Reportes DCC\\ENEL Global MS - Service Visit History.xlsx", "files\\service_requests_history.xlsx")

def convert_excel_to_csv(input_file, output_file):

    newWorkbook = openpyxl.load_workbook(input_file)
    firstWorksheet = newWorkbook.active
    outputCsvFile = csv.writer(open(output_file, "w", encoding='utf-8'), delimiter=",")

    for eachrow in firstWorksheet.rows:
        row = [cell.value for cell in eachrow]
        outputCsvFile.writerow(row)

def write_larrays(lfile, larray): # lfile -> Log File; larray -> Log Array

    with open(lfile, "w") as f:
        f.write('\n'.join(larray))

def set_inventory_array():

    inventory_array_pre = []

    with open(inventory_csv, encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            inventory_array_pre.append(row)

    inventory_array = [list(map(lambda a:a.strip(), x))[0:20] for x in inventory_array_pre if isinstance(x, list) and x != []]

    return inventory_array

def set_nrd_array():

    nrd_array_pre = []
    
    with open(nrd_csv, encoding="utf-8") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=",")
        for row in spamreader:
            nrd_array_pre.append(row)

    nrd_array = [list(map(lambda a:a.strip(), x)) for x in nrd_array_pre if not x == [] and x[8] == "Chile"]

    print(nrd_array)

    return nrd_array

def set_service_requests_array():

    service_requests_array_pre = []

    with open(nrd_csv, encoding="utf-8") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=",")
        for row in spamreader:
            service_requests_array_pre.append(row)

    service_requests_array = [x for x in service_requests_array_pre[4:] if x[14] == "CL"]

    return service_requests_array

def has_conectivity(ip_address):

    result = subprocess.run("ping %s" % ip_address, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = result.stdout.decode('latin-1')

    # print(type(out))
    # print("ping output: %s" % out)

    if "enviados = 4, recibidos = 4" in out: return True

    return False

def get_data_from_inventory(serial, key, inventory_array):

    print("Get data from inventory")
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
        'Coordenadas': 9,
        'Level': 10,
        'Referencia en el piso': 11,
        'Punto de red': 12,
        'Grid': 13,
        'Device Status': 14,
        'Contacto': 15,
        'Teléfono': 16,
        'Correo': 17,
        'Checkeada': 18,
        'En Movimiento': 19,
        'Observaciones': 20
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
        r = requests.get(url, verify=False, timeout=20)
    except:
        try:
            s = requests.Session()
            s.mount('https://', SSLAdapter())
            print("Fetching through SSLv1")
            r = s.get(url, verify=False, timeout=5)
        except Exception as e:
            print(type(e))
            if type(e) == requests.exceptions.ConnectionError:
                print("Conenction Error!")
            elif type(e) == requests.exceptions.ReadTimeout:
                print("Read Timeout!")

            return "SSLv1 Connection Error"

    if r.text == "" or r.text == None: return None
    elif "Celiveo Enabled" in r.text: return True
    elif len(r.text) < 15000: return "No guest EWS"

    return False

def check_solution(inventory_array):

    connectivity_array = []
    invalid_ip_array = []
    no_connectivity_array = []
    no_connection_timeout_array = []
    no_connection_error_array = []
    no_connection_read_timeout_array = []
    no_connection_array_sslv1 = []
    operationals_no_conectivity = []
    no_celiveo_array = []
    no_web_array = []
    no_guest_ews_array = []

    for row in inventory_array[1:]:

        serial = row[0]
        ip = row[4]
        site = row[7]
        model = row[3]
        hostname = row[5]
        status = row[14]
        level = row[10]

        ip = ip.strip()

        print("\n\n-------------------------------------------------------------")
        print("IP: %s" % str(ip))

        invalid_ip_condition = ip == "0.0.0.0" or ip == None or ip == "" or  not "." in ip
        storage_levels_condition = level == "Bodega Santa Rosa" or level == "Bodega SO Piso 1" or level == "Bodega San Isidro Of. 7"

        if storage_levels_condition: 
            print("In Storage!")
            continue

        if invalid_ip_condition:
            print("Invalid or Empty IP!")
            invalid_ip_array.append("%s | %s | %s | %s | %s | %s" % (serial, model, ip, hostname, site, status))
            continue

        if not has_conectivity(ip):
            print('has connectivity!')
            no_connectivity_array.append("%s | %s | %s | %s | %s | %s" % (serial, model, ip, hostname, site, status))
            if status == "Operational":
                operationals_no_conectivity.append("%s | %s | %s | %s | %s | %s" % (serial, model, ip, hostname, site, status))
            continue
        else:
            print('Has no conectivity!')
            connectivity_array.append("%s | %s | %s | %s | %s | %s" % (serial, model, ip, hostname, site, status))

        try:
            r = requests.get("https://%s" % (ip), timeout=20)
            print("No exception!")
        except Exception as e:
            print(type(e))
            if type(e) == requests.exceptions.SSLError:
                pass
            elif type(e) == requests.exceptions.ConnectTimeout:
                no_connection_timeout_array.append("%s | %s | %s | %s | %s | %s" % (serial, model, ip, hostname, site, status))
                continue
            elif type(e) == requests.exceptions.ConnectionError:
                no_connection_error_array.append("%s | %s | %s | %s | %s | %s" % (serial, model, ip, hostname, site, status))
                continue
            elif type(e) == requests.exceptions.ReadTimeout:
                no_connection_read_timeout_array.append("%s | %s | %s | %s | %s | %s" % (serial, model, ip, hostname, site, status))
                continue

        bool_v = solution_is_installed(ip)

        if bool_v == None: no_web_array.append("%s | %s | %s | %s | %s" % (serial, model, ip, hostname, site))
        elif bool_v == "No guest EWS": no_guest_ews_array.append("%s | %s | %s | %s | %s" % (serial, model, ip, hostname, site))
        elif bool_v == "SSLv1 Connection Error": no_connection_array_sslv1.append("%s | %s | %s | %s | %s" % (serial, model, ip, hostname, site))
        elif not bool_v: no_celiveo_array.append("%s | %s | %s | %s | %s" % (serial, model, ip, hostname, site))

    write_larrays('connectivity_ips.txt', connectivity_array)
    write_larrays('invalid_ip_array.txt', invalid_ip_array)
    write_larrays('no_connectivity_ips.txt', no_connectivity_array)
    write_larrays('no_connection_timeout_array.txt', no_connection_timeout_array)
    write_larrays('no_connection_timeout_array.txt', no_connection_error_array)
    write_larrays('no_connection_read_timeout.txt', no_connection_read_timeout_array)
    write_larrays('no_connection_array_sslv1.txt', no_connection_array_sslv1)
    write_larrays('operationals_no_conectivity.txt', operationals_no_conectivity)
    write_larrays('no_celiveo_ips.txt', no_celiveo_array)
    write_larrays('no_web_ips.txt', no_web_array)
    write_larrays('no_guest_ews_array.txt', no_guest_ews_array)

if __name__ == "__main__":

    copy_reports()

    convert_excel_to_csv(inventory_excel, inventory_csv)
    # convert_excel_to_csv(nrd_excel, nrd_csv)
    # convert_excel_to_csv(service_request_excel, service_requests_csv)

    inventory_array = set_inventory_array()
    # nrd_array = set_nrd_array()

    check_solution(inventory_array)

    # nrd_report_array = check_nrds(nrd_array, service_requests_csv)
    # create_nrd_report(nrd_report_array)