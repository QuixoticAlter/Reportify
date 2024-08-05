import requests
from requests.exceptions import ConnectTimeout, SSLError, ReadTimeout

import requests
from urllib3.exceptions import InsecureRequestWarning
from adapter import SSLAdapter

import shutil
import openpyxl
import csv
import subprocess
import pyodbc

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from PIL import Image

from nrds import check_nrds, create_nrd_report

inventory_excel = "files\\inventario.xlsx"
inventory_csv = "files\\inventario.csv"
nrd_excel = "files\\export_nrd.xlsx"
nrd_csv = "files\\export_nrd.csv"
service_request_excel = "files\\service_requests_history.xlsx"
service_requests_csv = "files\\service_requests_history.csv"
access_db = "C:\\Users\\clsoportehp\\OneDrive - Enel Spa\\Respaldo\\Respaldo Inventario.accdb"

def copy_reports():

    shutil.copy("C:\\Users\\clsoportehp\\Documents\\Reportes DCC\\Enel Global MS Devices.xlsx", "files\\export_nrd.xlsx")
    shutil.copy("C:\\Users\\clsoportehp\\Documents\\Reportes DCC\\ENEL Global MS - Service Visit History.xlsx", "files\\service_requests_history.xlsx")

def get_data_from_access():

    conn = pyodbc.connect(
       r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\clsoportehp\OneDrive - Enel Spa\Respaldo\inventario.accdb;'
    )

    cursor = conn.cursor()
    cursor.execute('''
        select Serial, Etiqueta, Modelo, [Dirección IP], [Host Name], [MAC Address], 
        Site, [Level], [Device Status] from [Inventario Completo]
    ''')
    rows = cursor.fetchall()

    return rows

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

    inventory_array = get_data_from_access()
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
        'Modelo': 2, 
        'Dirección IP': 3, 
        'Host Name': 4, 
        'MAC Address': 5, 
        'Site': 6, 
        'Level': 7, 
        'Device Status': 8
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

def has_corporative_background(ip):

    # Control Panel snapshot url
    url = "https://%s/hp/device/ControlPanelSnapshot/Index" % ip

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--window-size=1960,1600")
    chrome_options.add_argument('log-level=3')

    driver = webdriver.Chrome(options=chrome_options)
    try:
        driver.get(url)
    except:
        return None

    try:
        img = WebDriverWait(driver, 120).until(
            EC.presence_of_element_located((By.ID, 'ControlPanelSnapshotImage'))
        )
    except:
        return 'Timeout'

    # coordinates = img.rect
    # x = coordinates['x']
    # y = coordinates['y']
    # width = coordinates['width']
    # height = coordinates['height']

    img.screenshot('./control_panel_snapshot.png')

    driver.close()

    im = Image.open('./control_panel_snapshot.png')
    pixel_list = list(im.getdata())
    n_white_pixels = pixel_list.count((255, 255, 255, 255))
    n_pixels = len(pixel_list)
    white_pixels_ratio = n_white_pixels/n_pixels

    print('White pixels ratio: %s' % white_pixels_ratio)

    if white_pixels_ratio > 0.3:
        print("No corporative background!")
        return False

    return True

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
    no_corporative_background_array = []
    web_timeout_array = []

    for row in inventory_array:

        serial = row[0]
        ip = row[3]
        site = row[6]
        model = row[2]
        hostname = row[4]
        status = row[8]
        level = row[7]

        print("\n\n-------------------------------------------------------------")
        print("IP: %s" % str(ip))

        invalid_ip_condition = ip == "0.0.0.0" or ip == None or ip == "" or  not "." in ip
        storage_site_condition = level == "Bodega SO"

        if storage_site_condition: 
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

        bool_c = has_corporative_background(ip)
        if not bool_c:
            print('No corporative background!')
            no_corporative_background_array.append("%s | %s | %s | %s | %s" % (serial, model, ip, hostname, site))
        elif bool_c == 'Timeout':
            web_timeout_array.append("%s | %s | %s | %s | %s" % (serial, model, ip, hostname, site))
        elif bool_c == None:
            no_web_array.append("%s | %s | %s | %s | %s" % (serial, model, ip, hostname, site))

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
    write_larrays('no_corporative_background_array.txt', no_corporative_background_array)
    write_larrays('web_timeout_array.txt', web_timeout_array)

if __name__ == "__main__":

    # copy_reports()

    convert_excel_to_csv(inventory_excel, inventory_csv)
    # convert_excel_to_csv(nrd_excel, nrd_csv)
    # convert_excel_to_csv(service_request_excel, service_requests_csv)

    inventory_array = set_inventory_array()
    # nrd_array = set_nrd_array()

    check_solution(inventory_array)

    # nrd_report_array = check_nrds(nrd_array, service_requests_csv)
    # create_nrd_report(nrd_report_array)