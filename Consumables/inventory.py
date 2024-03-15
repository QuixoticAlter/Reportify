from sites import exceptions

def get_data_from_inventory(serial, key, inventory_array):

    print(serial)

    index_map = {
        'Serial': 0,
        'Etiqueta': 1,
        'SKU': 2,
        'Modelo': 3,
        'Dirección IP': 4,
        'Host Name': 5,
        'MAC Adress': 6,
        'Site': 7,
        'Building': 8,
        'Coordenadas': 9,
        'Level': 10,
        'Referencia en el piso': 11,
        'Punto de red': 12,
        'Grid': 13,
        'Device Status': 14,
        'Contacto': 15,
        'Teléfono': 16,
        'Correo': 17,
        'Checkeada': 18,
        'En Movimiento': 19,
        'Observaciones': 20
    }

    # print('length of inventory array: %s' % str(len(inventory_array)))
    # print('second element of the array: %s' % str(inventory_array[1]))
    # print('serial: %s' % str(serial))
    # print('key: %s' % str(key))
    # print('field: %s' % str(index_map[key]))

    data_pre = [x[index_map[key]] for x in inventory_array if x[0] == serial and x[0] not in exceptions]
    print('Data Pre: %s' % str(data_pre))
    data = data_pre[0]

    return data