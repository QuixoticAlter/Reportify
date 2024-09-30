
import socket
from database import Machine

def ping_80_port(ip_addr):

    try:
        socket.setdefaulttimeout(10)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip_addr, 80))
    except OSError as error:
        return False
    else:
        s.close()
        return True

def get_conectivity():

    machines_connection = []
    machines_no_connection = []

    machines = Machine.select()
    for m in machines:
        if ping_80_port(m.ip_addr): machines_connection.append(m)
        else: machines_no_connection.append(m)

    return machines_connection, machines_no_connection

if __name__ == "__main__":

    machines_connection, machines_no_connection = get_conectivity()

    with open('machines_no_connectivity.txt') as f:
        f.write('\n'.join(machines_no_connection))

    with open('machines_connectivity.txt') as f:
        f.write('\n'.join(machines_connection))