from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from PIL import Image
import numpy as np

from time import sleep

def get_control_snapshot_screenshot(ip):

    # Control Panel snapshot url
    url = "https://%s/hp/device/ControlPanelSnapshot/Index" % ip

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--window-size=1960,1600")
    chrome_options.add_argument('log-level=3')

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    img = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, 'ControlPanelSnapshotImage'))
    )

    coordinates = img.rect
    x = coordinates['x']
    y = coordinates['y']
    width = coordinates['width']
    height = coordinates['height']

    img.screenshot('./control_panel_snapshot.png')

def is_corporative_logo(image):

    im = Image.open('./control_panel_snapshot.png')
    pixel_list = list(im.getdata())
    print(pixel_list[1])
    n_white_pixels = pixel_list.count((255, 255, 255 , 255))
    n_pixels = len(pixel_list)
    white_pixels_ratio = n_white_pixels/n_pixels
    print('White Pixels Ratio: %s' % white_pixels_ratio)
    with open('img_data.txt', 'w') as f:
        f.write(str(pixel_list))

get_control_snapshot_screenshot('10.112.194.178')
is_corporative_logo('./control_panel_snapshot.png')