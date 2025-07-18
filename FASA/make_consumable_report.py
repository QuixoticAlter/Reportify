# Author: Pablo Godoy
# Corporate Mail: pablogodoy@manpowerchile.cl
# Personal Mail (Bussines Inquiries): sandman-ice@proton.me
# Position: OSA FASA (Chile)

# Instructions:
# 1. Download the supply order history report from DCC (Select a day previous to the last day in the report).
# 2. Download the consumable levels report from DCC.
# 3. Check if there is another file called "FASA Chile Global MS Supply Order History.xlsx", if it's the case remove it.
# 4. Check if there is another file called "FASA Chile Global MS Consumable Levels.xlsx", if it's the case remove it.
# 3. Excute this program through the command python make_consumable_report.py -i
# 4. Enjoy It!

import requests
import openpyxl
import re
import numpy as np
import pprint

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
import csv

from playwright.sync_api import sync_playwright

def get_n_guide_from_ingram_web(order_id):

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(ignore_https_errors=True)
        
        try:
            page.goto("https://hpmps.ingrammicro.com")

            user = page.locator("//input[@id='txtID']")
            user.wait_for(timeout=120000)
            user.type("246985")

            password = page.locator("//input[@id='txtPassword']")
            password.wait_for(timeout=120000)
            password.type("1234567")

            submit = page.locator("//input[@id='btnAutentificar']")
            submit.click()

        except Exception as e:
            print("Error on login!")

        try:
            consultaxordenes = page.locator("//div[@id='contenido_pnEstados']/p/a")
            consultaxordenes.wait_for(timeout=120000)
            consultaxordenes.click()

            order_input = page.locator("//input[@id='contenido_orden']")
            order_input.wait_for(timeout=120000)
            order_input.type(order_id)

            input_buscar_pedido = page.locator("//a[@id='contenido_btnVerPedidos']")
            input_buscar_pedido.wait_for(timeout=120000)
            input_buscar_pedido.click()

        except:
            print("Error on searching!")

        try:
            n_guide_link = page.locator("//table[@class='table table-hover']/tbody/tr[2]/td[10]/a")
            n_guide_link.wait_for(timeout=120000)
            n_guide_text = n_guide_link.inner_text()
        except:
            print("Error on getting the n guide!")

        r = requests.get(n_guide_link, allow_redirects=True)
        open('files/delivery_guides/%s.jpg' % n_guide_text, 'wb').write(r.content)

        return n_guide_text
    
def get_cartridges_install_date(ip_addr, model):

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(ignore_https_errors=True)

        try:
            print("Getting cartridges install date on https://%s/#hId-pgConsumables" % ip_addr)
            page.goto("https://%s/#hId-pgConsumables" % ip_addr)

            cyan_install_date = page.locator('//tr[@class="gui-list-tbl-even-row"][3]/td[2]')
            cyan_install_date.wait_for(timeout=120000)
            cyan_install_date_text = cyan_install_date.inner_text()

            magenta_install_date = page.locator('//tr[@class="gui-list-tbl-even-row"][3]/td[3]')
            magenta_install_date.wait_for(timeout=120000)
            magenta_install_date_text = magenta_install_date.inner_text()

            yellow_install_date = page.locator('//tr[@class="gui-list-tbl-even-row"][3]/td[4]')
            yellow_install_date.wait_for(timeout=120000)
            yellow_install_date_text = yellow_install_date.inner_text()

            black_install_date = page.locator('//tr[@class="gui-list-tbl-even-row"][3]/td[5]')
            black_install_date.wait_for(timeout=120000)
            black_install_date_text = black_install_date.inner_text()
        
        except:
            print("Error getting the cartridges install date!")
            return None

    return black_install_date_text, cyan_install_date_text, magenta_install_date_text, yellow_install_date_text

