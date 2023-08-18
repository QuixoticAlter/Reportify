# Author: Pablo Godoy
# Corporate Mail: pablogodoy@manpowerchile.cl
# Personal Mail (Bussines Inquiries): sandman-ice@proton.me
# Position: OSA ENEL (Chile)

# Instructions:
# 1. Download the supply order history report from DCC (Select a day previous to the last day in the report).
# 2. Check if there is another file called "ENEL Global MS Supply Order History.xlsx", if it's the case remove it.
# 3. Excute this script through the command python make_consumable_report.py
# 4. Enjoy It!

import csv
import openpyxl
import requests
import shutil

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from PIL import Image
from pytesseract import pytesseract

from time import sleep
from datetime import datetime

import argparse

supply_export_csv = "Files\\supply_order_history.csv"
supply_export_excel = "Files\\supply_order_history.xlsx"
inventory_excel = "Files\\inventario.xlsx"
inventory_csv = "Files\\inventario.csv"

def copy_reports():

    supply_export_excel = shutil.copy("C:\\Users\\clsoportehp\\Downloads\\ENEL Global MS Supply Order History.xlsx","Files\\supply_order_history.xlsx")
    inventory_excel = shutil.copy("C:\\Users\\clsoportehp\\OneDrive - Enel Spa\\Reportes\\Inventario Completo ENEL.xlsx", "Files\\inventario.xlsx")

def get_conditional(value):

    a = not isinstance(value, type(None)) and not isinstance(value, int) and not isinstance(value, datetime)
    return a

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

    # with open('inventory_array.txt', 'w') as inventory_file:
    #     for x in inventory_array:
    #         inventory_file.write('%s\n' % str(x))

    # print('length of inventory array: %s' % str(len(inventory_array)))
    # print('1th element of inventory: %s' % str(inventory_array[0]))
    # print('Lenght of 1th element of inventory: %s' % str(len(inventory_array[0])))

    return inventory_array

def set_supply_order_array():

    supply_order_array_pre = []

    with open(supply_export_csv, encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            supply_order_array_pre.append(row)

    # with open('supply_order_array.txt', 'w') as supply_file:
    #     for x in supply_order_array_pre:
    #         supply_file.write('%s\n' % str(x))

    supply_order_array = [list(map(lambda a: a.strip(), x)) for x in supply_order_array_pre if isinstance(x, list) and x != []]

    # with open('supply_order_array2.txt', 'w') as supply_file:
    #     for x in supply_order_array:
    #         supply_file.write('%s\n' % str(x))

    # print('supply order array: %s' % supply_order_array[1])

    return supply_order_array[4:]

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

def get_n_guide_from_ingram_web(order_id):

    chrome_options = Options()
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://hpmps.anovo.cl")

    user = driver.find_element(By.ID, "txtID")
    user.clear()
    user.send_keys('247118')

    password = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'txtPassword')))
    password.clear()
    password.send_keys('1234567')

    submit = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'btnAutentificar')))
    submit.send_keys(Keys.RETURN)

    consultaxordenes = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[@id="contenido_pnEstados"]/p/a')))
    consultaxordenes.click()

    order_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'contenido_orden')))
    order_input.send_keys(order_id)

    input_buscar_pedido = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'contenido_btnVerPedidos')))
    input_buscar_pedido.click()

    try:
        n_guide = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//table[@class="table table-hover"]/tbody/tr[2]/td[10]/a')))
        n_guide_text = n_guide.text
        n_guide_link = n_guide.get_attribute('href')

        r = requests.get(n_guide_link, allow_redirects=True)
        open('delivery_guides/%s.jpg' % n_guide_text, 'wb').write(r.content)

        driver.close()

        return n_guide_text

    except Exception as e:

        print(e)
        return None

