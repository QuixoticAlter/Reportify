import selenium
import requests
from requests.exceptions import ConnectTimeout, SSLError

from IPs import Ips

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from selenium.common.exceptions import WebDriverException

from time import sleep
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

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--window-size=1960,1600")
    chrome_options.add_argument('log-level=3')
        
    driver = webdriver.Chrome(options=chrome_options)

    try:

        driver.get("https://%s" % (ip))

        # more_details = WebDriverWait(driver, 60).until(
        #     EC.presence_of_element_located((By.ID, "details-button")))
        # more_details.click()
        
        # proceed_link = WebDriverWait(driver, 60).until(
        #     EC.presence_of_element_located((By.ID, "proceed-link")))
        # proceed_link.click()

        login = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.ID, "EwsLogin")))
        login.click()

        password = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.ID, "PasswordTextBox")))
        password.send_keys("I10veR0ckNR011!!")

        submit = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.ID, "signInOk")))
        submit.click()

        general_menu_option = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.ID, "SettingsPages")))
        general_menu_option.click()

        solutions_installer_menu_option = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.ID, "SolutionInstaller")))
        solutions_installer_menu_option.click()

    except Exception as e:

        if type(e) == selenium.common.exceptions.WebDriverException:
            print(e)
            return None

    try:
        solutions_installed_div = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.ID, "SolutionsTable")))
        
        print("Solution installed")
        return True

    except:
        print("No solution")

    driver.close()

    return False

def check_solution(inventory_array):

    no_celiveo_array = []
    no_connection_array = []

    for row in inventory_array:

        serial = row[0]
        ip = row[4]

        print("\n\n-------------------------------------------------------------")
        print("IP: %s" % str(ip))

        try:
            r = requests.get("https://%s" % (ip))
        except Exception as e:
            print(type(e))
            if type(e) == requests.exceptions.SSLError:
                pass
            elif type(e) == requests.exceptions.ConnectTimeout:
                no_connection_array.append([serial, ip])
                continue
            elif type(e) == requests.exceptions.ConnectionError:
                no_connection_array.append([serial, ip])
                continue

        if not solution_is_installed(ip): no_celiveo_array.append([serial, ip])

    with open('no_celiveo_ips.txt', "w") as f:
        f.write('\n'.join(no_celiveo_array))
    
    with open("no_connection_ips.txt", "w") as f:
        f.write('\n'.join(no_connection_array))

if __name__ == "__main__":

    copy_reports()
    convert_excel_to_csv(inventory_excel, inventory_csv)
    inventory_array = set_inventory_array()
    check_solution(inventory_array)