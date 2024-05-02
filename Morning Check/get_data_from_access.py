import pyodbc

def get_data_from_access():

    conn = pyodbc.connect(
        r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\clsoportehp\OneDrive - Enel Spa\Respaldo\inventario.accdb;'
    )

    cursor = conn.cursor()
    cursor.execute('''
        select Serial, Etiqueta, Modelo, [Dirección IP], [Host Name], [MAC Address], 
        Site, Grid, [Device Status] from [Inventario Completo]
        ''')
    rows = cursor.fetchall()
    return rows

rows = get_data_from_access()
print(rows[0])