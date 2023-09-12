import requests
from urllib3.exceptions import InsecureRequestWarning
from adapter import SSLAdapter

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

ip = "10.115.31.88"
url = "https://%s/hp/device/InternalPages/Index?id=ConfigurationPage" % ip

try:
    r = requests.get(url, verify=False)
except:
    s = requests.Session()
    s.mount('https://', SSLAdapter())
    r = s.get(url, verify=False)

if "Celiveo Enabled" in r.text:
    print("Celiveo Found!")

if r.text == "":
    print("Blank!")

print(type(r.text))
print(len(r.text))

with open("test.html", 'w', encoding="utf-8") as f:
    f.write(r.text)