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
    
def get_cartridges_install_date(ip_addr):

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

    return black_install_date_text, cyan_install_date_text, magenta_install_date_text, yellow_install_date_text
    
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

    parser.add_argument('-c', '--consumable-web', action="store_true", help='Get consumable levels through web scraping')
    parser.add_argument('-i', '--installation-dates', action="store_true", help="Get installation dates")
    args = parser.parse_args()

    if not args.consumable_web:
        black_levels_below_threshold = ConsumableLevel.select().where(
            (ConsumableLevel.detection_date >= (datetime.now() - timedelta(hours=24))) & (ConsumableLevel.black_level <= Threshold) 
            & (ConsumableLevel.machine != None)
        )
        cyan_levels_below_threshold = ConsumableLevel.select().where(
            (ConsumableLevel.detection_date >= (datetime.now() - timedelta(hours=24))) & (ConsumableLevel.cyan_level <= Threshold)
            & (ConsumableLevel.machine != None)
        )
        magenta_levels_below_threshold = ConsumableLevel.select().where(
            (ConsumableLevel.detection_date >= (datetime.now() - timedelta(hours=24))) & (ConsumableLevel.magenta_level <= Threshold)
            & (ConsumableLevel.machine != None)
        )
        yellow_levels_below_threshold = ConsumableLevel.select().where(
            (ConsumableLevel.detection_date >= (datetime.now() - timedelta(hours=24))) & (ConsumableLevel.yellow_level <= Threshold)
            & (ConsumableLevel.machine != None)
        )

        last_30_days_black_supply_orders = SupplyOrder.select().where(
            (SupplyOrder.creation_date >= (datetime.now() - timedelta(days=20))) & (SupplyOrder.black_cartridge != None) & (SupplyOrder.machine != None)
        )
        last_30_days_cyan_supply_orders = SupplyOrder.select().where(
            (SupplyOrder.creation_date >= (datetime.now() - timedelta(days=20))) & (SupplyOrder.cyan_cartridge != None) & (SupplyOrder.machine != None)
        )
        last_30_days_magenta_supply_orders = SupplyOrder.select().where(
            (SupplyOrder.creation_date >= (datetime.now() - timedelta(days=20))) & (SupplyOrder.magenta_cartridge != None) & (SupplyOrder.machine != None)
        )
        last_30_days_yellow_supply_orders = SupplyOrder.select().where(
            (SupplyOrder.creation_date >= (datetime.now() - timedelta(days=20))) & (SupplyOrder.yellow_cartridge != None) & (SupplyOrder.machine != None)
        )

        print("Lenght of black levels below threshold: %s" % len(black_levels_below_threshold))
        print("Lenght of last 30-days supply orders: %s" % len(last_30_days_black_supply_orders))

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

        with open("levels_below_threshold.txt", "w") as f:
            for serial in black_levels_below_threshold_serials: f.write("%s" %serial)

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
        
        if args.installation_dates:

            for order in all_orders_to_create:
                print("order: %s" % order)
                try:
                    machine = Machine.get(Machine.serial == order[0])
                    cartridges_install_date = get_cartridges_install_date(machine.ip_addr)
                    print(cartridges_install_date)
                except: continue
                if 'B' in order:
                    last_black_supply_orders = SupplyOrder.select().where(SupplyOrder.black_cartridge != None).order_by(SupplyOrder.creation_date.desc())
                    last_black_supply_order = last_black_supply_orders[0]
                    if last_black_supply_order.creation_date > datetime.strptime(cartridges_install_date[0], "%Y-%m-%d"): order[1] = None
                if 'C' in order:
                    last_cyan_supply_orders = SupplyOrder.select().where(SupplyOrder.cyan_cartridge != None).order_by(SupplyOrder.creation_date.desc())
                    last_cyan_supply_order = last_cyan_supply_orders[0]
                    if last_cyan_supply_order.creation_date > datetime.strptime(cartridges_install_date[1], "%Y-%m-%d"): order[2] = None
                if 'M' in order:
                    last_magenta_supply_orders = SupplyOrder.select().where(SupplyOrder.magenta_cartridge != None).order_by(SupplyOrder.creation_date.desc())
                    last_magenta_supply_order = last_magenta_supply_orders[0]
                    if last_magenta_supply_order.creation_date > datetime.strptime(cartridges_install_date[0], "%Y-%m-%d"): order[3] = None
                if 'Y' in order:
                    last_yellow_supply_orders = SupplyOrder.select().where(SupplyOrder.yellow_cartridge != None).order_by(SupplyOrder.creation_date.desc())
                    last_yellow_supply_order = last_yellow_supply_orders[0]
                    if last_yellow_supply_order.creation_date > datetime.strptime(cartridges_install_date[0], "%Y-%m-%d"): order[4] = None

            all_orders_to_create = [order for order in all_orders_to_create if not (order[1] == None and order[2] == None and order[3] == None and order[4] == None)]

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