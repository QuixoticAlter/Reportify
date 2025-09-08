import requests
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

url = "https://10.237.59.21/supplies/cartridges"

chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--ignore-certificate-errors")
# chrome_options.add_argument("--window-size=1960,1600")
chrome_options.add_argument('log-level=3')

driver = webdriver.Chrome(options=chrome_options)

driver.get(url)

input_pin = WebDriverWait(driver, 120).until(
    EC.presence_of_element_located((By.ID, 'pin'))    
)
input_pin.send_keys('13274311')

try: 
    register_button = WebDriverWait(driver, 120).until(
        EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "Registro")]'))
    )
    register_button.click()
except:
    register_button = WebDriverWait(driver, 120).until(
        EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "Sign In")]'))
    )
    register_button.click()

widgets = WebDriverWait(driver, 120).until(
    EC.visibility_of_all_elements_located((By.XPATH, '//mat-list-item[contains(@class, "ng-tns-c104")]'))
)

for widget in widgets:
    widget.click()
    print(widget.get_attribute("class"))

sleep(100000)