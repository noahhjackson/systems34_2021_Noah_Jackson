import tkinter
from tkinter import *

top = tkinter.Tk()
width_window, height_window = top.winfo_screenwidth(), top.winfo_screenheight()

C = tkinter.Canvas(top, bg="black", cursor="circle", height=height_window, width=width_window)


def ellipse(h, k, a, b):
    x1 = h-a
    x2 = h+a
    y1 = k+b
    y2 = k-b

    return x1, y1, x2, y2


arc = C.create_oval(ellipse(width_window/2, height_window/2, 500, 300), fill="red")
arc_filling = C.create_oval(ellipse(width_window/2, height_window/2, 495, 295), fill="black")

C.pack(fill="both", expand=True)
top.mainloop()