def get_supply_levels(ip_addr, model):
    
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(ignore_https_errors=True)

        black_level = None
        cyan_level = None
        yellow_level = None
        magenta_level = None

        try:

            if model == "HP OfficeJet Pro 9020":

                print("Getting supply levels on https://%s/#hId-pgConsumables" % ip_addr)
                page.goto("https://%s/#hId-pgConsumables" % ip_addr)

                cyan_level_element = page.locator('//table[@id="appConsumable-inkCart-tbl-Tbl"]/tbody/tr[9]/td[2]')
                cyan_level_element.wait_for(timeout=120000)
                cyan_level_text = cyan_level_element.inner_text()

                magenta_level_element = page.locator('//table[@id="appConsumable-inkCart-tbl-Tbl"]/tbody/tr[9]/td[3]')
                magenta_level_element.wait_for(timeout=120000)
                magenta_level_text = magenta_level_element.inner_text()

                yellow_level_element = page.locator('//table[@id="appConsumable-inkCart-tbl-Tbl"]/tbody/tr[9]/td[4]')
                yellow_level_element.wait_for(timeout=120000)
                yellow_level_text = yellow_level_element.inner_text()

                black_level_element = page.locator('//table[@id="appConsumable-inkCart-tbl-Tbl"]/tbody/tr[9]/td[5]')
                black_level_element.wait_for(timeout=120000)
                black_level_text = black_level_element.inner_text()

            elif model == "HP OfficeJet Pro 9130": return None # USE A SIMPLE CV FUNCTION TO DETECT THE LEVELS THROUGH A SCREENSHOT

                # print("Getting supply levels on https://%s" % ip_addr)

                #         page.

                #         cyan_level_element = page.locator('gauge-container-instanceId_40')
                #         cyan_level_element.wait_for(timeout=120000)
                #         cyan_level_text = cyan_level_element.inner_text()

                #         magenta_level_element = page.locator('//table[@id="appConsumable-inkCart-tbl-Tbl"]/tbody/tr[9]/td[3]')
                #         magenta_level_element.wait_for(timeout=120000)
                #         magenta_level_text = magenta_level_element.inner_text()

                #         yellow_level_element = page.locator('//table[@id="appConsumable-inkCart-tbl-Tbl"]/tbody/tr[9]/td[4]')
                #         yellow_level_element.wait_for(timeout=120000)
                #         yellow_level_text = yellow_level_element.inner_text()

                #         black_level_element = page.locator('//table[@id="appConsumable-inkCart-tbl-Tbl"]/tbody/tr[9]/td[5]')
                #         black_level_element.wait_for(timeout=120000)
                #         black_level_text = black_level_element.inner_text()
                
        except Exception as e:
            print (e)
            print("Error getting the supply levels!")
            return None

    return black_level_text, cyan_level_text, magenta_level_text, yellow_level_text
    
def nth_element_contains(x, l):

    if len(l) == 0: return None

    for i in range(0, len(l)):
        if x in l[i]: return i

    return None

def get_last_supply_order():
    return None

def check_high_consume_machines():

    orders = []

    for site in sites_high_consume_machines:

        m = Machine.get(Machine.id == site.machines.id)

        order = [m.serial, None, None, None, None]
        supply_levels = get_supply_levels(m.ip_addr, m.model)
        cartridge_install_date = get_cartridges_install_date(m.ip_addr, m.model, m.model)

        if supply_levels == None or cartridge_install_date == None: continue

        try: a = int(supply_levels[0]) <= 500
        except: a = supply_levels[0] == "Low"
        try: b = int(supply_levels[1]) <= 500
        except: b = supply_levels[1] == "Low"
        try: c = int(supply_levels[2]) <= 500
        except: c = supply_levels[2] == "Low"
        try: d = int(supply_levels[3]) <= 500
        except: d = supply_levels[3] == "Low"

        if a and datetime.strptime(cartridge_install_date[0], "%Y-%m-%d") >= get_last_supply_order(m.serial, "B"): order[1] = "B"
        if b and datetime.strptime(cartridge_install_date[1], "%Y-%m-%d") >= get_last_supply_order(m.serial, "C"): order[2] = "C"
        if c and datetime.strptime(cartridge_install_date[2], "%Y-%m-%d") >= get_last_supply_order(m.serial, "M"): order[3] = "M"
        if d and datetime.strptime(cartridge_install_date[3], "%Y-%m-%d") >= get_last_supply_order(m.serial, "Y"): order[4] = "Y"

