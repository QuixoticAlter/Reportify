import requests
from urllib3.exceptions import InsecureRequestWarning
from adapter import SSLAdapter

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

ip = "10.115.132.21"
url = "https://%s/hp/device/InternalPages/Index?id=ConfigurationPage" % ip

try:
    r = requests.get(url, verify=False)
except:
    s = requests.Session()
    s.mount('https://', SSLAdapter())
    r = s.get(url, verify=False)

if "Celiveo Enabled" in r.text:
    print("Celiveo Found!")

if "Registro" in r.text:
    print("No EWS!!!")

with open("test.html", 'w', encoding="utf-8") as f:
    f.write(r.text)