# This script check the NRDs and cateogrize them. 
# It takes the NRDS in the database and test conectivity
# Also compares serials registered in DCC and the ones installed

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

def take_action():

    nrds = NRD.select()
    machine_changed_nrds = [nrd for nrd in nrds if nrd.is_machine_changed]

if __name__ == "__main__":

    review_NRDs()