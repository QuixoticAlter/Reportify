import requests
from datetime import datetime
from database import SupplyOrder, Machine
from playwright.sync_api import sync_playwright
from make_consumable_report import get_supply_levels

def get_n_guide_from_ingram_web(order_id):

    no_info_ingram = False
    no_dg_link = False

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(ignore_https_errors=True)
        
        try:
            page.goto("https://hpmps.ingrammicro.com")

            user = page.locator("//input[@id='txtID']")
            user.wait_for(timeout=3000)
            user.type("246985")

            password = page.locator("//input[@id='txtPassword']")
            password.wait_for(timeout=3000)
            password.type("1234567")

            submit = page.locator("//a[@id='btnAutentificar']")
            submit.click()

        except Exception as e:
            print("Error on login!")

        try:
            consultaxordenes = page.locator("//div[@id='contenido_pnEstados']/p/a")
            consultaxordenes.wait_for(timeout=3000)
            consultaxordenes.click()

            order_input = page.locator("//input[@id='contenido_orden']")
            order_input.wait_for(timeout=3000)
            order_input.fill(str(order_id))

            input_buscar_pedido = page.locator("//a[@id='contenido_btnVerPedidos']")
            input_buscar_pedido.wait_for(timeout=3000)
            input_buscar_pedido.click()

        except Exception as e:
            print(e)
            print("Error on searching!")

        try:
            n_guide_table = page.locator("//table[@class='table table-hover']")
            n_guide_table.wait_for(timeout=3000)
        except:
            no_info_ingram = True
        
        try:
            n_guide_link = page.locator("//table[@class='table table-hover']/tbody/tr[2]/td[10]/a")
            n_guide_link.wait_for(timeout=3000)
            n_guide_text = n_guide_link.inner_text()
        except:
            no_dg_link = True

        return (no_info_ingram, no_dg_link)

def get_supply_orders():

    no_guides = []

    orders = SupplyOrder.select().where(SupplyOrder.creation_date >= datetime.strptime('01-08-2025', '%d-%m-%Y'))
    for order in orders:
        no_info_ingram, no_dg_link = get_n_guide_from_ingram_web(order.n_order)

        print(no_info_ingram, no_dg_link)
        
        if no_info_ingram: 
            try:
                machine = Machine.get(Machine.id == order.machine)

                partnumbers = [order.cyan_cartridge, order.magenta_cartridge, order.yellow_cartridge, order.black_cartridge]
                filt_partnumbers = [x for x in partnumbers if x != None]
                filt_partnumbers_str = ' - '.join(filt_partnumbers)

                try: bl, cl, ml, yl = get_supply_levels(machine.ip_addr, machine.model, machine.pin)
                except: bl, cl, ml, yl, = ["Desconocido", "Desconocido", "Desconocido", "Desconocido"]

                no_guides.append((
                    machine.serial, order.n_order, order.creation_date, filt_partnumbers_str,
                    'Sin informacion', 'Sin guia de despacho', bl, cl, ml, yl
                ))

            except:
                pass
            
            continue

        if no_dg_link:
            try:
                machine = Machine.get(Machine.id == order.machine)

                partnumbers = [order.cyan_cartridge, order.magenta_cartridge, order.yellow_cartridge, order.black_cartridge]
                filt_partnumbers = [x for x in partnumbers if x != None]
                filt_partnumbers_str = ' - '.join(filt_partnumbers)

                try: bl, cl, ml, yl = get_supply_levels(machine.ip_addr, machine.model, machine.pin)
                except: bl, cl, ml, yl, = ["Desconocido", "Desconocido", "Desconocido", "Desconocido"]

                no_guides.append((
                    machine.serial, order.n_order, order.creation_date, filt_partnumbers_str, 
                    'Con informacion', 'Sin guia de despacho', bl, cl, ml, yl
                ))
            
            except:
                pass

    return no_guides

no_guides = get_supply_orders()
with open("no_guides.txt", 'w') as f:
    for no_g in no_guides: f.write("%s,%s,%s,%s,%s,%s\n" % (
        no_g[0], no_g[1], no_g[2], no_g[3], no_g[4], no_g[5], no_g[6], no_g[7], no_g[8], no_g[9]
    ))