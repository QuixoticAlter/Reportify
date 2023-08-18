from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from time import sleep

import requests

def download_consumable_report():

    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument('log-level=3')

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://dcc.ext.hp.com/")

    login = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, "//button[@ng-click='login.hpidLogin()']")))
    login.click()

    username = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, 'username')))
    username.clear()
    username.send_keys('pablogodoy@manpowerchile.cl')

    next = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, 'user-name-form-submit')))
    next.click()

    pasword = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, "password")))
    pasword.send_keys("Desierto312!")

    order_input = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, 'sign-in')))
    order_input.click()

    input_buscar_pedido = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, 'contenido_btnVerPedidos')))
    input_buscar_pedido.click()

    try:
        n_guide = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, '//table[@class="table table-hover"]/tbody/tr[2]/td[60]/a')))
        n_guide_text = n_guide.text
        n_guide_link = n_guide.get_attribute('href')

        r = requests.get(n_guide_link, allow_redirects=True)
        open('delivery_guides/%s.jpg' % n_guide_text, 'wb').write(r.content)

        driver.close()

        return n_guide_text

    except Exception as e:

        print(e)
        return None
    
if __name__ == "__main__":
    download_consumable_report()