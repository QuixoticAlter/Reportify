import tkinter as tk
from tkcalendar import DateEntry

root = tk.Tk()
root.title("Reportify")

label = tk.Label(root, text="Fecha de inicio (DD-MM-YYYY):")
label.pack()

entry = tk.Entry(root)
entry.pack()

cal = DateEntry(root, width=12, background='blue', foreground='white', borderwidht=2)
cal.pack(padx=10, pady=10)

root.geometry("640x480+200-1100")

root.mainloop()