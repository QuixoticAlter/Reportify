# Author: Pablo Godoy
# Corporate Mail: pablogodoy@manpowerchile.cl
# Personal Mail (Bussines Inquiries): sandman-ice@proton.me
# Position: OSA FASA (Chile)

# Instructions:
# 1. Download the FASA MDA HelDesk report
# 2. Put the MDA report in the Documents\Reportes folder
# 3. Check if there is another excel file in the folder. If that is the case, remove it
# 4. Rename the file to "Fasa Chile Informe MDA.xlsx"
# 4. Execute this script through the command python make_mda_report.py

from config import MDA_Report_Route, mda_export_excel, mda_export_csv
from deps.utils import copy_reports, convert_excel_to_csv, get_array_from_csv
from datetime import datetime

import openpyxl
import os
import argparse

def set_formatted_dates(start_date, end_date):

    start_date_string = start_date.replace('-04:00', '')
    start_date_array = start_date_string.split('T')
    # print("Start Date Array: %s" % start_date_array)
    start_date_string_2 = ' '.join(start_date_array)
    # print("Start Date Pre-Formatted: %s" % start_date_string_2)
    start_date_from_string = datetime.strptime(start_date_string_2, "%Y-%m-%d %H:%M:%S")
    start_date_formatted = start_date_from_string.strftime("%d-%m-%Y %H:%M:%S")

    end_date_string = end_date.replace('-04:00', '')
    end_date_array = end_date_string.split('T')
    # print('End Date Array: %s' % end_date_array)
    end_date_string_2 = ' '.join(end_date_array)
    # print("End Date Pre-Formatted: %s" % end_date_string_2)
    end_date_from_string = datetime.strptime(end_date_string_2, "%Y-%m-%d %H:%M:%S")
    end_date_formatted = end_date_from_string.strftime("%d-%m-%Y %H:%M:%S")

    # print("Formatted Start Date: %s" % start_date_formatted)
    # print("Formatted End Date: %s\n" % end_date_formatted)

    return start_date_formatted, end_date_formatted

def make_excel_report(final_mda_array, filename=None):

    wb = openpyxl.Workbook()
    ws1 = wb.create_sheet("Sheet_A", 0)
    ws1.title = "Reporte MDA"
    del wb['Sheet']

    wb.active = wb["Reporte MDA"]
    ws = wb.active

    ws['A1'] = 'Ticket'
    ws['B1'] = 'Título'
    ws['C1'] = 'Estado'
    ws['D1'] = 'SLA'
    ws['E1'] = 'Grupo'
    ws['F1'] = 'Fecha Inicio'
    ws['G1'] = 'Fecha Solución'
    ws['H1'] = 'Usuario Afectado'
    ws['I1'] = 'Tipo'
    ws['J1'] = 'Categorías'

    for i in range(1, len(final_mda_array)):

        # print("Usuario Afectado: %s" % final_mda_array[i-1][7])
        # print(i-1)

        ws['A%s' % str(i+1)] = final_mda_array[i-1][0]
        ws['B%s' % str(i+1)] = final_mda_array[i-1][1]
        ws['C%s' % str(i+1)] = final_mda_array[i-1][2]
        ws['D%s' % str(i+1)] = final_mda_array[i-1][3]
        ws['E%s' % str(i+1)] = final_mda_array[i-1][4]
        ws['F%s' % str(i+1)] = final_mda_array[i-1][5]
        ws['G%s' % str(i+1)] = final_mda_array[i-1][6]
        ws['H%s' % str(i+1)] = final_mda_array[i-1][7]
        ws['I%s' % str(i+1)] = final_mda_array[i-1][8]
        ws['J%s' % str(i+1)] = final_mda_array[i-1][9]

    if filename: 
        filename_ext = filename + '.xlsx'
        report_route = os.path.join('files', filename_ext)
    else:
        filename_ext = 'Reporte MDA.xlsx'
        report_route = os.path.join('files', filename_ext)
        
    wb.save(report_route)

def set_final_mda_report_array(mda_array):

    final_array = []

    for x in mda_array[1:]:

        f_start_date, f_end_date = set_formatted_dates(x[5], x[6])

        ticket = x[0]
        title = x[1]
        status = x[2]
        sla = x[3]
        group = x[4]
        start_date = f_start_date
        end_date = f_end_date
        affected_user = x[7]
        type = x[8]
        category = x[9]

        final_array.append([ticket, title, status, sla, group, start_date, end_date, affected_user, type, category])

    return final_array

def get_mda_report_array(csvfile):

    array = get_array_from_csv(csvfile)
    with open('mda_array.txt', 'w') as f:
        f.write(str(array))

    return array

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        prog='AMRG = Automatic MDA Report Generator',
        description='This program generates a MDA report automatically.'
    )

    parser.add_argument('-n', '--file-name', help='The filename desired for the final report')
    args = parser.parse_args()

    if args.file_name: fname = args.file_name

    # print("Ruta export MDA: %s" % MDA_Report_Route)
    # print("Ruta export MDA copiado: %s" % mda_export_excel)
    # print("Ruta export MDA CSV: %s" % mda_export_csv)

    copy_reports(MDA_Report_Route, mda_export_excel)
    convert_excel_to_csv(mda_export_excel, mda_export_csv)
    mda_report_array = get_mda_report_array(mda_export_csv)
    final_mda_report_array = set_final_mda_report_array(mda_report_array)
    with open('final_mda_report_array.txt', 'w') as f:
        f.write(str(final_mda_report_array))
    make_excel_report(final_mda_report_array, fname)
