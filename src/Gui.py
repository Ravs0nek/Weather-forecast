import tkinter as tk
import os
from PIL import Image, ImageTk

os.chdir(r'C:\Users\milos\OneDrive\Dokumenty\GitHub\Weather-forecast\images')
root = tk.Tk()
root.title('Weather forecast')
root.iconbitmap("icon.ico")
root.geometry('800x600+50+50')
root.resizable(0, 0)
root.columnconfigure(0, weight=2)
root.columnconfigure(1, weight=2)
img = Image.open("weather.png")
smaller_image = img.resize((300,200), Image.ANTIALIAS)
img1 = ImageTk.PhotoImage(smaller_image)
tk.Label(root, image = img1).grid(column=1, row=0, sticky=tk.E, padx = 5,pady = 5)
root.mainloop()






