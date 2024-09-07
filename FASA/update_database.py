
import openpyxl
import csv
import shutil
from datetime import datetime

from config import *
from database import *

def convert_excel_to_csv(input_file, output_file):

    newWorkbook = openpyxl.load_workbook(input_file)
    firstWorksheet = newWorkbook.active
    outputCsvFile = csv.writer(open(output_file, "w", encoding='latin-1'), delimiter=",")

    for eachrow in firstWorksheet.rows:
        row = [cell.value for cell in eachrow]
        outputCsvFile.writerow(row)

def copy_reports():

    shutil.copy(Inventory_Route, inventory_excel)
    shutil.copy(SOH_Report_Route, supply_export_excel)
    shutil.copy(CL_Report_Route, consumable_levels_export_excel)
    # shutil.copy(MDA_Report_Name, mda_export_excel)

def convert_excel_exports_to_csv():

    convert_excel_to_csv(inventory_excel, inventory_csv)
    convert_excel_to_csv(supply_export_excel, supply_export_csv)
    convert_excel_to_csv(consumable_levels_export_excel, consumable_levels_export_csv)
    # convert_excel_to_csv(mda_export_excel, mda_export_csv)

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
            site.name = x[6]
            site.building = x[7]
            site.physical_address = x[8]
            site.city = x[9]
            site.save()
        else:
            query = Site.update(
                building = x[7],
                physical_address = x[8],
                city = x[9]
            ).where(Site.name == x[6])
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
            machine.site = Site.select().where(Site.name == x[6])
            machine.status = x[12]
            machine.collection_method = x[13]
            machine.save()
        else:
            query = Machine.update(
                asset = x[1],
                sku = x[2],
                model = x[3],
                ip_addr = x[4],
                hostname = x[5],
                site = Site.select().where(Site.name == x[6]),
                status = x[12],
                collection_method = x[13]
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

        rows = ConsumableLevel.select().where(ConsumableLevel.detection_date == x[9])
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

if __name__ == "__main__":

    copy_reports()
    convert_excel_exports_to_csv()
    update_inventory()
    update_consumable_levels()
    update_supply_orders()

    machine_serial = "TH9B46604M"
    machineObj = Machine.get(Machine.serial == machine_serial)
    site_name = machineObj.site.name
    print("Site Name: %s" % site_name)

    levels = [(x.black_level, x.cyan_level, x.magenta_level, x.yellow_level) for x in machineObj.consumable_levels][0]
    print(levels)
