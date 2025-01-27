from database import *

def select_newest_machine(a, b):

    if a > b: return a
    if b > a: return b

machines = Machine().select()
machines_serials = [x.serial for x in machines]

checked_machines = []
duplicated_machines = []

for m in machines_serials:
    if m in checked_machines: duplicated_machines.append(m)
    checked_machines.append(m)

with open('duplicated_machines.txt', 'w') as f:
    for m in duplicated_machines: f.write('%s\n' % (m))

for m in duplicated_machines:
    machines = Machine().select().where(Machine.serial == m)
    if len(machines) >= 2:
        machines_ids = [m.id for m in machines]
        sorted_machine_ids = sorted(machines_ids, reverse=True)
        newest_m = sorted_machine_ids[0]
        print(newest_m)
        Machine().delete_by_id(newest_m)