import requests
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

ip_addr = "10.237.59.21"
pin = "13274311"

def get_supply_levels_9130(ip_addr, pin):

    url = "https://%s" % ip_addr

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--window-size=1366,768")
    chrome_options.add_argument('log-level=3')

    prefs = {
        "download.default_directory": r"C:\Users\HP\Documents\Programas\Reportify\FASA\files\reports",  # Use a full, absolute path
        "download.prompt_for_download": False,  # Optional: disable the download prompt
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True  # Optional: ensure safe browsing
    }

    chrome_options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    support_tools = WebDriverWait(driver, 120).until(
        EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "Herramientas de soporte")]'))    
    )
    support_tools.click()

    reports_and_pages = WebDriverWait(driver, 120).until(
        EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "Informes y páginas")]'))
    )
    reports_and_pages.click()

    input_pin = WebDriverWait(driver, 120).until(
        EC.presence_of_element_located((By.ID, 'pin'))    
    )
    input_pin.send_keys(pin)

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

    download_tab = WebDriverWait(driver, 120).until(
        EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "Descargar")]'))
    )
    download_tab.click()

    printer_report_status = WebDriverWait(driver, 120).until(
        EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "Informe estado impresora")]'))
    )
    printer_report_status.click()

    download_button = WebDriverWait(driver, 120).until(
        EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "Descargar")]'))
    )
    download_button.click()

    sleep(5)

    accept_button = WebDriverWait(driver, 120).until(
        EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "Aceptar")]'))
    )
    accept_button.click()

    driver.close()

get_supply_levels_9130(ip_addr, pin)