def remove_space(l):

    lp = [x.replace(' ', '') for x in l]
    return lp

def get_last_arc_order_date(serial, color):

    colors = {'B': '3JA57AL', 'C':'3JA54AL', 'M': '3JA55AL', 'Y': '3JA56AL'}
    
    arc_orders = []

    with open(arc_orders_csv, encoding='latin-1') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            arc_orders.append(row)

    arc_orders_processed = [remove_space(x) for x in arc_orders]
    arc_order_selected = [x for x in arc_orders_processed if x[2] == serial]
    print('Size of arc order selected: %s' % len(arc_order_selected))
    if len(arc_order_selected) > 0:
        arc_order_selected.sort(reverse=True)
        if serial == 'TH36TH61W9':
            with open('arc_orders_array.txt', 'w') as f: f.write(str(arc_order_selected))
        return datetime.strptime(arc_order_selected[0][1], '%d-%m-%Y')
    
    return datetime.strptime('01-01-2000', '%d-%m-%Y')

def get_new_machines_orders():

    orders_to_create = []
    new_machines = NewMachine.select()

    for m in new_machines:

        order = [m.serial, None, None, None, None]

        supply_levels = get_supply_levels(m.ip_addr, m.model)
        cartridge_install_dates = get_cartridges_install_date(m.ip_addr, m.model)

        print(m.serial)
        print(supply_levels)
        print(cartridge_install_dates)

        if supply_levels == None or cartridge_install_dates == None: continue

        try: a = int(supply_levels[0]) <= 500
        except: a = supply_levels[0] == "Low"
        try: b = int(supply_levels[1]) <= 500
        except: b = supply_levels[1] == "Low"
        try: c = int(supply_levels[2]) <= 500
        except: c = supply_levels[2] == "Low"
        try: d = int(supply_levels[3]) <= 500
        except: d = supply_levels[3] == "Low"

        print(get_last_arc_order_date(m.serial, "B"))
        print(get_last_arc_order_date(m.serial, "C"))
        print(get_last_arc_order_date(m.serial, "M"))
        print(get_last_arc_order_date(m.serial, "Y"))

        if a and datetime.strptime(cartridge_install_dates[0], "%Y-%m-%d") >= get_last_arc_order_date(m.serial, "B"): order[1] = "B"
        if b and datetime.strptime(cartridge_install_dates[1], "%Y-%m-%d") >= get_last_arc_order_date(m.serial, "C"): order[2] = "C"
        if c and datetime.strptime(cartridge_install_dates[2], "%Y-%m-%d") >= get_last_arc_order_date(m.serial, "M"): order[3] = "M"
        if d and datetime.strptime(cartridge_install_dates[3], "%Y-%m-%d") >= get_last_arc_order_date(m.serial, "Y"): order[4] = "Y"

        if order[1] == None and order[2] == None and order[3] == None and order[4] == None: continue

        orders_to_create.append(order)

    with open("new_machines_low_levels.txt", "w") as f:
        for order in orders_to_create:
            f.write("%s %s %s %s %s\n" % (order[0], order[1], order[2], order[3], order[4]))

