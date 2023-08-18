# Author: Pablo Godoy (OSA ENEL)
# Dependencias: Python 3.11
# Comando para ejecutar script: python ipchecker.py

import requests
import csv
import subprocess
import openpyxl
# from ips.py import inventory_ips

NRDS_FILE = "NRDS.csv"

def get_NRDS_ips():

	nrds_ips = []
	
	with open(NRDS_FILE, encoding="utf-8") as csvfile:
		spamreader = csv.reader(csvfile, delimiter=';')
		for row in spamreader:
			if row[2] == 'ENEL Global MS' and row[16] == 'Automatic':
				nrds_ips.append(row[17])

	return nrds_ips

def get_NRDS_conectivity(nrds_ips):

	ips_no_conectivity = []
	ips_conectivity = []
	ips_intermitency = []

	for i in nrds_ips:
		# print('\n%s' % str(i))
		proc = subprocess.run('ping -t -n 10 %s' % i, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		output = proc.stdout.decode('latin-1')
		# print(output)
		perdidos_index = output.index("perdidos =")
		n_paquetes_perdidos = int(output[perdidos_index+11:perdidos_index+13])
		# print('n° de paquetes perdidos: %s' % n_paquetes_perdidos)

		if n_paquetes_perdidos == 0:
			ips_conectivity.append(i)
		elif n_paquetes_perdidos == 10:
			ips_no_conectivity.append(i)
		else:
			ips_intermitency.append(i)

	return [ips_conectivity, ips_no_conectivity, ips_intermitency]

def get_export_to_excel(ips_connectivity, ips_no_conectivity, ips_intermitency):

	wb = openpyxl.Workbook()
	ws = wb.active
	ws.title = 'ips con conectividad'

	for i in range(1, len(rows)):
		ws['A%s' % str(i+1)] = rows[i-1][0]
		ws['B%s' % str(i+1)] = rows[i-1][1]
		ws['C%s' % str(i+1)] = rows[i-1][2]
		ws['D%s' % str(i+1)] = rows[i-1][3]
		ws['E%s' % str(i+1)] = rows[i-1][4]
		ws['F%s' % str(i+1)] = rows[i-1][5]
		ws['G%s' % str(i+1)] = rows[i-1][6]
		ws['H%s' % str(i+1)] = rows[i-1][7]
		ws['I%s' % str(i+1)] = rows[i-1][8]
		ws['J%s' % str(i+1)] = rows[i-1][9]
		ws['K%s' % str(i+1)] = rows[i-1][10]
		ws['L%s' % str(i+1)] = rows[i-1][11]
		ws['M%s' % str(i+1)] = rows[i-1][12]
		ws['N%s' % str(i+1)] = rows[i-1][13]
		ws['O%s' % str(i+1)] = rows[i-1][14]
		ws['P%s' % str(i+1)] = rows[i-1][15]
		ws['Q%s' % str(i+1)] = rows[i-1][16]
		ws['R%s' % str(i+1)] = rows[i-1][17]

nrds_ips = get_NRDS_ips()
ips_connectivity, ips_no_conectivity, ips_intermitency = get_NRDS_conectivity(NRDS_IPS)
