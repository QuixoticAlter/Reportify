from pypdf import PdfReader

reader = PdfReader("example.pdf")
text = ""
for page in reader.pages:
    text += page.extract_text()

text_array = text.splitlines()
consumable_line = [x for x in text_array if "Páginas restantes aproximadas" in x][0]
print(consumable_line)