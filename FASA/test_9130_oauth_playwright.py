import requests
from time import sleep
import re
from playwright.sync_api import sync_playwright

ip_addr = "https://10.237.59.21/supplies/cartridges"
oauth_url = "https://%s/cdm/oauth2/v1/token" % ip_addr
pin = 13274311

def handle_response(response):
     
    if (response.request.resource_type == "xhr" or response.request.resource_type == "fetch") and "/cdm/oauth2/v1/token" in response.request.url:
        print(f"XHR/Fetch Response URL: {response.url}")
        text = response.json()
        response.request.access_token = text['access_token']

    else: response.request.access_token = None

with sync_playwright() as pw:
        
        browser = pw.chromium.launch(headless=False)
        page = browser.new_page(ignore_https_errors=True)

        response = page.goto("%s" % ip_addr)

        pin_input = page.locator('//input[@id="pin"]')
        pin_input.wait_for(timeout=20000)
        pin_input.type("%s" % pin)

        try: 
            register_button = page.locator('//span[contains(text(), "Registro")]')
            register_button.wait_for(timeout=20000)
            register_button.click()
        except:
            register_button = page.locator('//span[contains(text(), "Sign In")]')
            register_button.wait_for(timeout=20000)
            register_button.click()

        sleep(1)
        spans = page.locator('//span[contains(@class, "mat-content ng-tns-c104")]')
        for i in range(1, 5): 
            print(spans.nth(i))
            class_name = spans.nth(i).get_attribute('class')
            print(class_name)
            span_c = page.locator('//span[@class="%s"]' % class_name)
            span_c.wait_for(timeout=2000)
            span_c.click()

        sleep(10)

        cyan_approx_pages = page.locator('//div[@id="approxPagesRemaining_C"]')
        cyan_approx_pages.wait_for(timeout=20000)
        cyan_approx_pages_text = cyan_approx_pages.inner_text()

        magenta_approx_pages = page.locator('//div[@id="approxPagesRemaining_M"]')
        magenta_approx_pages.wait_for(timeout=20000)
        magenta_approx_pages_text = magenta_approx_pages.inner_text()

        yellow_approx_pages = page.locator('//div[@id="approxPagesRemaining_Y"]')
        yellow_approx_pages.wait_for(timeout=20000)
        yellow_approx_pages_text = yellow_approx_pages.inner_text()

        black_approx_pages = page.locator('//div[@id="approxPagesRemaining_K"]')
        black_approx_pages.wait_for(timeout=20000)
        black_approx_pages_text = black_approx_pages.inner_text()

        print(cyan_approx_pages_text, magenta_approx_pages_text, yellow_approx_pages_text, black_approx_pages_text)

        black_approx_pages_text_filt = re.findall(r"\d+", black_approx_pages_text)[0]
        magenta_approx_pages_text_filt = re.findall(r"\d+",magenta_approx_pages_text)[0]
        cyan_approx_pages_text_filt = re.findall(r"\d+", cyan_approx_pages_text)[0]
        yellow_approx_pages_text_filt = re.findall(r"\d+", yellow_approx_pages_text)[0]

        black_approx_pages_int = int(black_approx_pages_text_filt)
        magenta_approx_pages_int = int(magenta_approx_pages_text_filt)
        cyan_approx_pages_int = int(cyan_approx_pages_text_filt)
        yellow_approx_pages_int = int(yellow_approx_pages_text_filt)

        print(black_approx_pages_int, magenta_approx_pages_int, cyan_approx_pages_int, yellow_approx_pages_int)