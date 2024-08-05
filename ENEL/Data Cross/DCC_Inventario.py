import csv
import openpyxl
import shutil
import pyodbc

device_asset_csv = "files\\supply_order_history.csv"
device_asset_excel = "files\\supply_order_history.xlsx"

def copy_reports():

    shutil.copy("C:\\Users\\clsoportehp\\Documents\\Reportes DCC\\ENEL Global MS Device Asset.xlsx", "files\\device_asset.xlsx")

def convert_excel_to_csv(input_file, output_file):

    newWorkbook = openpyxl.load_workbook(input_file)
    firstWorksheet = newWorkbook.active
    outputCsvFile = csv.writer(open(output_file, "w", encoding='utf-8'), delimiter=",")

    for eachrow in firstWorksheet.rows:
        row = [cell.value for cell in eachrow]
        outputCsvFile.writerow(row)

def get_data_from_access():

    conn = pyodbc.connect(
       r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\clsoportehp\OneDrive - Enel Spa\Respaldo\inventario.accdb;'
    )

    cursor = conn.cursor()
    cursor.execute('''
        select Serial, Etiqueta, Modelo, [Dirección IP], [Host Name], [MAC Address], 
        Site, [Level], [Device Status] from [Inventario Completo]
    ''')
    rows = cursor.fetchall()

    return rows

def set_inventory_array():

    inventory_array = get_data_from_access()
    return inventory_array

def set_device_asset_array():

    device_asset_array_pre = []

    with open(device_asset_csv, encoding="utf-8") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=",")
        for row in spamreader:
            device_asset_array.append(row)

    device_asset_array = [x for x in device_asset_array_pre[4:] if x[14] == "CL"]

    return device_asset_array

def main():

    copy_reports()
    return

if __name__ == '__main__':
    main()