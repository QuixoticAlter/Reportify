import selenium
import requests
from requests.exceptions import ConnectTimeout, SSLError

from IPs import Ips

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from selenium.common.exceptions import WebDriverException

from time import sleep

def solution_is_installed(ip):

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--window-size=1960,1600")
    chrome_options.add_argument('log-level=3')
        
    driver = webdriver.Chrome(options=chrome_options)

    try:

        driver.get("https://%s" % (ip))

        # more_details = WebDriverWait(driver, 60).until(
        #     EC.presence_of_element_located((By.ID, "details-button")))
        # more_details.click()
        
        # proceed_link = WebDriverWait(driver, 60).until(
        #     EC.presence_of_element_located((By.ID, "proceed-link")))
        # proceed_link.click()

        login = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.ID, "EwsLogin")))
        login.click()

        password = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.ID, "PasswordTextBox")))
        password.send_keys("I10veR0ckNR011!!")

        submit = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.ID, "signInOk")))
        submit.click()

        general_menu_option = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.ID, "SettingsPages")))
        general_menu_option.click()

        solutions_installer_menu_option = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.ID, "SolutionInstaller")))
        solutions_installer_menu_option.click()

    except Exception as e:

        if type(e) == selenium.common.exceptions.WebDriverException:
            print(e)
            return None

    try:
        solutions_installed_div = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.ID, "SolutionsTable")))
        
        print("Solution installed")
        return True

    except:
        print("No solution")

    driver.close()

    return False

def check_solution():

    no_celiveo_array = []

    for ip in Ips:

        print("\n\n-------------------------------------------------------------")
        print("IP: %s" % str(ip))

        try:
            r = requests.get("https://%s" % (ip))
        except Exception as e:
            print(type(e))
            if type(e) == requests.exceptions.SSLError:
                pass
            elif type(e) == requests.exceptions.ConnectTimeout:
                continue
            elif type(e) == requests.exceptions.ConnectionError:
                continue

        if not solution_is_installed(ip): no_celiveo_array.append(ip)

    with open('no_celiveo_ips.txt', "w") as f:
        f.write('\n'.join(no_celiveo_array))

check_solution()