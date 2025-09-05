from database import Machine
import csv

machines = Machine.select()

fields = [(m.serial, m.model, m.sku, m.ip_addr, m.site.name, m.site.physical_address, m.site.city, m.pin, m.status, m.collection_method) for m in machines]

with open('db_export.csv', 'w', newline='', encoding='utf-8') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter='|', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerows(fields)