
import csv
from config import *
from database import *

machines = Machine().select()
machines_serials = [x.serial for x in machines]

inventory_array = []

with open(inventory_csv, encoding='latin-1') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for row in spamreader:
        inventory_array.append(row)

inventory_array_post = [x for x in inventory_array if x != []]
inventory_serials = [x[0] for x in inventory_array_post]

unmatched_serials = [x for x in inventory_serials if x not in machines_serials]

for x in unmatched_serials:
    m = Machine.get(Machine.serial == x.serial)
    m.delete()