def get_last_24h_consumamble_levels(Threshold=30):

    blbt = ConsumableLevel.select().where(
         (ConsumableLevel.detection_date >= (datetime.now() - timedelta(hours=24))) & (ConsumableLevel.black_level <= Threshold) 
        & (ConsumableLevel.machine != None)
    )
    clbt = ConsumableLevel.select().where(
        (ConsumableLevel.detection_date >= (datetime.now() - timedelta(hours=24))) & (ConsumableLevel.cyan_level <= Threshold)
        & (ConsumableLevel.machine != None)
    )
    mlbt = ConsumableLevel.select().where(
        (ConsumableLevel.detection_date >= (datetime.now() - timedelta(hours=24))) & (ConsumableLevel.magenta_level <= Threshold)
        & (ConsumableLevel.machine != None)
    )
    ylbt = ConsumableLevel.select().where(
        (ConsumableLevel.detection_date >= (datetime.now() - timedelta(hours=24))) & (ConsumableLevel.yellow_level <= Threshold)
        & (ConsumableLevel.machine != None)
    )

    return blbt, clbt, mlbt, ylbt

def get_last_20d_supply_orders():

    l20dbo = SupplyOrder.select().where(
        (SupplyOrder.creation_date >= (datetime.now() - timedelta(days=20))) & (SupplyOrder.black_cartridge != None) & (SupplyOrder.machine != None)
    )
    last20dco = SupplyOrder.select().where(
        (SupplyOrder.creation_date >= (datetime.now() - timedelta(days=20))) & (SupplyOrder.cyan_cartridge != None) & (SupplyOrder.machine != None)
    )
    l20dmo = SupplyOrder.select().where(
        (SupplyOrder.creation_date >= (datetime.now() - timedelta(days=20))) & (SupplyOrder.magenta_cartridge != None) & (SupplyOrder.machine != None)
    )
    l20dyo = SupplyOrder.select().where(
        (SupplyOrder.creation_date >= (datetime.now() - timedelta(days=20))) & (SupplyOrder.yellow_cartridge != None) & (SupplyOrder.machine != None)
    )

    return l20dbo, last20dco, l20dmo, l20dyo

def get_old_orders_to_create():

    old_orders_to_create = []
    with open(final_orders_to_create_file) as f:
        old_orders_to_create = f.readlines()
        print(old_orders_to_create)

    check_old_orders_to_create = [x.split(' ')[0:-1] for x in old_orders_to_create if 'Check' in x]

    old_orders_to_create_db = OrderToCreate.select().where(OrderToCreate.perception_date >= datetime.now() - timedelta(days=20))
    old_orders_to_create_db_array = [
        [x.machine.serial, 
        'B' if x.black_needed else None,
        'C' if x.cyan_needed else None,
        'M' if x.magenta_needed else None,
        'Y' if x.yellow_needed else None]
        for x in old_orders_to_create_db
    ]

    total_old_orders_to_create = old_orders_to_create_db_array + check_old_orders_to_create

    with open('total_old_orders_to_create.txt', 'w') as f:
        pprint.pprint(total_old_orders_to_create, f)

    return total_old_orders_to_create

def save_old_orders_to_create(old_orders):

    orders_array = []
    for order in old_orders:
        order_dict = {
            'machine': Machine.get(Machine.serial == order[0]),
            'black_needed': order[1] == 'B',
            'cyan_needed': order[2] == 'C',
            'magenta_needed': order[3] == 'M',
            'yellow_needed': order[4] == 'Y',
            'perception_date': datetime.now(),
            'pending_of_creation': False
        }
        
        order_db = OrderToCreate.select().where(
            (OrderToCreate.machine == order_dict['machine']) &
            (OrderToCreate.black_needed == order_dict['black_needed']) & (OrderToCreate.cyan_needed == order_dict['cyan_needed']) &
            (OrderToCreate.magenta_needed == order_dict['magenta_needed']) & (OrderToCreate.yellow_needed == order_dict['yellow_needed']) & 
            (OrderToCreate.perception_date >= datetime.now() - timedelta(days=20))
        )

        if len(order_db) == 0: orders_array.append(order_dict)

    OrderToCreate.insert_many(orders_array).execute()

