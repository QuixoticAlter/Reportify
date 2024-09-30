
from datetime import datetime

from database import Machine, MachineChange, ChannelCase, HelpDeskCase
from playwright.sync_api import sync_playwright

def machine_changed(m):

    print("Checking IP %s" % m.ip_addr)

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(ignore_https_errors=True)
        try:
            page.goto("https://%s/#hId-pgDevInfo" % m.ip_addr)
            serial_element = page.locator("xpath=//table[@id='appDevInfo-printerInfo-tbl-Tbl']/tbody/tr[3]/td[2]")
            serial_element.wait_for(timeout=120000)
            serial_installed = serial_element.inner_text()
            browser.close()
        except Exception as e:
            print(e)
            serial_installed = None
            browser.close()

        if serial_installed != None:
            print(serial_installed)
            if serial_installed != m.serial:
                print("Serial installed different from serial registered!")
                rows = MachineChange.select().where(MachineChange.old_serial == m.serial and MachineChange.new_serial == serial_installed) 
                if len(rows) == 0: 
                    machine_change = MachineChange()
                    machine_change.old_serial = m.serial
                    machine_change.new_serial = serial_installed
                    casos_canal = m.channel_cases
                    n_cases = [c.n_case for c in casos_canal]
                    if n_cases != []: machine_change.case_associated = sorted(n_cases)[0]
                    machine_change.site_associated = m.site
                    machine_change.save()
                
                return True
    
    return False

def get_machines_changed():

    machines = Machine.select()
    for m in machines:
        print(m.ip_addr)
        if m.ip_addr != "0.0.0.0" and m.ip_addr != None and m.ip_addr != "":
            machine_changed(m)