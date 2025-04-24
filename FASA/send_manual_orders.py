# This script checks for pending manual orders to create (ARC Orders).
# It checks for supplies part numbers and and fill the form file (excel file) automatically

import smtplib
from database import Machine, OrderToCreate

def get_manual_pending_orders_to_create():

    potc = OrderToCreate.select().where(OrderToCreate.pending_of_creation == True)
    mpotc = [order for order in potc if potc.machine.no_dcc]

def send_manual_arc_order_email():

    