import os

Account_Name = "Fasa Chile"
Threshold = 10
Threshold_10 = 10
exceptional_threshold = 50

sites_high_consume_machines = ['Local 58']
sites_with_no_trigger = [
    'Local 688', 
    'Local 58', 
    'Local 397', 
    'Local 715',
    'TH356F614K',
    'Local 701', 
    'Local 404', 
    'Local 681',
    'Local 679',
    'Local 394',
    'Local 283',
    'Local 482',
    'Local 426',
    'Local 686',
    'Local 387'
]

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
arc_orders_csv = "files\\arc_orders.csv"
automatic_orders_csv = "files\\automatic_orders.csv"
manual_orders_csv = "files\\manual_orders.csv"
inventory_excel = "files\\inventario.xlsx"
inventory_csv = "files\\inventario.csv"
new_machines_csv = "files\\new_machines_not_added_to_dcc.csv"
consumable_levels_export_excel = "files\\consumable_levels.xlsx"
consumable_levels_export_csv = "files\\consumable_levels.csv"
service_requests_export_excel = "files\\service_requests.xlsx"
service_requests_export_csv = "files\\service_requests.csv"
mda_export_excel = "files\\mda_export.xlsx"
mda_export_csv = "files\\mda_export.csv"
nrd_export_excel = "files\\nrd_export.xlsx"
nrd_export_csv = "files\\nrd_export.csv"

city_region_dict =  {
    "Antofagasta": "II",
    "Temuco": "IX",
    "Santiago": "RM",
    "La Serena": "IV",
    "El Bosque": "RM",
    "Calama": "II",
    "La Florida": "RM",
    "Maipú": "RM",
    "Puente Alto": "RM",
    "Valparaíso": "V",
    "San Joaquín": "RM",
    "Coquimbo": "IV",
    "San Miguel": "RM",
    "Rengo": "VI",
    "Viña del Mar": "V",
    "Quilpué": "V",
    "Iquique": "I",
    "Ovalle": "IV",
    "La Reina": "RM",
    "Vitacura": "RM",
    "Puchuncaví": "V",
    "Rancagua": "VI",
    "La Calera": "V",
    "Ñuñoa": "RM",
    "La Ligua": "V",
    "Villa Alemana": "V",
    "Chillán": "XVI",
    "Parral": "VII",
    "Talca": "VII",
    "Osorno": "X",
    "Puerto Aysén": "XI",
    "Talcahuano": "VIII",
    "Puerto Montt": "X",
    "Valdivia": "XIV",
    "Concepción": "VIII",
    "Recoleta": "RM",
    "Los Ángeles": "VIII",
    "Arica": "XV",
    "Castro": "X",
    "Coronel": "VIII",
    "Copiapó": "III",
    "Villarrica": "IX",
    "Los Andes": "V",
    "San Fernando": "VI",
    "Victoria": "IX",
    "San Felipe": "V",
    "Quillota": "V",
    "Vallenar": "III",
    "Conchalí": "RM",
    "Puerto Natales": "XII",
    "Macul": "RM",
    "Linares": "VII",
    "Concón": "V",
    "San Bernardo": "RM",
    "Pudahuel": "RM",
    "Cerrillos": "RM",
    "Melipilla": "RM",
    "Colina": "RM",
    "San Javier": "VII",
    "San Vicente de Tagua Tagua": "VI",
    "Curicó": "VII",
    "Quintero": "V",
    "Providencia": "RM",
    "Las Condes": "RM",
    "San Pedro de la Paz": "VIII",
    "Renca": "RM",
    "Lo Barnechea": "RM",
    "Talagante": "RM",
    "Santa Cruz": "VI",
    "Punta Arenas": "XII",
    "Coyhaique": "XI",
    "Independencia": "RM",
    "Cauquenes": "VII",
    "La Cisterna": "RM",
    "Puerto Varas": "X",
    "Estación Central": "RM",
    "Ancud": "X",
    "San Francisco de Mostazal": "VI",
}
