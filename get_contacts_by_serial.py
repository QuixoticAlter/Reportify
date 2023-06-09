import csv
from ordered_serials import serials

contactos = [*range(0,305,1)]

print(contactos)

print(serials[304])

with open('contactos.csv', encoding='utf-8') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=';')
	for row in spamreader:
		for i in range(0, 305):
			if serials[i] == row[0]:
				contactos[i] = (row[0], row[6], row[7], row[8])


with open('orderd_contacts.csv', 'w', newline='') as csvfile:
	spamwriter = csv.writer(csvfile, delimiter=';')	
	for i in range(0, 305):
		spamwriter.writerow((contactos[i][0], contactos[i][1], contactos[i][2], contactos[i][3]))