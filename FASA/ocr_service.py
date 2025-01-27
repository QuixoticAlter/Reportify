import pytesseract
from pdf2image import convert_from_path
import os

pdf_path ='pdf_files/local_728.pdf'
pages = convert_from_path(pdf_path, 500)

for pageNum,imgBlob in enumerate(pages):
    text = pytesseract.image_to_string(imgBlob,lang='spa')
    with open('test.txt', 'a') as the_file:
            the_file.write(text)