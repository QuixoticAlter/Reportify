import csv
import requests

url1 = "https://enelcom-my.sharepoint.com/:x:/r/personal/servicioimpresion_hp_chile_enel_com/_layouts/15/Doc.aspx?sourcedoc=%7BC3317384-ACC6-47D6-B76E-2B39D92ACFA7%7D&file=Control%20Suministros.xlsx&action=default&mobileredirect=true"
url2 = "https://enelcom-my.sharepoint.com/:x:/r/personal/servicioimpresion_hp_chile_enel_com/Documents/Reportes/Control%20Suministros.xlsx?d=wc3317384acc647d6b76e2b39d92acfa7&csf=1&web=1&e=dtVezm"

r1 = requests.get(url1)
r2 = requests.get(url2)

open("inventario1.xlsx", "wb").write(r1.content)
open("inventario2.xlsx", "wb").write(r2.content)