def get_row_avg(row):

    row_l = [row.black_level, row.magenta_level, row.cyan_level, row.yellow_level]
    return sum(row_l)/4

def order_final_orders_to_create(array):

    avg_array = []
    for i in range(0, len(array)):
        machine = Machine.get(Machine.serial == array[i][0])
        cl = ConsumableLevel.get(ConsumableLevel.machine == machine)
        avg_array.append((i, get_row_avg(cl)))

    avg_array.sort(key=lambda array:array[1])

    sorted_array = []

    for i in range(0, len(avg_array)):
        sorted_array.append(array[avg_array[i][0]])

    return sorted_array

def get_standard_machines_orders(consumable_web, installation_date):

    blbt, clbt, mlbt, ylbt = get_last_24h_consumamble_levels()
    blbt_10, clbt_10, mlbt_10, ylbt_10 = get_last_24h_consumamble_levels(Threshold_10)
    blbt_0, clbt_0, mlbt_0, ylbt_0 = get_last_24h_consumamble_levels(Threshold_0)
    l20dbo, last20dco, l20dmo, l20dyo = get_last_20d_supply_orders()

    total_supplies_below_10 = sum([len(blbt_10), len(clbt_10), len(mlbt_10), len(ylbt_10)])
    total_supplies_on_0 = sum([len(blbt_0), len(clbt_0), len(mlbt_0), len(ylbt_0)])

    black_levels_below_threshold_serials = [x.machine.serial for x in blbt]
    cyan_levels_below_threshold_serials = [x.machine.serial for x in clbt]
    magenta_levels_below_threshold_serials = [x.machine.serial for x in mlbt]
    yellow_levels_below_threshold_serials = [x.machine.serial for x in ylbt]

    last_30_days_black_supply_orders_serials = [x.machine.serial for x in l20dbo]
    last_30_days_cyan_supply_orders_serials = [x.machine.serial for x in last20dco]
    last_30_days_magenta_supply_orders_serials = [x.machine.serial for x in l20dmo]
    last_30_days_yellow_supply_orders_serials = [x.machine.serial for x in l20dyo]

    black_orders_to_create = [(x, 'B') for x in black_levels_below_threshold_serials if x not in last_30_days_black_supply_orders_serials]
    cyan_orders_to_create = [(x, 'C') for x in cyan_levels_below_threshold_serials if x not in last_30_days_cyan_supply_orders_serials]
    magenta_orders_to_create = [(x, 'M') for x in magenta_levels_below_threshold_serials if x not in last_30_days_magenta_supply_orders_serials]
    yellow_orders_to_create = [(x, 'Y') for x in yellow_levels_below_threshold_serials if x not in last_30_days_yellow_supply_orders_serials]
    
    orders_to_create = black_orders_to_create + cyan_orders_to_create + magenta_orders_to_create + yellow_orders_to_create
    
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

    if installation_date:

        for order in all_orders_to_create:
            machine = Machine.get(Machine.serial == order[0])
            cartridges_install_date = get_cartridges_install_date(machine.ip_addr, machine.model)
            supply_levels = get_supply_levels(machine.ip_addr, machine.model)
            # print(cartridges_install_date)
            # print(supply_levels)
            if cartridges_install_date == None and supply_levels == None: continue
            if 'B' in order:
                last_black_supply_orders = SupplyOrder.select().where((SupplyOrder.black_cartridge != None) & (SupplyOrder.machine == machine)).order_by(SupplyOrder.creation_date.desc())
                if len(last_black_supply_orders) != 0: last_black_supply_order = last_black_supply_orders[0]
                try:
                    print("Last black order date: %s" % last_black_supply_order.creation_date)
                    if last_black_supply_order.creation_date > datetime.strptime(cartridges_install_date[0], "%Y-%m-%d"): order[1] = None
                    if supply_levels[0] != 'Low':
                        if '>' in supply_levels[0]: order[1] = None
                        elif int(supply_levels[0]) >= 50 : order[1] = None
                except: continue
            if 'C' in order:
                last_cyan_supply_orders = SupplyOrder.select().where((SupplyOrder.cyan_cartridge != None) & (SupplyOrder.machine == machine)).order_by(SupplyOrder.creation_date.desc())
                if len(last_cyan_supply_orders) != 0: last_cyan_supply_order = last_cyan_supply_order = last_cyan_supply_orders[0]
                try:
                    print("Last Cyan order date: %s" % last_cyan_supply_order.creation_date)
                    if last_cyan_supply_order.creation_date > datetime.strptime(cartridges_install_date[1], "%Y-%m-%d"): order[2] = None
                    if supply_levels[1] != 'Low':
                        if '>' in supply_levels[1]: order[2] = None
                        elif int(supply_levels[1]) >= 50 : order[2] = None
                except: pass
            if 'M' in order:
                last_magenta_supply_orders = SupplyOrder.select().where((SupplyOrder.magenta_cartridge != None) & (SupplyOrder.machine == machine)).order_by(SupplyOrder.creation_date.desc())
                if len(last_magenta_supply_orders) != 0: last_magenta_supply_order = last_magenta_supply_orders[0]
                try:
                    if last_magenta_supply_order.creation_date > datetime.strptime(cartridges_install_date[2], "%Y-%m-%d"): order[3] = None
                    if supply_levels[2] != 'Low':
                        if '>' in supply_levels[2]: order[3] = None
                        elif int(supply_levels[2]) >= 50 : order[3] = None
                except: pass
            if 'Y' in order:
                last_yellow_supply_orders = SupplyOrder.select().where((SupplyOrder.yellow_cartridge != None) & (SupplyOrder.machine == machine)).order_by(SupplyOrder.creation_date.desc())
                if len(last_yellow_supply_orders) != 0: last_yellow_supply_order = last_yellow_supply_orders[0]
                try:
                    print("Last yellow order creation date: %s" % last_yellow_supply_order.creation_date)
                    if last_yellow_supply_order.creation_date > datetime.strptime(cartridges_install_date[3], "%Y-%m-%d"): order[4] = None
                    if supply_levels[3] != 'Low':
                        if '>' in supply_levels[3]: order[4] = None
                        elif int(supply_levels[3]) >= 50 : order[4] = None
                except: pass

    all_orders_to_create = [order for order in all_orders_to_create if not (order[1] == None and order[2] == None and order[3] == None and order[4] == None)]

    with open('all_orders_to_create.txt', 'w') as f:
        pprint.pprint(all_orders_to_create, f)

    old_orders_to_create = get_old_orders_to_create()
    save_old_orders_to_create(old_orders_to_create)

    types_order = []

    for order in old_orders_to_create:
        types_order.append(order)

    for t_order in types_order:
        print(t_order)

    final_orders_to_create = [order for order in all_orders_to_create if order not in old_orders_to_create]
    final_orders_to_create = order_final_orders_to_create(final_orders_to_create)

    try: os.remove('final_orders_to_create.txt')
    except: pass

    with open('final_orders_to_create.txt', 'a') as f:
        f.write('total number of supplies below threshold_10: %s\n' % total_supplies_below_10)
        for x in all_orders_to_create:
            f.write("%s %s %s %s %s\n" % (x[0], x[1], x[2], x[3], x[4]))

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        prog='ASRG = Automatic Supply Report Generator',
        description='This program generates a supply report automatically.'
    )

    parser.add_argument('-c', '--consumable-web', action="store_true", help='Get consumable levels through web scraping')
    parser.add_argument('-i', '--installation-dates', action="store_true", help="Get installation dates")
    args = parser.parse_args()

    consumable_web = False
    installation_date = False

    if args.consumable_web: consumable_web = True
    if args.installation_dates: installation_date = True

    get_standard_machines_orders(consumable_web, installation_date)
    # check_high_consume_machines()
    # get_new_machines_orders()