import csv
import openpyxl
from datetime import datetime

MDA_excel = "MDA.xlsx"
MDA_csv = "MDA.csv"

def convert_excel_to_csv(input_file, output_file):

    newWorkbook = openpyxl.load_workbook(input_file)
    firstWorksheet = newWorkbook.active
    outputCsvFile = csv.writer(open(output_file, "w", encoding='utf-8'), delimiter=",")

    for eachrow in firstWorksheet.rows:
        row = [cell.value for cell in eachrow]
        outputCsvFile.writerow(row)

    return output_file

def get_incidents_array(input_csv):

    inventory_array_pre = []

    with open(input_csv, encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            inventory_array_pre.append(row)

    inventory_array = [x for x in inventory_array_pre if x != []]

    return inventory_array

def main():

	csv_file = convert_excel_to_csv(MDA_excel, MDA_csv)
	inventory_array = get_incidents_array(csv_file)

	for i in range(0, len(inventory_array) - 1):

		if i >= 1:

			fecha_inicial = datetime.strptime(inventory_array[i][5], '%Y-%m-%d %H:%M:%S')
			fecha_final = datetime.strptime(inventory_array[i][6], '%Y-%m-%d %H:%M:%S')

			time_delta = fecha_final - fecha_inicial
			inventory_array[i][4] = time_delta.seconds

	with open(""):

main()