# Author: Pablo Godoy
# Corporate Mail: pablogodoy@manpowerchile.cl
# Personal Mail (Bussines Inquiries): sandman-ice@proton.me
# Position: OSA FASA (Chile)

# Instructions:
# 1. Download the supply order history report from DCC (Select a day previous to the last day in the report).
# 2. Download the consumable levels report from DCC.
# 3. Check if there is another file called "FASA Chile Global MS Supply Order History.xlsx", if it's the case remove it.
# 4. Check if there is another file called "FASA Chile Global MS Consumable Levels.xlsx", if it's the case remove it.
# 3. Excute this program through the command python make_consumable_report.py -d %d/%m/%Y
# 4. Enjoy It!

import requests
import openpyxl

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from datetime import datetime, timedelta

from config import *
from database import *
from deps.utils import has_conectivity

import argparse
import traceback

def get_n_guide_from_ingram_web(order_id):

    chrome_options = Options()
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://hpmps.ingrammicro.com")

    user =  WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, 'txtID')))
    user.clear()
    user.send_keys('247118')

    password = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, 'txtPassword')))
    password.clear()
    password.send_keys('1234567')

    submit = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, 'btnAutentificar')))
    submit.send_keys(Keys.RETURN)

    consultaxordenes = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '//div[@id="contenido_pnEstados"]/p/a')))
    consultaxordenes.click()

    order_input = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, 'contenido_orden')))
    order_input.send_keys(order_id)

    input_buscar_pedido = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, 'contenido_btnVerPedidos')))
    input_buscar_pedido.click()

    try:
        n_guide = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//table[@class="table table-hover"]/tbody/tr[2]/td[10]/a')))
        n_guide_text = n_guide.text
        n_guide_link = n_guide.get_attribute('href')

        r = requests.get(n_guide_link, allow_redirects=True)
        open('files/delivery_guides/%s.jpg' % n_guide_text, 'wb').write(r.content)

        driver.close()

        return n_guide_text

    except Exception as e:

        print(e)
        print(traceback.format_exc())
        return None

def generate_orders_report(rows):

    wb = openpyxl.Workbook()
    ws1 = wb.create_sheet("Sheet_A", 0)
    ws1.title = 'órdenes suministros'

    # print(wb.sheetnames)

    wb.active = wb["órdenes suministros"]
    ws = wb.active

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
        ws['A%s' % str(i+1)] = rows[i-1][0]
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

    ws0 = wb['Sheet']
    del wb[ws0]
    wb.save('files\\Reporte Suministros.xlsx')

def get_date(row):
    return row[0]

def main(startdate):

    datetime_start_date = datetime.strptime(startdate, '%d/%m/%Y')
    supply_report_rows = []

    for row in supply_order_array[1:]:

        # print('type of creation date: %s' % type(row[2]))

        datetime_creation_date = datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S')
        t_delta = datetime_creation_date.timestamp() - datetime_start_date.timestamp()

        if row[29] == "CHILE" and t_delta >= 0 and row[15] != "Maintenence":

            datetime_ct = datetime.strptime(row[2], "%Y-%m-%d %H:%M:%S")
            print("Creation Date: %s" % datetime_ct.strftime("%d/%m/%Y"))

            device_serial = row[11]
            if device_serial in exceptions: continue
            ip = get_data_from_access("select [IP Address] from inventario where [Serial Number] = ?", device_serial)
            model = row[13]
            sku = row[14]
            supply = row[15]
            status = row[5]
            destiny = get_data_from_access("select Building from inventario where [Serial Number] = ?", device_serial)
            n_request = row[0]
            n_ingram = row[21]
            n_guide = ''
            n_guide = get_n_guide_from_ingram_web(n_request)

            if row[6] == 'DCC':
                order_method = 'Manual'
            elif row[6] == 'FFN':
                order_method = 'Automático'

            supply_report_rows.append([
                datetime_ct, device_serial, ip, model,
                sku, supply, status, destiny, n_request,
                n_ingram, n_guide, '', '', '', '', '',
                order_method, '', ''
            ])

    ordered_supply_report_rows = sorted(supply_report_rows)
    formatted_suply_report_rows = [[
        x[0].strftime("%d/%m/%Y"), x[1], x[2], x[3],
        x[4], x[5], x[6], x[7], x[8], x[9], x[10],
        x[11], x[12], x[13], x[14], x[15], x[16], x[17]]
        for x in ordered_supply_report_rows]
    print('First element of total rows: %s' % formatted_suply_report_rows[0])
    return formatted_suply_report_rows

