
import openpyxl
import csv
import shutil
from datetime import datetime, timedelta

from config import *
from database import *

from playwright.sync_api import sync_playwright

def array_replace_char(x):

    processed_x = [a.replace(" ", "") for a in x]

    return processed_x

def convert_excel_to_csv(input_file, sheet_name, output_file):

    wb = openpyxl.load_workbook(input_file)
    firstWorksheet = wb[sheet_name]
    outputCsvFile = csv.writer(open(output_file, "w", encoding='utf-8'), delimiter=",")

    for eachrow in firstWorksheet.rows:
        row = [cell.value for cell in eachrow]
        outputCsvFile.writerow(row)

def csv_to_array(input_csv):

    array = []

    with open(input_csv, encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            array.append(row)

    array = [x for x in array if x != []]

    return array

def copy_reports():

    shutil.copy(Inventory_Route, inventory_excel)
    shutil.copy(SOH_Report_Route, supply_export_excel)
    shutil.copy(CL_Report_Route, consumable_levels_export_excel)
    shutil.copy(SR_Report_Route, service_requests_export_excel)
    shutil.copy(MDA_Report_Route, mda_export_excel)
    shutil.copy(NRD_Report_Route, nrd_export_excel)

def convert_excel_exports_to_csv():

    convert_excel_to_csv(inventory_excel, 'Inventario', inventory_csv)
    convert_excel_to_csv(supply_export_excel, 'Report', supply_export_csv)
    convert_excel_to_csv(consumable_levels_export_excel, 'Report', consumable_levels_export_csv)
    convert_excel_to_csv(service_requests_export_excel, 'Report', service_requests_export_csv)
    convert_excel_to_csv(mda_export_excel, 'Datos', mda_export_csv)
    convert_excel_to_csv(nrd_export_excel, 'Report', nrd_export_csv)

def get_supply_levels(ip_addr):
    
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(ignore_https_errors=True)

        black_level = None
        cyan_level = None
        yellow_level = None
        magenta_level = None

        try:
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
        
        except Exception as e:
            print (e)
            print("Error getting the supply levels!")
            return None

    cl_values = []
    for cl in [black_level_text, cyan_level_text, magenta_level_text, yellow_level_text]:

        cl_value = cl.replace("> ", "").strip()
        try: cl_value = int(cl)*100/2000
        except: cl_value = 0

        cl_values.append(cl_value)

    return cl_values

def update_inventory():

    inventory_array = csv_to_array(inventory_csv)

    for x in inventory_array[1:]:

        rows = Site.select().where(Site.name == x[7])
        if len(rows) == 0:
            site = Site()
            site.name = x[7]
            site.building = x[8]
            site.physical_address = x[9]
            site.city = x[10]
            site.save()
        else:
            query = Site.update(
                building = x[8],
                physical_address = x[9],
                city = x[10]
            ).where(Site.name == x[7])
            query.execute()

        rows = Machine.select().where(Machine.serial == x[0])
        if len(rows) == 0:
            machine = Machine()
            machine.serial = x[0]
            machine.asset = x[1]
            machine.sku = x[2]
            machine.model = x[3]
            machine.ip_addr = x[4]
            machine.hostname = x[5]
            machine.site = Site.get(Site.name == x[7])
            machine.status = x[13]
            machine.collection_method = x[14]
            machine.save()
        else:
            query = Machine.update(
                asset = x[1],
                sku = x[2],
                model = x[3],
                ip_addr = x[4],
                hostname = x[5],
                site = Site.get(Site.name == x[7]),
                status = x[13],
                collection_method = x[14]
            ).where(Machine.serial == x[0])
            query.execute()

        if x[17] == 'No es visible para el OSA en DCC, presuntamente por permisos':
            query = Machine.update(no_dcc=True).where(Machine.serial == x[0])
            query.execute()

def update_new_machines():

    new_machines_array = csv_to_array(new_machines_csv)

    for x in new_machines_array[1:]:

        rows = Site.select().where(Site.name == x[5])
        if len(rows) == 0:
            site = Site()
            site.name = x[5]
            site.building = x[7] + " - " + x[5]
            site.physical_address = x[6]
            site.city = x[7]
            site.save()
        else:
            query = Site.update(
                building = x[7] + " - " + x[5],
                physical_address = x[6],
                city = x[7]
            ).where(Site.name == x[5])
            query.execute()

        rows = NewMachine.select().where(NewMachine.serial == x[0])
        if len(rows) == 0:
            machine = NewMachine()
            machine.serial = x[0]
            machine.asset = x[1]
            machine.sku = x[2]
            machine.model = x[3]
            machine.ip_addr = x[4]
            machine.site = Site.get(Site.name == x[5])
            machine.status = x[9]
            machine.collection_method = x[10]
            machine.save()
        else:
            query = NewMachine.update(
                asset = x[1],
                sku = x[2],
                model = x[3],
                ip_addr = x[4],
                site = Site.get(Site.name == x[5]),
                status = x[9],
                collection_method = x[10]
            ).where(NewMachine.serial == x[0])
            query.execute()

def update_consumable_levels():

    consumable_levels_array = csv_to_array(consumable_levels_export_csv)

    for x in consumable_levels_array[4:]:
        rows = ConsumableLevel.select().where(ConsumableLevel.detection_date == datetime.strptime(x[9], '%m/%d/%Y %H:%M:%S'))
        if len(rows) == 0:
            consumable_level = ConsumableLevel()
            try:
                consumable_level.machine = Machine.get(Machine.serial == x[8])
            except Exception as e:
                try:
                    rmachine = RemovedMachine.get(RemovedMachine.serial == x[8])
                    consumable_level.removed_machine = rmachine
                except:
                    rmachine = RemovedMachine()
                    rmachine.serial = x[8]
                    rmachine.save()
                    consumable_level.removed_machine = rmachine
            consumable_level.detection_date = datetime.strptime(x[9], '%m/%d/%Y %H:%M:%S')
            consumable_level.magenta_level = 0 if x[12] == "out" else x[12]
            consumable_level.cyan_level = 0 if x[11] == "out" else x[11]
            consumable_level.yellow_level = 0 if x[13] == "out" else x[13]
            consumable_level.black_level = 0 if x[10] == "out" else x[10]
            consumable_level.save()

    consumable_level_serials = [x[8] for x in consumable_levels_array[3:]]
    all_invetory_serials = [m.serial for m in Machine.select()]
    isnicl = [x for x in all_invetory_serials if not x in consumable_level_serials] # -> Inventory serials not in consumbale levels

    for s in isnicl:
        print(s)
        try: m = Machine.get(Machine.serial == s)
        except: continue
        cls = get_supply_levels(m.ip_addr) if m.ip_addr != "0.0.0.0" else None
        if cls == None: continue
        print(cls)
        consumable_level = ConsumableLevel()
        consumable_level.machine = m
        consumable_level.detection_date = datetime.now()
        consumable_level.black_level = cls[0]
        consumable_level.cyan_level = cls[1]
        consumable_level.magenta_level = cls[2]
        consumable_level.yellow_level = cls[3]
        consumable_level.save()

def update_local_supply_orders():

    supply_orders_array = csv_to_array(automatic_orders_csv)
    supply_orders_array += csv_to_array(manual_orders_csv)
    supply_orders_array += csv_to_array(arc_orders_csv)

    processed_supply_orders = list(map(lambda x: array_replace_char(x), supply_orders_array))

    for x in processed_supply_orders:
        if x[0] != "n_order":
            rows = SupplyOrder.select().where(SupplyOrder.n_order == x[0])
            if len(rows) == 0:
                supplyorder = SupplyOrder()
                supplyorder.n_order = x[0]
                try:
                    supplyorder.machine = Machine.get(Machine.serial == x[2])
                except Exception as e:
                    try:
                        rmachine = RemovedMachine.get(RemovedMachine.serial == x[2])
                        supplyorder.removed_machine = rmachine
                    except:
                        rmachine = RemovedMachine()
                        rmachine.serial = x[2]
                        rmachine.save()
                        supplyorder.removed_machine = rmachine
                supplyorder.cyan_cartridge = "3JA54AL" if x[4] == "3JA54AL" else None
                supplyorder.magenta_cartridge =  "3JA55AL" if x[5] == "3JA55AL" else None
                supplyorder.yellow_cartridge = "3JA56AL" if x[6] == "3JA56AL" else None
                supplyorder.black_cartridge = "3JA57AL" if x[3] == "3JA57AL" else None
                print("Creation Date: %s" % str(x[1]))
                supplyorder.creation_date = datetime.strptime(x[1], '%d-%m-%Y')
                supplyorder.arrival_date = None
                supplyorder.close_date = None
                supplyorder.save()
            else:

                try:
                    m = Machine.get(Machine.serial == x[11])
                    query = SupplyOrder.update(machine_id = m.id).where(SupplyOrder.n_order == x[0])
                    query.execute()
                except: pass

                if x[4] == "3JA54AL":
                    query = SupplyOrder.update(cyan_cartridge = "3JA54AL").where(SupplyOrder.n_order == x[0])
                    query.execute()
                elif x[5] == "3JA55AL":
                    query = SupplyOrder.update(magenta_cartridge = "3JA55AL").where(SupplyOrder.n_order == x[0])
                    query.execute()
                elif x[6] == "3JA56AL":
                    query = SupplyOrder.update(yellow_cartridge = "3JA56AL").where(SupplyOrder.n_order == x[0])
                    query.execute()
                elif x[3] == "3JA57AL":
                    query = SupplyOrder.update(black_cartridge = "3JA57AL").where(SupplyOrder.n_order == x[0])
                    query.execute()

def update_supply_orders():

    supply_orders_array = csv_to_array(supply_export_csv)

    cartridge_parts = {
        "cyan": "3JA54AL",
        "magenta": "3JA55AL",
        "yellow": "3JA56AL",
        "black": "3JA57AL"
    }

    for x in supply_orders_array[4:]:
        rows = SupplyOrder.select().where(SupplyOrder.n_order == x[0])
        if len(rows) == 0:
            supplyorder = SupplyOrder()
            supplyorder.n_order = x[0]
            try:
                supplyorder.machine = Machine.get(Machine.serial == x[11])
            except Exception as e:
                try:
                    rmachine = RemovedMachine.get(RemovedMachine.serial == x[11])
                    supplyorder.removed_machine = rmachine
                except:
                    rmachine = RemovedMachine()
                    rmachine.serial = x[11]
                    rmachine.save()
                    supplyorder.removed_machine = rmachine
            supplyorder.cyan_cartridge = "3JA54AL" if x[14] == "3JA54AL" else None
            supplyorder.magenta_cartridge =  "3JA55AL" if x[14] == "3JA55AL" else None
            supplyorder.yellow_cartridge = "3JA56AL" if x[14] == "3JA56AL" else None
            supplyorder.black_cartridge = "3JA57AL" if x[14] == "3JA57AL" else None
            supplyorder.creation_date = datetime.strptime(x[2], '%Y-%m-%d %H:%M:%S')
            supplyorder.arrival_date = None
            supplyorder.close_date = None
            supplyorder.save()
        else:

            try:
                m = Machine.get(Machine.serial == x[11])
                query = SupplyOrder.update(machine_id = m.id).where(SupplyOrder.n_order == x[0])
                query.execute()
            except: pass

            if x[14] == "3JA54AL":
                query = SupplyOrder.update(cyan_cartridge = "3JA54AL").where(SupplyOrder.n_order == x[0])
                query.execute()
            elif x[14] == "3JA55AL":
                query = SupplyOrder.update(magenta_cartridge = "3JA55AL").where(SupplyOrder.n_order == x[0])
                query.execute()
            elif x[14] == "3JA56AL":
                query = SupplyOrder.update(yellow_cartridge = "3JA56AL").where(SupplyOrder.n_order == x[0])
                query.execute()
            elif x[14] == "3JA57AL":
                query = SupplyOrder.update(black_cartridge = "3JA57AL").where(SupplyOrder.n_order == x[0])
                query.execute()

def update_nrd():

    nrd_array = csv_to_array(nrd_export_csv)
    nrd_array_serials = [x[2] for x in nrd_array]
    # print("NRD Serials: %s" % nrd_serials)
    db_nrds = NRD.select()
    db_nrds_serials = [nrd.serial for nrd in db_nrds]

    new_nrds_serials = [x for x in nrd_array_serials if not x in db_nrds_serials]
    for x in new_nrds_serials:
        nrd = NRD()
        nrd.machine_associated = Machine.get()


    removed_nrds = [nrd for nrd in db_nrds if not nrd.machine_associated.serial in nrd_array_serials]
    
    for nrd in removed_nrds: print(nrd.id)
    for nrd in removed_nrds: NRD.delete_by_id(nrd.id)

def update_helpdesk_cases():

    mda_array = csv_to_array(mda_export_csv)

    for x in mda_array[1:]:
        rows = HelpDeskCase.select().where(HelpDeskCase.ticket == x[0])
        if len(rows) == 0:
            helpdeskcase = HelpDeskCase()
            helpdeskcase.ticket = x[0]
            helpdeskcase.description = x[1]
            if '-03:00' in x[5]: start_date = x[5].replace('T', ' ').replace('-03:00', '')
            if '-04:00' in x[5]: start_date = x[5].replace('T', ' ').replace('-04:00', '')
            if '-03:00' in x[6]: end_date = x[6].replace('T', ' ').replace('-03:00', '')
            if '-04:00' in x[6]: end_date = x[6].replace('T', ' ').replace('-04:00', '')
            helpdeskcase.start_date = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
            helpdeskcase.end_date = datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')
            try: site_associated = Site.get(Site.name == x[7].replace('Farmacia ', 'Local '))
            except Site.DoesNotExist: pass
            try: helpdeskcase.site_associated = site_associated
            except: pass
            try: helpdeskcase.machine_associated = Machine.get(Machine.site == site_associated)
            except: pass
            helpdeskcase.save()

def get_helpdesk_associated(machine, creation_date):

    try:
        helpdesk_case = HelpDeskCase.get(
            (HelpDeskCase.machine_associated == machine) & (HelpDeskCase.start_date >= (creation_date - timedelta(days=4)))
        )
        return helpdesk_case
    except HelpDeskCase.DoesNotExist: return False

def update_service_requests():

    service_requests_array = csv_to_array(service_requests_export_csv)

    service_requests_array = [x for x in service_requests_array if x != []]
    chanel_cases = [x for x in service_requests_array if "#SUBK" in x[6]]
    osatask_entries = [x for x in service_requests_array if "#OSATASK" in x[6]]
    osarr_entries = [x for x in service_requests_array if "#OSARR" in x[6]]

    for x in chanel_cases:
        rows_chanel_cases = ChannelCase.select().where(ChannelCase.n_case == x[2])
        if len(rows_chanel_cases) == 0:
            channel_case = ChannelCase()
            channel_case.n_case = x[2]
            channel_case.work_order = x[23]
            channel_case.status = x[19]
            try: channel_case.description = x[6][x[6].index("Descripción:")+12:x[6].index("Evento")]
            except: pass
            try: channel_case.creation_date = datetime.strptime(x[17], '%Y-%m-%dT%H:%M:%S.%f')
            except: channel_case.creation_date = datetime.strptime(x[17], '%Y-%m-%dT%H:%M:%S')
            if channel_case.status == 'Closed':
                try: channel_case.close_date = datetime.strptime(x[28], '%Y-%m-%dT%H:%M:%S.%f')
                except: channel_case.close_date = datetime.strptime(x[28], '%Y-%m-%dT%H:%M:%S')
            try: channel_case.machine_associated = Machine.get(Machine.serial == x[12])
            except: pass
            try:
                mda_case_associated = get_helpdesk_associated(
                    channel_case.machine_associated, channel_case.creation_date
                )
                if mda_case_associated: channel_case.helpdesk_case_associated = mda_case_associated
            except: pass
            channel_case.save()

if __name__ == "__main__":

    copy_reports()
    convert_excel_exports_to_csv()
    update_inventory()
    update_new_machines()
    update_consumable_levels()
    update_supply_orders()
    update_local_supply_orders()
    # update_nrd()
    # update_helpdesk_cases()
    update_service_requests()

    machine_serial = "TH9B46604M"
    machineObj = Machine.get(Machine.serial == machine_serial)
    site_name = machineObj.site.name
    print("Site Name: %s" % site_name)

    levels = [(x.black_level, x.cyan_level, x.magenta_level, x.yellow_level) for x in machineObj.consumable_levels][0]
    print(levels)
