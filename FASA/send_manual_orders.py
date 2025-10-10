# This script checks for pending manual orders to create (ARC Orders).
# It checks for supplies part numbers and and fill the form file (excel file) automatically

import smtplib
from database import Machine, OrderToCreate

def get_manual_pending_orders_to_create():

    potc = OrderToCreate.select().where(OrderToCreate.pending_of_creation == True)
    mpotc = [order for order in potc if potc.machine.no_dcc]

def create_arc_form(serial, model, sku_array):

    total_array_9130 = [
        ("4S6X9PL", "HP 938E CYAN ORIGINAL INK CARTRIDGE"),
        4S6Y0PL,
        4S6Y1PL,
        4S6Y2PL
    ]

def send_manual_arc_order_email():

