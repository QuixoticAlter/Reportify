import csv
from datetime import datetime

def convert_csvfile_to_array(csvfile):

    array = []
    with open('Files\Reporte Suministros Histórico.csv', newline='', encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=";")
        for row in spamreader:
            array.append(row)

    # print(array)
    return array

def process_array(array):

    proc_array = [[
        datetime.strptime(x[0].strip(), "%d/%m/%Y"),
        x[1], x[2], x[3], x[4], x[5], x[6], x[7],
        x[8], x[9], x[10], x[11], x[12], x[13]]
        for x in array]
    
    return proc_array

def get_date(row):
    return row

if __name__ == "__main__":

    array = convert_csvfile_to_array("Files\\Reporte Suministros Histórico.csv")
    proc_array = process_array(array[1:])
    # print(proc_array[0])
    # print(type(proc_array[0]))
    ordered_array = sorted(proc_array)
    print(ordered_array[0])
    print(ordered_array[-1])
    print(type(ordered_array[0]))
    formatted_ordered_array = [[
        x[0].strftime("%d/%m/%Y"), x[1], x[2], x[3],
        x[4], x[5], x[6], x[7], x[8], x[9], x[10],
        x[11], x[12], x[13]]
        for x in ordered_array]
    with open("Files\\Reporte Suministros Históricos Ordenado.csv", 'w', encoding="utf-8", newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=";")
        spamwriter.writerows(formatted_ordered_array)
    # print(ordered_array)