def create_update_the_report(rows):

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'control suministro'
    print(wb.sheetnames)

    ws['A1'] = 'Fecha de solicitud'
    ws['B1'] = 'N° de Serie'
    ws['C1'] = 'IP'
    ws['D1'] = 'Modelo'
    ws['E1'] = 'SKU'
    ws['F1'] = 'Nombre Suministro'
    ws['G1'] = 'Estado'
    ws['H1'] = 'Oficina Destino'
    ws['I1'] = 'N° Solicitud'
    ws['J1'] = 'N° Tracking Ingram'
    ws['K1'] = 'Guía de Despacho'
    ws['L1'] = 'Fecha recepción'
    ws['M1'] = 'Estado Pedido'
    ws['N1'] = 'Demora en entrega'
    ws['O1'] = 'Fecha de cambio'
    ws['P1'] = 'Días entre recepción y cambio'
    ws['Q1'] = 'Método de solicitud'
    ws['R1'] = 'Persona que recibe'
    ws['S1'] = 'Comentarios'

    for i in range(1, len(rows)):
        ws['A%s' % str(i+1)] = rows[i-1][0].split(' ')[0]
        ws['B%s' % str(i+1)] = rows[i-1][1]
        ws['C%s' % str(i+1)] = rows[i-1][2]
        ws['D%s' % str(i+1)] = rows[i-1][3]
        ws['E%s' % str(i+1)] = rows[i-1][4]
        ws['F%s' % str(i+1)] = rows[i-1][5]
        ws['G%s' % str(i+1)] = rows[i-1][6]
        ws['H%s' % str(i+1)] = rows[i-1][7]
        ws['I%s' % str(i+1)] = rows[i-1][8]
        ws['J%s' % str(i+1)] = rows[i-1][9]
        ws['K%s' % str(i+1)] = rows[i-1][10]
        ws['L%s' % str(i+1)] = rows[i-1][11]
        ws['M%s' % str(i+1)] = rows[i-1][12]
        ws['N%s' % str(i+1)] = rows[i-1][13]
        ws['O%s' % str(i+1)] = rows[i-1][14]
        ws['P%s' % str(i+1)] = rows[i-1][15]
        ws['Q%s' % str(i+1)] = rows[i-1][16]
        ws['R%s' % str(i+1)] = rows[i-1][17]

    wb.save('Reporte Suministros Histórico.xlsx')

def main(startdate):

    copy_reports()
    convert_excel_to_csv(inventory_excel, inventory_csv)
    convert_excel_to_csv(supply_export_excel, supply_export_csv)
    inventory_array = set_inventory_array()
    supply_order_array = set_supply_order_array()
    # print('length of inventory array: %s' % str(len(inventory_array)))
    # print('length of supply order array: %s' % str(len(supply_order_array)))

    datetime_start_date = datetime.strptime(startdate, '%d/%m/%Y')
    supply_report_rows = []

    for row in supply_order_array[1:]:

        # print('type of creation date: %s' % type(row[2]))

        datetime_creation_date = datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S')
        t_delta = datetime_creation_date.timestamp() - datetime_start_date.timestamp()

        if row[29] == "CHILE" and t_delta >= 0:

            datetime_ct = datetime.strptime(row[2], "%Y-%m-%d %H:%M:%S")
            str_ct = datetime_ct.strftime("%d/%m/%Y")
            creation_date = str_ct
            print("Creation Date: %s" % creation_date)

            device_serial = row[11]
            ip = get_data_from_inventory(device_serial, 'Dirección IP', inventory_array)
            model = row[13]
            sku = row[14]
            supply = row[15]
            status = row[5]
            destiny = get_data_from_inventory(device_serial, 'Building', inventory_array)
            n_request = row[0]
            n_ingram = row[21]
            n_guide = ''
            n_guide = get_n_guide_from_ingram_web(n_request)

            if row[6] == 'DCC':
                order_method = 'Manual'
            elif row[6] == 'FFN':
                order_method = 'Automático'

            # print('Fecha de creación: %s' % str(creation_date))
            # print('Serie: %s' % str(device_serial))
            # print('Dirección IP: %s' % str(ip))
            # print('Modelo: %s' % str(model))
            # print('Suministro: %s' % str(supply))
            # print('Estado: %s' % str(status))
            # print('Oficina Destino: %s' % str(destiny))
            # print('N° Solicitud: %s' % str(n_request))
            # print('N° Tracking Ingram %s' % str(n_ingram))
            # print('Guía de Despacho: %s' % str(n_guide))

            supply_report_rows.append([
                creation_date,
                device_serial,
                ip,
                model,
                sku,
                supply,
                status,
                destiny,
                n_request,
                n_ingram,
                n_guide,
                '',
                '',
                '',
                '',
                '',
                order_method,
                '',
                ''
            ])

    return supply_report_rows

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        prog='ASRG = Automatic Supply Report Generator',
        description='This program generates a supply report automatically.'
    )

    parser.add_argument('-d', '--startdate', help='The date from which the program will start to generate the final row/array to export. Format Accepted: DD-MM-YYYY')
    args = parser.parse_args()

    print(args.startdate)

    rows = main(args.startdate)
    print('Length of rows: %s' % str(len(rows)))
    print(rows[0])
    create_update_the_report(rows)