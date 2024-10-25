# This script check the NRDs and cateogrize them. 
# It takes the NRDS in the database and test conectivity
# Also compares serials registered in DCC and the ones installed
# It generates a lis

from database import NRD, MachineChange
from conectivity import ping_80_port
from machine_changes import machine_changed

def review_NRDs():

    connection_nrds = []
    no_connection_nrds = []
    machine_changed_nrds = []
    unknown_reason_nrds = []

    nrds = NRD.select()
    for nrd in nrds:
        if ping_80_port(nrd.machine_associated.ip_addr): 
            connection_nrds.append(nrd)
            nrd.has_conectivity = True
            nrd.save()
        else: 
            no_connection_nrds.append(nrd)
            nrd.has_conectivity = False
            nrd.save()

    for nrd in connection_nrds:
        if machine_changed(nrd.machine_associated): 
            machine_changed_nrds.append(nrd)
            nrd.is_machine_change = True
            nrd.save()
        else: 
            unknown_reason_nrds.append(nrd)
            nrd.is_unknown_reason = True
            nrd.save()

    # with open("machines_changed.txt") as f:
    #     f.write()

def make_nrd_report():

    nrds = NRD.select()
    
    machine_changed_nrds = [MachineChange.get(MachineChange.old_serial == nrd.machine_associated.serial) for nrd in nrds if nrd.is_machine_change]
    machine_changes = ["%s %s" % (mc.old_serial, mc.new_serial) for mc in machine_changed_nrds]
    with open('machine_changes.txt', 'w') as f: f.write('\n'.join(machine_changes))

    no_conectivity_machines = [MachineChange.get(MachineChange.)]

if __name__ == "__main__":

    review_NRDs()
    make_nrd_report()