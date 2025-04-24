from flask import Flask
from jinja2 import render_template
from database import Machine, NRD, OrderToCreate, LowLevelMachineRecentOrder

app = Flask(__name__)

def get_low_levels_machines_recent_order():

    low_levels_machines_with_recent_order = LowLevelMachineRecentOrder.select().where(LowLevelMachineRecentOrder.pending_of_verification == True).limit(10)
    return low_levels_machines_with_recent_order

def get_pending_orders_to_create():

    otc = OrderToCreate.select().where(OrderToCreate.pending_of_creation == True).limit(10)
    return otc

@app.route("/")
def main_dashboard():
    machines = Machine.select().limit(10)
    nrds = NRD.select().limit(10)
    pending_orders_to_create = get_pending_orders_to_create()
    return render_template('main_dashboard.jinja2', machines=machines)

if __name__ == "__main__": app.run()