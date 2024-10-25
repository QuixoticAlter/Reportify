
import openpyxl
import csv
import shutil
from datetime import datetime, timedelta

from config import *
from database import *

def convert_excel_to_csv(input_file, sheet_name, output_file):

    wb = openpyxl.load_workbook(input_file)
    firstWorksheet = wb[sheet_name]
    outputCsvFile = csv.writer(open(output_file, "w", encoding='utf-8'), delimiter=",")

    for eachrow in firstWorksheet.rows:
        row = [cell.value for cell in eachrow]
        outputCsvFile.writerow(row)

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

def update_inventory():

    inventory_array = []

    with open(inventory_csv, encoding='latin-1') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            inventory_array.append(row)

    inventory_array = [x for x in inventory_array if x != []]

    for x in inventory_array[1:]:

        rows = Site.select().where(Site.name == x[6])
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

def update_consumable_levels():

    consumable_levels_array = []

    with open(consumable_levels_export_csv, encoding='latin-1') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            consumable_levels_array.append(row)

    consumable_levels_array = [x for x in consumable_levels_array if x != []]

    for x in consumable_levels_array[3:]:
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

def update_supply_orders():

    supply_orders_array = []

    with open(supply_export_csv, encoding='latin-1') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            supply_orders_array.append(row)

    supply_orders_array = [x for x in supply_orders_array if x != []]

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

    nrd_array = []

    with open(nrd_export_csv, encoding='latin-1') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            nrd_array.append(row)

    nrd_array = [x for x in nrd_array if x != []]

    for x in nrd_array[1:]:
        print("NRD Serial: %s" % x[2])
        rows = NRD.select().where(NRD.machine_associated == Machine.get(Machine.serial == x[2]))
        if len(rows) == 0:
            nrd = NRD()
            try: nrd.machine_associated = Machine.get(Machine.serial == x[2])
            except Machine.DoesNotExist: continue
            nrd.last_collection_date = x[4]
            nrd.save()
        
    nrd_serials = [x[2] for x in nrd_array]
    # print("NRD Serials: %s" % nrd_serials)
    db_nrds = NRD.select()
    removed_nrds = [nrd for nrd in db_nrds if not nrd.machine_associated.serial in nrd_serials]
    for nrd in removed_nrds: print(nrd.id)
    for nrd in removed_nrds: NRD.delete_by_id(nrd.id)

def update_helpdesk_cases():

    mda_array = []

    with open(mda_export_csv, encoding='latin-1') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            mda_array.append(row)

    mda_array = [x for x in mda_array if x != []]

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

    service_requests_array = []

    with open(service_requests_export_csv, encoding='latin-1') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            service_requests_array.append(row)

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
    update_consumable_levels()
    update_supply_orders()
    update_nrd()
    update_helpdesk_cases()
    update_service_requests()

    machine_serial = "TH9B46604M"
    machineObj = Machine.get(Machine.serial == machine_serial)
    site_name = machineObj.site.name
    print("Site Name: %s" % site_name)

    levels = [(x.black_level, x.cyan_level, x.magenta_level, x.yellow_level) for x in machineObj.consumable_levels][0]
    print(levels)
