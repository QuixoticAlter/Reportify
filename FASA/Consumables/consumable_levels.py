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

from database import get_data_from_access
from sites import province_sites, RM_sites, exceptions

create_orders_array = []

def get_supply_order(serial, color, supply_orders, level_date, status):

	matches = [[x[0],x[2]] for x in supply_orders if x[11] == serial and color in x[15]]
	print('Matches: %s' % str(matches))
	max_t_delta = timedelta(days=240)
	match = [
		x for x in matches 
		if dt.strptime(level_date, '%m/%d/%Y %H:%M:%S')-dt.strptime(x[1], '%Y-%m-%d %H:%M:%S') <= max_t_delta
	]

	try:
		print("Best Match %s" % match[0])
		return match[0][0]
	except:
		if status == "Off-Line": return "No Aplica"
		return "Revisar o Crear Orden"

def get_threshold(site):

	print("Site: %s" % site)

	if site in province_sites: return 15
	if site in RM_sites: return 10

def check_levels(serial, site, supply_orders, b_l, c_l, m_l, y_l, g_l, p_b, m_b, level_date, status):

	b_o = None
	c_o = None
	m_o = None
	y_o = None
	g_o = None
	mb_o = None
	pb_o = None

	if b_l != "No Aplica" and b_l <= get_threshold(site):
		b_o = get_supply_order(serial, 'Black', supply_orders, level_date, status)
	elif c_l != "No Aplica" and c_l <= get_threshold(site):
		c_o = get_supply_order(serial, 'Cyan', supply_orders, level_date, status)
	elif m_l != "No Aplica" and m_l <= get_threshold(site):
		m_o = get_supply_order(serial, 'Magenta', supply_orders, level_date, status)
	elif y_l != "No Aplica" and y_l <= get_threshold(site):
		y_o = get_supply_order(serial, 'Yellow', supply_orders, level_date, status)
	elif g_l != "No Aplica" and g_l <= get_threshold(site):
		g_o = get_supply_order(serial, 'Gray', supply_orders, level_date, status)
	elif p_b != "No Aplica" and p_b <= get_threshold(site):
		pb_o = get_supply_order(serial, 'Photo Black', supply_orders, level_date, status)
	elif m_b != "No Aplica" and m_b <= get_threshold(site):
		mb_o = get_supply_order(serial, 'Matte Black', supply_orders, level_date, status)

	return b_o, c_o, m_o, y_o, g_o, mb_o, pb_o

def get_level_value(data):

	if data == 'out': return 0
	try:
		return int(data)
	except:
		return "No Aplica"
	
def generate_levels_report_array(inventory_array, supply_order_array, consumable_levels_array, consumables_web):

	levels_array_report = []

	for row in consumable_levels_array:

		print("Serial: %s" % row[8])

		if row[8] in exceptions: continue

		if not consumables_web:
			serial = row[8]
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
			site = get_data_from_inventory(serial, 'Site', inventory_array)
			status = get_data_from_inventory(serial, 'Device Status', inventory_array)
		else:
			serial = row[8]
			level_date = row[3]
			model = row[2]
			ip_adress = row[1]
			b_l = get_level_value(row[4])
			y_l = get_level_value(row[5])
			m_l = get_level_value(row[6])
			c_l = get_level_value(row[7])
			g_l = get_level_value(row[8])
			m_b = get_level_value(row[9])
			p_b = get_level_value(row[10])
			site = get_data_from_inventory(serial, 'Site', inventory_array)
			status = get_data_from_inventory(serial, 'Device Status', inventory_array)

		b_o, c_o, m_o, y_o, g_o, mb_o, pb_o = check_levels(
			serial, site, supply_order_array, b_l, c_l, m_l, y_l,
			g_l, p_b, m_b, level_date, status
		)

		levels_array_report.append([
			level_date, serial, model, ip_adress, status, b_l, c_l, m_l,
			y_l, g_l, p_b, m_b, b_o, c_o, m_o, y_o, g_o, mb_o, pb_o, ''
		])
	return levels_array_report

def generate_levels_report(levels_array_report):

	wb = openpyxl.load_workbook('files\\Reporte Suministros.xlsx')
	ws1 = wb.create_sheet("Sheet_B", 1)
	ws1.title = 'niveles recientes'

	wb.active = wb['niveles recientes']
	ws = wb.active
	# print(wb.sheetnames)

	ws['A1'] = 'Fecha de medición'
	ws['B1'] = 'Serial'
	ws['C1'] = 'Modelo'
	ws['D1'] = 'Dirección IP'
	ws['E1'] = 'Status'
	ws['F1'] = 'Nivel de Negro'
	ws['G1'] = 'Nivel de Cyan'
	ws['H1'] = 'Nivel de Magenta'
	ws['I1'] = 'Nivel de Amarillo'
	ws['J1'] = 'Nivel de Gris'
	ws['K1'] = 'Nivel de Negro Fotográfico'
	ws['L1'] = 'Nivel de Negro Matte'
	ws['M1'] = 'Pedido de Negro'
	ws['N1'] = 'Pedido de Cyan'
	ws['O1'] = 'Pedido de Magenta'
	ws['P1'] = 'Pedido de Amarillo'
	ws['Q1'] = 'Pedido de Gris'
	ws['R1'] = 'Pedido de Negro Fotográfico'
	ws['S1'] = 'Pedido de Negro Matte'
	ws['T1'] = 'Comentarios'

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
		ws['T%s' % str(i+1)] = levels_array_report[i-1][19]

	wb.save('files\\Reporte Suministros.xlsx')