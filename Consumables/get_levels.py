
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from models import monochrome, plotters

import requests
import re
import traceback

from datetime import datetime

def get_consumable_levels(inventory_array):

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--window-size=1960,1600")
    chrome_options.add_argument('log-level=3')
        
    driver = webdriver.Chrome(options=chrome_options)

    for row in inventory_array[1:]:

        consumable_levels_array = []

        serial = row[0]
        ip = row[4]
        model = row[3]

        print("Serial: %s" % serial)
        print("Ip Address: %s" % ip)
        print("Model: %s" % model)

        try:
            r = requests.get("https://%s" % (ip))
        except Exception as e:
            print(type(e))
            if type(e) == requests.exceptions.SSLError:
                pass
            elif type(e) == requests.exceptions.ConnectTimeout:
                print('------------------------------------------------------\n')
                continue
            elif type(e) == requests.exceptions.ConnectionError:
                print('------------------------------------------------------\n')
                continue

        try:

            driver.get("https://%s" % (ip))

            if not model.strip() in plotters:

                black_bar = WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'Black')]/span")))
                black_bar_style = black_bar.get_attribute("style")
                matches = re.search(r'\d+', black_bar_style)
                black_level = matches.group(0)
                
                if not model.strip() in monochrome:

                    yellow_bar = WebDriverWait(driver, 60).until(
                        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'Yellow')]/span")))
                    yellow_bar_style = yellow_bar.get_attribute("style")
                    matches = re.search(r'\d+', yellow_bar_style)
                    yellow_level = matches.group(0)

                    magenta_bar = WebDriverWait(driver, 60).until(
                        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'Magenta')]/span")))
                    magenta_bar_style= magenta_bar.get_attribute("style")
                    matches = re.search(r'\d+', magenta_bar_style)
                    magenta_level = matches.group(0)

                    cyan_bar = WebDriverWait(driver, 60).until(
                        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'Cyan')]/span")))
                    cyan_bar_style = cyan_bar.get_attribute("style")
                    matches = re.search(r'\d+', cyan_bar_style)
                    cyan_level = matches.group(0)
                
                else:

                    yellow_level = None
                    magenta_level = None
                    cyan_level = None

                grey_level = None
                matte_black_level = None
                photo_black_level = None

            else:

                photo_black_bar = WebDriverWait(driver, 60).until(
                        EC.presence_of_element_located((By.XPATH, "//div[@class='hpe-progress-linear photo-black']")))
                photo_black_bar_style = photo_black_bar.get_attribute("style")
                matches = re.search(r'\d+', photo_black_bar_style)
                photo_black_level = matches.group(0)

                grey_bar = WebDriverWait(driver, 60).until(
                        EC.presence_of_element_located((By.XPATH, "//div[@class='hpe-progress-linear gray']")))
                grey_bar_style = grey_bar.get_attribute("style")
                matches = re.search(r'\d+', grey_bar_style)
                grey_level = matches.group(0)

                matte_black_bar = WebDriverWait(driver, 60).until(
                        EC.presence_of_element_located((By.XPATH, "//div[@class='hpe-progress-linear matte-black']")))
                matte_black_style = matte_black_bar.get_attribute("style")
                matches = re.search(r'\d+', matte_black_style)
                matte_black_level = matches.group(0)

                cyan_bar = WebDriverWait(driver, 60).until(
                        EC.presence_of_element_located((By.XPATH, "//div[@class='hpe-progress-linear cyan']")))
                cyan_bar_style = cyan_bar.get_attribute("style")
                matches = re.search(r'\d+', cyan_bar_style)
                cyan_level = matches.group(0)
            
                magenta_bar = WebDriverWait(driver, 60).until(
                        EC.presence_of_element_located((By.XPATH, "//div[@class='hpe-progress-linear magenta']")))
                magenta_bar_style = magenta_bar.get_attribute("style")
                matches = re.search(r'\d+', magenta_bar_style)
                magenta_level = matches.group(0)

                yellow_bar = WebDriverWait(driver, 60).until(
                        EC.presence_of_element_located((By.XPATH, "//div[@class='hpe-progress-linear yellow']")))
                yellow_bar_style = yellow_bar.get_attribute("style")
                matches = re.search(r'\d+', yellow_bar_style)
                yellow_level = matches.group(0)
                
                black_level = None

            print('\n------------------------------------------------')
            print("Black Level: %s" % str(black_level))
            print("Yellow Level: %s" % str(yellow_level))
            print("Magenta Level: %s" % str(magenta_level))
            print("Cyan Level: %s" % str(cyan_level))
            print("Photo Black Level: %s" % str(photo_black_level))
            print("Matte Black Level: %s" % str(matte_black_level))
            print("Grey Level: %s" % str(grey_level))

            measure_date = datetime.now()

            consumable_levels_array.append([
                serial, ip, model, measure_date, black_level, yellow_level, 
                magenta_level, cyan_level, grey_level, matte_black_level,
                photo_black_level
            ])
        
        except Exception as e:

            print("type of selenium exception: %s" % str(type(e)))
            print(traceback.format_exc())
            print('-----------------------------------------------\n')
            continue

        print("----------------------------------------------------\n")