# This scripts clears all rows of table 'removed_machines'

from database import RemovedMachine, SupplyOrder, ConsumableLevel

rms = RemovedMachine.select()
for rm in rms: rm.delete_instance()

sords = SupplyOrder().select()
for s in sords: s.delete_instance()

cls = ConsumableLevel.select()
for cl in cls: cl.delete_instance()