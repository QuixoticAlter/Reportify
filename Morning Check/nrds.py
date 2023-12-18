import csv
import openpyxl

def find_serial_on_logfiles(serial, logfile):

    with open(logfile, "r") as f:
        for line in f.readlines():
            if serial in line: return True

def find_serial_on_export(serial, export_file):

    with open(export_file, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            if serial in row:
                return True

def check_nrds(nrd_array, service_requests_csv):

    print("nrd array inside check_nrds: %s" % nrd_array)

    nrd_report_array = []

    for x in nrd_array:

        serial = x[2]
        asset_number = x[11]
        site = x[10]
        last_collection_date = x[4]
        collect_method = x[14]
        ip_address = x[15]
        host_name = x[16]
        asset_status = x[17]
        conectivity = find_serial_on_logfiles(serial, "no_connection_ips.txt") or find_serial_on_logfiles(serial, "no_connection_sslv1.txt")
        ews = find_serial_on_logfiles(serial, "no_web_ips.txt")
        service_request_subk = find_serial_on_export(serial, service_requests_csv)

        nrd_report_array.append([
            serial, asset_number, site, last_collection_date, collect_method, 
            ip_address, host_name, asset_status, conectivity, ews, service_request_subk
        ])

    print("nrd report array: %s" % nrd_report_array)

    return nrd_report_array

def create_nrd_report(rows):

    print(rows)

    wb = openpyxl.Workbook()
    ws1 = wb.create_sheet("Sheet_A", 0)
    ws1.title = 'NRDS Report'

    wb.active = wb["NRDS Report"]
    ws = wb.active

    ws['A1'] = 'Serial Number'
    ws['B1'] = 'Asset Number'
    ws['C1'] = 'Site'
    ws['D1'] = 'Last Collection Date'
    ws['E1'] = 'Collec Method'
    ws['F1'] = 'IP Address'
    ws['G1'] = 'Host Name'
    ws['H1'] = 'Asset Status'
    ws['I1'] = 'Conectividad'
    ws['J1'] = 'EWS'
    ws['K1'] = 'Comentarios'
    ws['L1'] = 'Revisado'

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

    ws0 = wb.get_sheet_by_name('Sheet')
    wb.remove_sheet(ws0)
    wb.save('files\\NRD Report.xlsx')