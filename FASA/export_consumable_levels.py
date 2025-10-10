from database import *
from datetime import datetime, timedelta

cls = ConsumableLevel.select().where(ConsumableLevel.detection_date >= datetime.now() - timedelta(days=5))

final_array = []

for cl in cls:
    final_array.append((
        cl.machine.serial, cl.machine.site.name, cl.machine.site.physical_address, cl.machine.site.city, 
        cl.cyan_level, cl.magenta_level, cl.yellow_level, cl.black_level
    ))

with open("consumble_levels.txt", "w", encoding="Utf-8") as f:

    for cl in final_array: f.write("%s|%s|%s|%s|%s|%s|%s|%s\n" % (cl[0], cl[1], cl[2], cl[3], cl[4], cl[5], cl[6], cl[7]))