
import pyautogui
from PIL import ImageGrab
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

def take_screenshot():
    
    st = "icons/screenshot.png"

    screenshot = ImageGrab.grab()
    screenshot.save(st)
    screenshot.close()

    return st

def detetect_icon_and_return_coordinates(icon, st):

    img = cv.imread(icon, cv.IMREAD_GRAYSCALE)
    assert img is not None, "file could not be read, check with os.path.exists()"
    img2 = img.copy()
    template = cv.imread(st, cv.IMREAD_GRAYSCALE)
    assert template is not None, "file could not be read, check with os.path.exists()"
    w, h = img2.shape[::-1]
    print(w, h)
    
    meth = 'TM_CCOEFF_NORMED'

    img = img2.copy()
    method = getattr(cv, meth)

    # Apply template Matching
    res = cv.matchTemplate(img,template,method)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)

    top_left = max_loc
    print(top_left)
    bottom_right = (top_left[0] + w, top_left[1] + h)
    middle_point = (top_left[0] + w/2, top_left[1] + h/2)

    return middle_point

def check_and_select_dcc():

    chrome_icon = 'icons/chrome_icon.PNG'
    hp_favicon = 'icons/hp_favicon.PNG'
    login_interface = 'icons/login_interface.PNG'

    st = take_screenshot()
    chrome_icon_position = detetect_icon_and_return_coordinates(chrome_icon, st)
    pyautogui.click(chrome_icon_position)

    st = take_screenshot()
    hp_favicon_position = detetect_icon_and_return_coordinates(hp_favicon, st)
    pyautogui.click(hp_favicon_position)

    st = take_screenshot()
    login_interface_position = detetect_icon_and_return_coordinates(login_interface, st)
    pyautogui(login_interface_position)

if __name__ == "__main__":
    
    serial = 'TH36TH61VC'
    check_and_select_dcc()