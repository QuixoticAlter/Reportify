# Autor: Pablo Godoy
# Correo Corporativo: pablogodoy@manpowerchile.cl
# Correo Personal: sandman-ice@proton.me
# Cargo: OSA ENEL

import csv
import openpyxl
import selenium
import requests
import shutil

from make_consumable_report import set_inventory_array, set_supply_order_array, convert_excel_to_csv, get_data_from_inventory
from sites import province_sites, RM_sites

create_orders_array = []

def copy_reports():

    supply_export_excel = shutil.copy("C:\\Users\\clsoportehp\\Downloads\\ENEL Global MS Consumable Levels.xlsx","Files\\consumable_levels.xlsx")
	
def set_consumable_levels_array():

    consumable_levels_pre = []

    with open('Files\\consumable_levels.csv', encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            consumable_levels_pre.append(row)

    consumable_levels = [list(map(lambda a:a.strip(), x)) for x in consumable_levels_pre[4:] if isinstance(x, list) and x != [] and x[1] == "Chile"]

    with open('Files\\consumable_levels.txt', 'w') as inventory_file:
        for x in consumable_levels:
            inventory_file.write('%s\n' % str(x))

    # print('length of consumable levels array: %s' % str(len(consumable_levels)))
    # print('1th element of consumable leveles: %s' % str(consumable_levels[0]))
    # print('Lenght of 1th element of consumable levels: %s' % str(len(consumable_levels[0])))

    return consumable_levels

def check_delivery_request(serial, color, supply_order_array):

	for item in supply_order_array:
		if serial in item and color in item:
			return None

	return [serial, color]

def is_plotter(serial, inventory_array):

	model = get_data_from_inventory(serial, "Modelo", inventory_array)
	plotter_models = ["HP DesignJet T2600dr 36-in PS MFP", "HP DesignJetT1600 36-in PS Printer"]

	if model in plotter_models: return True

	return False

def get_threshold(site):

	if site in province_sites: return 15
	if site in RM_sites: return 10

def check_plotter_levels(serial, site, supply_orders, c_l, m_l, y_l, g_l, p_b, m_b):

	if c_l and c_l <= get_threshold(site):
		check_delivery_request(serial, 'Cyan', supply_orders)
	elif m_l and m_l <= get_threshold(site):
		check_delivery_request(serial, 'Magenta', supply_orders)
	elif y_l and y_l <= get_threshold(site):
		check_delivery_request(serial, 'Yellow', supply_orders)
	elif g_l and g_l <= get_threshold(site):
		check_delivery_request(serial, 'Gray', supply_orders)
	elif p_b and p_b <= get_threshold(site):
		check_delivery_request(serial, 'Photo Black', supply_orders)
	elif m_b and m_b <= get_threshold(site):
		check_delivery_request(serial, 'Matte Black', supply_orders)

def check_printer_levels(serial, site, supply_orders, b_l, c_l, m_l, y_l):

	if b_l and b_l <= get_threshold(site):
		check_delivery_request(serial, 'black', supply_orders)
	elif c_l and c_l <= get_threshold(site):
		check_delivery_request(serial, 'cyan', supply_orders)
	elif m_l and m_l <= get_threshold(site):
		check_delivery_request(serial, 'magenta', supply_orders)
	elif y_l and y_l <= get_threshold(site):
		check_delivery_request(serial, 'yellow', supply_orders)

def get_supply_order_from_supply_order_array(serial, color, supply_orders, level_date):

	print(serial)

	index_map = {
		"ORDER_ID": 1,
		"CREATE_DT": 2,
		"STATUS": 3,
		"DEV_SERIAL_NO": 4,
		"DEV_MODEL_NO": 5,
		"DEV_MODEL_NAME": 6,
		"ORD_PART_NO": 7,
		"ORD_PART_DESC": 8,
		"COUNTRY": 9,
		"STATUS": 10,
		"SITE": 11
	}

	# print('length of inventory array: %s' % str(len(inventory_array)))
	# print('second element of the array: %s' % str(inventory_array[1]))
	# print('serial: %s' % str(serial))
	# print('key: %s' % str(key))
	# print('field: %s' % str(index_map[key]))

	matches = [x[index_map[key]] for x in supply_orders if x[4] == serial and color in x[8]]
	print('Matches: %s' % str(matches))
	matches = matches[0]

def write_consumable_levels(consumbable_levels_array, create_orders_array, inventory_array, supply_orders):

	wb = openpyxl.Workbook()
	ws = wb.active
	ws.title = 'control suministro'
	print(wb.sheetnames)

	ws['A1'] = 'Fecha de medición'
	ws['B1'] = 'Serial'
	ws['C1'] = 'Modelo'
	ws['D1'] = 'Dirección IP'
	ws['E1'] = 'Nivel de Negro'
	ws['F1'] = 'Nivel de Cyan'
	ws['G1'] = 'Nivel de Magenta'
	ws['H1'] = 'Nivel de Amarillo'
	ws['I1'] = 'Nivel de Gris'
	ws['J1'] = 'Nivel de Negro Fotográfico'
	ws['K1'] = 'Nivel de Negro Matte'
	ws['L1'] = 'Pedido de Negro'
	ws['M1'] = 'Pedido de Cyan'
	ws['N1'] = 'Pedido de Magenta'
	ws['O1'] = 'Pedido de Amarillo'
	ws['P1'] = 'Pedido de Gris'
	ws['Q1'] = 'Pedido de Negro Fotográfico'
	ws['R1'] = 'Pedido de Negro Matte'
	ws['S1'] = 'Comentarios'

	for i in range(1, len(consumbable_levels_array)):
		ws['A%s' % str(i+1)] = consumbable_levels_array[i-1][8]
		ws['B%s' % str(i+1)] = consumbable_levels_array[i-1][9]
		ws['C%s' % str(i+1)] = consumbable_levels_array[i-1][6]
		ws['D%s' % str(i+1)] = get_data_from_inventory[consumbable_levels_array[i-1][8], "Dirección IP", inventory_array]
		ws['E%s' % str(i+1)] = consumbable_levels_array[i-1][10]
		ws['F%s' % str(i+1)] = consumbable_levels_array[i-1][11]
		ws['G%s' % str(i+1)] = consumbable_levels_array[i-1][12]
		ws['H%s' % str(i+1)] = consumbable_levels_array[i-1][13]
		ws['I%s' % str(i+1)] = consumbable_levels_array[i-1][34]
		ws['J%s' % str(i+1)] = consumbable_levels_array[i-1][36]
		ws['K%s' % str(i+1)] = consumbable_levels_array[i-1][37]

		serial = consumbable_levels_array[i-1][8]
		level_date = consumbable_levels_array[i-1][9]

		ws['L%s' % str(i+1)] = get_supply_order_from_supply_order_array(serial, 'Black', supply_orders, level_date)
		ws['M%s' % str(i+1)] = get_supply_order_from_supply_order_array(serial, 'Cyan', supply_orders, level_date)
		ws['N%s' % str(i+1)] = get_supply_order_from_supply_order_array(serial, 'Magenta', supply_orders, level_date)
		ws['O%s' % str(i+1)] = get_supply_order_from_supply_order_array(serial, 'Yellow', supply_orders, level_date)
		ws['P%s' % str(i+1)] = get_supply_order_from_supply_order_array(serial, 'Grey', supply_orders, level_date)
		ws['Q%s' % str(i+1)] = get_supply_order_from_supply_order_array(serial, 'Photo black', supply_orders, level_date)
		ws['R%s' % str(i+1)] = get_supply_order_from_supply_order_array(serial, 'Matte black', supply_orders, level_date)

	wb.save('Niveles de Consumibles.xlsx')

def check_levels():

	copy_reports()
	convert_excel_to_csv('Files\\consumable_levels.xlsx', 'Files\\consumable_levels.csv')
	convert_excel_to_csv('Files\\inventario.xlsx', 'Files\\inventario.csv')
	consumable_levels_array = set_consumable_levels_array()
	inventory_array = set_inventory_array()
	supply_orders = set_supply_order_array()

	create_orders_array = []

	for row in consumable_levels_array:

		print(row[8])
		site = get_data_from_inventory(row[8], 'Site', inventory_array)

		serial = row[8]
		black_level = int(row[10]) if row[10] else None
		cyan_level = int(row[11]) if row[11] else None
		magenta_level = int(row[12]) if row[12] else None
		yellow_level = int(row[13]) if row[13] else None
		grey_level = int(row[34]) if row[34] else None
		photo_black = int(row[36]) if row[36] else None
		matte_black = int(row[37]) if row[37] else None

		if is_plotter(serial, inventory_array): 
			create_orders_array.append(check_plotter_levels(
				serial, site, supply_orders, cyan_level, magenta_level, yellow_level,
				grey_level, photo_black, matte_black
			))
		else:
			create_orders_array.append(check_printer_levels(
				serial, site, supply_orders, black_level, cyan_level, magenta_level, yellow_level
			))

	write_consumable_levels(consumable_levels_array, create_orders_array)

if __name__ == "__main__":

	check_levels()