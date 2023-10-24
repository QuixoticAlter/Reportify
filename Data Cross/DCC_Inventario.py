import csv
import openpyxl
import shutil

device_asset_csv = "files\\supply_order_history.csv"
device_asset_excel = "files\\supply_order_history.xlsx"
inventory_excel = "files\\inventario.xlsx"
inventory_csv = "files\\inventario.csv"

def copy_reports():

    shutil.copy("C:\\Users\\clsoportehp\\OneDrive - Enel Spa\\Reportes\\Inventario Completo ENEL.xlsx", "files\\inventario.xlsx")
    shutil.copy("C:\\Users\\clsoportehp\\Documents\\Reportes DCC\\ENEL Global MS Device Asset.xlsx", "files\\device_asset.xlsx")

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