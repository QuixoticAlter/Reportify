# This scripts clears all data of tables RemovedMachine, SupplyOrder, ConsumableLevel and OrderToCreate

from database import RemovedMachine, SupplyOrder, ConsumableLevel, OrderToCreate

rms = RemovedMachine.select()
for rm in rms: rm.delete_instance()

sords = SupplyOrder().select()
for s in sords: s.delete_instance()

cls = ConsumableLevel.select()
for cl in cls: cl.delete_instance()

otcs = OrderToCreate.select()
for otc in otcs: otc.delete_instance()