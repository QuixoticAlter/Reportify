
from database import *
import requests

from datetime import datetime
from playwright.sync_api import sync_playwright
from make_consumable_report import get_last_24h_consumamble_levels, get_last_20d_supply_orders

def check_delivery_guide(order_id):

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

# Get machines with low levels recent orders
def get_machines_lwrc():

    blbt, clbt, mlbt, ylbt = get_last_24h_consumamble_levels()
    l20dbo, last20dco, l20dmo, l20dyo = get_last_20d_supply_orders()

    black_levels_below_threshold_serials = [x.machine.serial for x in blbt]
    cyan_levels_below_threshold_serials = [x.machine.serial for x in clbt]
    magenta_levels_below_threshold_serials = [x.machine.serial for x in mlbt]
    yellow_levels_below_threshold_serials = [x.machine.serial for x in ylbt]

    last_30_days_black_supply_orders_serials = [x.machine.serial for x in l20dbo]
    last_30_days_cyan_supply_orders_serials = [x.machine.serial for x in last20dco]
    last_30_days_magenta_supply_orders_serials = [x.machine.serial for x in l20dmo]
    last_30_days_yellow_supply_orders_serials = [x.machine.serial for x in l20dyo]

    black_serials_with_orders_created = [x for x in black_levels_below_threshold_serials if x in last_30_days_black_supply_orders_serials]
    cyan_serials_with_orders_created = [(x, 'C') for x in cyan_levels_below_threshold_serials if x in last_30_days_cyan_supply_orders_serials]
    magenta_serials_with_orders_created = [(x, 'M') for x in magenta_levels_below_threshold_serials if x in last_30_days_magenta_supply_orders_serials]
    yellow_serials_with_orders_created = [(x, 'Y') for x in yellow_levels_below_threshold_serials if x in last_30_days_yellow_supply_orders_serials]

    black_orders_created = [SupplyOrder.get(SupplyOrder.machine == Machine.get(Machine.serial == s)) for s in black_serials_with_orders_created]
    cyan_orders_created = [SupplyOrder.get(SupplyOrder.machine == Machine.get(Machine.serial == s)) for s in cyan_serials_with_orders_created]
    magenta_orders_created = [SupplyOrder.get(SupplyOrder.machine == Machine.get(Machine.serial == s)) for s in magenta_serials_with_orders_created]
    yellow_orders_created = [SupplyOrder.get(SupplyOrder.machine == Machine.get(Machine.serial == s)) for s in yellow_serials_with_orders_created]

    for order in black_orders_created:
        has_dg = check_delivery_guide(order.n_order)
        last_verification = datetime.now()