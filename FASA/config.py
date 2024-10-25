import os

Account_Name = "Fasa Chile"
Threshold = 10
Threshold_10 = 10
exceptional_threshold = 50

high_consume_machines = []

SOH_Report_Name = Account_Name + " Supply Order History.xlsx"
CL_Report_Name = Account_Name + " Consumable Levels.xlsx"
SR_Report_Name = Account_Name + " - Service Visit History.xlsx"
MDA_Report_Name = Account_Name + " Informe MDA.xlsx"
NRD_Report_Name = Account_Name + " NRD Devices.xlsx"

DCC_Reports_Route = "C:\\Users\\HP\\Documents\\Reportes"
Inventory_Route = "C:\\Users\\HP\\Documents\\Inventario Fasa 2024.xlsx"
SOH_Report_Route = os.path.join(DCC_Reports_Route, SOH_Report_Name)
CL_Report_Route = os.path.join(DCC_Reports_Route, CL_Report_Name)
SR_Report_Route = os.path.join(DCC_Reports_Route, SR_Report_Name)
MDA_Report_Route = os.path.join(DCC_Reports_Route, MDA_Report_Name)
NRD_Report_Route = os.path.join(DCC_Reports_Route, NRD_Report_Name)

supply_export_csv = "files\\supply_order_history.csv"
supply_export_excel = "files\\supply_order_history.xlsx"
inventory_excel = "files\\inventario.xlsx"
inventory_csv = "files\\inventario.csv"
consumable_levels_export_excel = "files\\consumable_levels.xlsx"
consumable_levels_export_csv = "files\\consumable_levels.csv"
service_requests_export_excel = "files\\service_requests.xlsx"
service_requests_export_csv = "files\\service_requests.csv"
mda_export_excel = "files\\mda_export.xlsx"
mda_export_csv = "files\\mda_export.csv"
nrd_export_excel = "files\\nrd_export.xlsx"
nrd_export_csv = "files\\nrd_export.csv"