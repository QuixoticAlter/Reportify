# Autor: Pablo Godoy
# Correo Corporativo: pablogodoy@manpowerchile.cl
# Correo Personal: sandman-ice@proton.me
# Cargo: OSA ENEL

import csv
import openpyxl
import selenium
import requests
import shutil

from datetime import datetime as dt
from datetime import timedelta

from inventory import get_data_from_inventory
from sites import province_sites, RM_sites, exceptions

create_orders_array = []

def get_supply_order(serial, color, supply_orders, level_date):

	matches = [x[0] for x in supply_orders if x[4] == serial and color in x[8]]
	print('Matches: %s' % str(matches))
	max_t_delta = timedelta(days=60)
	match = [
		x for x in matches 
		if dt.strptime(level_date, '%d/%m/%Y %H:%M:%S')-dt.strptime(x[2], '%d/%m/%Y') >= max_t_delta
	]

	print("Best Match %s" % match[0])

	try:
		return match[0]
	except:
		return "Revisar o Crear Orden"

def is_plotter(serial, inventory_array):

	model = get_data_from_inventory(serial, "Modelo", inventory_array)
	plotter_models = ["HP DesignJet T2600dr 36-in PS MFP", "HP DesignJetT1600 36-in PS Printer"]

	if model in plotter_models: return True

	return False

def get_threshold(site):

	print("Site: %s" % site)

	if site in province_sites: return 15
	if site in RM_sites: return 10

def check_levels(serial, site, supply_orders, b_l, c_l, m_l, y_l, g_l, p_b, m_b):

	if b_l and b_l <= get_threshold(site):
		b_o = get_supply_order(serial, 'Black', supply_orders)
	elif c_l and c_l <= get_threshold(site):
		c_o = get_supply_order(serial, 'Cyan', supply_orders)
	elif m_l and m_l <= get_threshold(site):
		m_o = get_supply_order(serial, 'Magenta', supply_orders)
	elif y_l and y_l <= get_threshold(site):
		y_o = get_supply_order(serial, 'Yellow', supply_orders)
	elif g_l and g_l <= get_threshold(site):
		g_o = get_supply_order(serial, 'Gray', supply_orders)
	elif p_b and p_b <= get_threshold(site):
		mb_o = get_supply_order(serial, 'Photo Black', supply_orders)
	elif m_b and m_b <= get_threshold(site):
		pb_o = get_supply_order(serial, 'Matte Black', supply_orders)

	return b_o, b_o, c_o, m_o, y_o, g_o, mb_o, pb_o

def get_level_value(data):

	if data == 'out': return 0
	try:
		return int(data)
	except:
		return None

def generate_levels_report_array(inventory_array, supply_order_array, consumable_levels_array):

	levels_array_report = []

	for row in consumable_levels_array:

		print("Serial: %s" % row[8])

		serial = row[8]
		if serial not in exceptions:
			level_date = row[9]
			model = row[6]
			ip_adress = get_data_from_inventory(serial, "Dirección IP", inventory_array)
			b_l = get_level_value(row[10])
			c_l = get_level_value(row[11])
			m_l = get_level_value(row[12])
			y_l = get_level_value(row[13])
			g_l = get_level_value(row[34])
			p_b = get_level_value(row[36])
			m_b = get_level_value(row[37])
			site = get_data_from_inventory(row[8], 'Site', inventory_array)

			b_o, c_o, m_o, y_o, g_o, mb_o, pb_o = check_levels(
				serial, site, supply_order_array, b_l, c_l, m_l, y_l,
				g_l, p_b, m_b
			)

		levels_array_report.append([
			level_date, serial, model, ip_adress, b_l, c_l, m_l,
			y_l, g_l, p_b, m_b, b_o, c_o, m_o, y_o, g_o, mb_o, pb_o, ''
		])

	return levels_array_report

def generate_levels_report(levels_array_report, wb):

	wb = openpyxl.Workbook('Files\\Reporte Suministros.xlsx')
	wb.active = wb['Sheet_B']
	ws = wb.active
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

	for i in range(1, len(levels_array_report)):
		ws['A%s' % str(i+1)] = levels_array_report[i-1][0]
		ws['B%s' % str(i+1)] = levels_array_report[i-1][1]
		ws['C%s' % str(i+1)] = levels_array_report[i-1][2]
		ws['D%s' % str(i+1)] = levels_array_report[i-1][3]
		ws['E%s' % str(i+1)] = levels_array_report[i-1][4]
		ws['F%s' % str(i+1)] = levels_array_report[i-1][5]
		ws['G%s' % str(i+1)] = levels_array_report[i-1][6]
		ws['H%s' % str(i+1)] = levels_array_report[i-1][7]
		ws['I%s' % str(i+1)] = levels_array_report[i-1][8]
		ws['J%s' % str(i+1)] = levels_array_report[i-1][9]
		ws['K%s' % str(i+1)] = levels_array_report[i-1][10]
		ws['L%s' % str(i+1)] = levels_array_report[i-1][11]
		ws['M%s' % str(i+1)] = levels_array_report[i-1][12]
		ws['N%s' % str(i+1)] = levels_array_report[i-1][13]
		ws['O%s' % str(i+1)] = levels_array_report[i-1][14]
		ws['P%s' % str(i+1)] = levels_array_report[i-1][15]
		ws['Q%s' % str(i+1)] = levels_array_report[i-1][16]
		ws['R%s' % str(i+1)] = levels_array_report[i-1][17]
		ws['S%s' % str(i+1)] = levels_array_report[i-1][18]

	wb.save('Files\\Reporte Suministros.xlsx')