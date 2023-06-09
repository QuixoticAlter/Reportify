# Autor: Pablo Godoy
# Correo Corporativo: pablogodoy@manpowerchile.cl
# Correo Personal: sandman-ice@proton.me
# Cargo: OSA ENEL

import csv
import openpyxl
import selenium
import requests

def convert_excel_to_csv(input_file, output_file):

    newWorkbook = openpyxl.load_workbook(input_file)
    firstWorksheet = newWorkbook.active
    outputCsvFile = csv.writer(open(output_file, "w", encoding='utf-8'), delimiter=",")

    for eachrow in firstWorksheet.rows:
        row = [cell.value for cell in eachrow]
        outputCsvFile.writerow(row)

def check_delivery_request(serial, color, supply_order_array):

	for item in supply_order_array:
		if serial in item:
			return True

	return False

def main():

	consumable_levels_array = convert_excel_to_csv('consumable_levels.xlsx', 'consumable_levels.csv')
	supply_order_array = convert_excel_to_csv('supply_order_history.xlsx', 'supply_order_history.csv')
	black_matches_array = []
	cyan_matches_array = []
	magenta_matches_array = []
	yellow_matches_array = []

	for i in consumable_levels_array:

		serial = i[8]
		black_level = i[10]
		cyan_level = i[11]
		magenta_level = i[12]
		yellow_level = i[13]

		if black_level <= 10:
			if check_delivery_request(serial, 'black', supply_order_array):
				black_matches_array.append([serial, 'black'])
		elif cyan_level <= 10:
			if check_delivery_request(serial, 'cyan', supply_order_array):
				cyan_matches_array.append([serial, 'cyan'])
		elif magenta_level <= 10:
			if check_delivery_request(serial, 'magenta', supply_order_array):
				magenta_matches_array.append([serial, 'magenta'])
		elif yellow_level <= 10:
			if check_delivery_request(serial, 'yellow', supply_order_array):
				yellow_matches_array.append([serial, 'yellow'])

		if not check_delivery_request:
			make_consumable_request()