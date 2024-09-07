import subprocess
import openpyxl
import csv
import shutil
import os

def copy_reports(source, dest, on_error_message=None):

    try:
        shutil.copy(source, dest)
    except Exception as e:
        if type(e) == FileNotFoundError: 
            if on_error_message: print(on_error_message)

def convert_excel_to_csv(input_file, output_file):

    newWorkbook = openpyxl.load_workbook(input_file)
    firstWorksheet = newWorkbook.active
    outputCsvFile = csv.writer(open(output_file, "w", encoding='utf-8'), delimiter=",")

    for eachrow in firstWorksheet.rows:
        row = [cell.value for cell in eachrow]
        outputCsvFile.writerow(row)

def get_array_from_csv(csvfile):
    
    array_pre = []
    with open(csvfile, encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            array_pre.append(row)

    array = [x for x in array_pre if x != []]

    return array

def has_conectivity(ip_address):

    result = subprocess.run("ping %s" % ip_address, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = result.stdout.decode('latin-1')

    print(type(out))
    print("ping output: %s" % out)

    if "enviados = 4, recibidos = 4" in out: return True

    return False

