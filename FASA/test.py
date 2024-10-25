# from playwright.sync_api import sync_playwright

# with sync_playwright() as pw:
#     browser = pw.chromium.launch()
#     page = browser.new_page()
#     page.goto("https://python.org")
#     download_link = page.locator("xpath=//div[@class='small-widget download-widget']/p/a")
#     print(download_link.inner_text())

import requests
from adapter import SSLAdapter
from urllib3.exceptions import InsecureRequestWarning

def get_cartridges_install_date(ip):

    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
    # requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += 'AES256-GCM-SHA384'

    url = "https://%s/hp/device/InternalPages/Index?id=ConfigurationPage" % ip
    r = requests.get(url, verify=False, timeout=20)

    # try:
    #     r = requests.get(url, verify=False, timeout=20)
    # except:
    #     try:
    #         s = requests.Session()
    #         s.mount('https://', SSLAdapter())
    #         print("Fetching through SSLv1")
    #         r = s.get(url, verify=False, timeout=5)
    #     except Exception as e:
    #         print(type(e))
    #         if type(e) == requests.exceptions.ConnectionError:
    #             print("Conenction Error!")
    #         elif type(e) == requests.exceptions.ReadTimeout:
    #             print("Read Timeout!")

    #         return "SSLv1 Connection Error"

    print(r.text)
        
if __name__ == "__main__":

    ip = "154.41.1.98"
    ci_date = get_cartridges_install_date(ip)
    # print(ci_date)