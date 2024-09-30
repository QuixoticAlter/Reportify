# Author: Pablo Godoy
# Position: OSA FASA
# Corporative Mail: pablogodoy@manpowerchile.cl
# Bussines Inquiries: sandman-ice@proton.me

# This program takes the Service Visit History Report and makes a data cross with a helpdesk report.
# It generates a report which shows DCC service request case number along with the related helpdesk case number.
# It automatically takes the description of each case and put it on the report.

# Instructions

# Download the Service Request History Report from DCC. Move this report to the folder C:\Users\HP\Documents\Reportes
# Download the Helpdesk Report from the client helpdesk system. Move this report to the folder C:\Users\HP\Documents\Reportes
# Execute this program with the command python case_traking.py
# Enjoy it!

import openpyxl
import csv

if __name__ == "__main__":

    