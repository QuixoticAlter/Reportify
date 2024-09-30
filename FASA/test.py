from playwright.sync_api import sync_playwright

with sync_playwright() as pw:
    browser = pw.chromium.launch()
    page = browser.new_page()
    page.goto("https://python.org")
    download_link = page.locator("xpath=//div[@class='small-widget download-widget']/p/a")
    print(download_link.inner_text())