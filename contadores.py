import csv

def convert_excel_to_csv(input_file, output_file):

	newWorkbook = openpyxl.load_workbook(input_file)
	firstWorksheet = newWorkbook.active
	outputCsvFile = csv.writer(open(output_file, "w", encoding='utf-8'), delimiter=",")

	for eachrow in firstWorksheet.rows:
	    row = [cell.value for cell in eachrow]
	    outputCsvFile.writerow(row)

def set_inventory_array():

    inventory_array_pre = []

    with open('inventario.csv', encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            inventory_array_pre.append(row)

    inventory_array = [list(map(lambda a:a.strip(), x))[0:20] for x in inventory_array_pre if isinstance(x, list) and x != []]

    with open('inventory_array.txt', 'w') as inventory_file:
        for x in inventory_array:
            inventory_file.write('%s\n' % str(x))

    # print('length of inventory array: %s' % str(len(inventory_array)))
    # print('1th element of inventory: %s' % str(inventory_array[0]))
    # print('Lenght of 1th element of inventory: %s' % str(len(inventory_array[0])))

    return inventory_array

def main():

	