def nth_element_contains(x, l):

    if len(l) == 0: return None

    for i in range(0, len(l)):
        if x in l[i]: return i

    return None

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        prog='ASRG = Automatic Supply Report Generator',
        description='This program generates a supply report automatically.'
    )

    parser.add_argument('-d', '--startdate', help='The date from which the program will start to generate the final row/array to export. Format Accepted: DD/MM/YYYY')
    parser.add_argument('-c', '--consumable-web', action="store_true", help='Get consumable levels through web scraping')
    args = parser.parse_args()

    print("Start Date: %s" % args.startdate)

    if not args.consumable_web:
        black_levels_below_threshold = ConsumableLevel.select().where(
            (ConsumableLevel.detection_date >= (datetime.now() - timedelta(days=1))) & (ConsumableLevel.black_level <= Threshold) & (ConsumableLevel.machine != None)
        )
        cyan_levels_below_threshold = ConsumableLevel.select().where(
            (ConsumableLevel.detection_date >= (datetime.now() - timedelta(days=1))) & (ConsumableLevel.cyan_level <= Threshold) & (ConsumableLevel.machine != None)
        )
        magenta_levels_below_threshold = ConsumableLevel.select().where(
            (ConsumableLevel.detection_date >= (datetime.now() - timedelta(days=1))) & (ConsumableLevel.magenta_level <= Threshold) & (ConsumableLevel.machine != None)
        )
        yellow_levels_below_threshold = ConsumableLevel.select().where(
            (ConsumableLevel.detection_date >= (datetime.now() - timedelta(days=1))) & (ConsumableLevel.yellow_level <= Threshold) & (ConsumableLevel.machine != None)
        )

        last_30_days_black_supply_orders = SupplyOrder.select().where(
            (SupplyOrder.creation_date >= (datetime.now() - timedelta(days=30))) & (SupplyOrder.black_cartridge != None) & (SupplyOrder.machine != None)
        )
        last_30_days_cyan_supply_orders = SupplyOrder.select().where(
            (SupplyOrder.creation_date >= (datetime.now() - timedelta(days=30))) & (SupplyOrder.cyan_cartridge != None) & (SupplyOrder.machine != None)
        )
        last_30_days_magenta_supply_orders = SupplyOrder.select().where(
            (SupplyOrder.creation_date >= (datetime.now() - timedelta(days=30))) & (SupplyOrder.magenta_cartridge != None) & (SupplyOrder.machine != None)
        )
        last_30_days_yellow_supply_orders = SupplyOrder.select().where(
            (SupplyOrder.creation_date >= (datetime.now() - timedelta(days=30))) & (SupplyOrder.yellow_cartridge != None) & (SupplyOrder.machine != None)
        )

        print("Lenght of black levels below threshold: %s" % len(black_levels_below_threshold))
        print("Lenght of last 30-days supply orders: %s" % len(last_30_days_black_supply_orders))

        # for x in black_levels_below_threshold: print(type(x.detection_date))

        black_levels_below_threshold_serials = [x.machine.serial for x in black_levels_below_threshold]
        cyan_levels_below_threshold_serials = [x.machine.serial for x in cyan_levels_below_threshold]
        magenta_levels_below_threshold_serials = [x.machine.serial for x in magenta_levels_below_threshold]
        yellow_levels_below_threshold_serials = [x.machine.serial for x in yellow_levels_below_threshold]
        levels_below_threshold_array = [
            len(black_levels_below_threshold),
            len(cyan_levels_below_threshold),
            len(magenta_levels_below_threshold),
            len(yellow_levels_below_threshold),
        ]
        n_levels_below_threshold = sum(levels_below_threshold_array)

        last_30_days_black_supply_orders_serials = [x.machine.serial for x in last_30_days_black_supply_orders]
        last_30_days_cyan_supply_orders_serials = [x.machine.serial for x in last_30_days_cyan_supply_orders]
        last_30_days_magenta_supply_orders_serials = [x.machine.serial for x in last_30_days_magenta_supply_orders]
        last_30_days_yellow_supply_orders_serials = [x.machine.serial for x in last_30_days_yellow_supply_orders]

        black_orders_to_create = [(x, 'B') for x in black_levels_below_threshold_serials if x not in last_30_days_black_supply_orders_serials]
        cyan_orders_to_create = [(x, 'C') for x in cyan_levels_below_threshold_serials if x not in last_30_days_cyan_supply_orders_serials]
        magenta_orders_to_create = [(x, 'M') for x in magenta_levels_below_threshold_serials if x not in last_30_days_magenta_supply_orders_serials]
        yellow_orders_to_create = [(x, 'Y') for x in yellow_levels_below_threshold_serials if x not in last_30_days_yellow_supply_orders_serials]

        # bsbt -> But still below threshold
        black_orders_created_bsbt = [(x, 'B') for x in black_levels_below_threshold_serials if x in last_30_days_black_supply_orders_serials]
        cyan_orders_created_bsbt = [(x, 'C') for x in cyan_levels_below_threshold_serials if x in last_30_days_cyan_supply_orders_serials]
        magenta_orders_created_bsbt = [(x, 'M') for x in magenta_levels_below_threshold_serials if x in last_30_days_magenta_supply_orders_serials]
        yellow_orders_created_bsbt = [(x, 'Y') for x in yellow_levels_below_threshold_serials if x in last_30_days_yellow_supply_orders_serials]
        
        orders_to_create = black_orders_to_create + cyan_orders_to_create + magenta_orders_to_create + yellow_orders_to_create
        orders_created_bsbt = black_orders_created_bsbt + cyan_orders_created_bsbt + magenta_orders_created_bsbt + yellow_orders_created_bsbt

        all_orders_to_create = []
        for x in orders_to_create:
            order = [None, None, None, None, None]
            order_index = nth_element_contains(x[0], all_orders_to_create)
            if order_index != None:
                all_orders_to_create[order_index][1] = 'B' if x[1] == 'B' else all_orders_to_create[order_index][1]
                all_orders_to_create[order_index][2] = 'C' if x[1] == 'C' else all_orders_to_create[order_index][2]
                all_orders_to_create[order_index][3] = 'M' if x[1] == 'M' else all_orders_to_create[order_index][3]
                all_orders_to_create[order_index][4] = 'Y' if x[1] == 'Y' else all_orders_to_create[order_index][4]
            else:
                order[0] = x[0]
                order[1] = 'B' if x[1] == 'B' else None
                order[2] = 'C' if x[1] == 'C' else None
                order[3] = 'M' if x[1] == 'M' else None
                order[4] = 'Y' if x[1] == 'Y' else None
                all_orders_to_create.append(order)

        # for order in all_orders_to_create:
        #     m = Machine.get(Machine.serial == order[0])
        #     if has_conectivity(m.ip_addr): order += ['has conectivity']
        #     else: order += ['has no conectivity']

        try: os.remove('all_orders_to_create.txt')
        except: pass

        try: os.remove('orders_created_bsbt.txt')
        except: pass

        with open('orders_created_bsbt.txt', 'a') as f:
            for x in orders_created_bsbt:
                if x[1] == 'B': so = SupplyOrder.get(
                    (SupplyOrder.machine.serial == x[0]) and (SupplyOrder.black_cartridge != None) and (SupplyOrder.creation_date >= (datetime.now() - timedelta(days=30)))
                )
                if x[1] == 'C': so = SupplyOrder.get(
                    (SupplyOrder.machine.serial == x[0]) and (SupplyOrder.cyan_cartridge != None) and (SupplyOrder.creation_date >= (datetime.now() - timedelta(days=30)))
                )
                if x[1] == 'M': so = SupplyOrder.get(
                    (SupplyOrder.machine.serial == x[0]) and (SupplyOrder.magenta_cartridge != None) and (SupplyOrder.creation_date >= (datetime.now() - timedelta(days=30)))
                )
                if x[1] == 'Y': so = SupplyOrder.get(
                    (SupplyOrder.machine.serial == x[0]) and (SupplyOrder.yellow_cartridge != None) and (SupplyOrder.creation_date >= (datetime.now() - timedelta(days=30)))
                )

                f.write("%s %s %s %s\n" % (x[0], x[1], so.n_order, so.creation_date))

        with open('all_orders_to_create.txt', 'a') as f:
            f.write('total number of supplies below threshold: %s\n' % n_levels_below_threshold)
            for x in all_orders_to_create:
                f.write("%s %s %s %s %s\n" % (x[0], x[1], x[2], x[3], x[4]))