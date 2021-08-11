import tkinter
from tkinter import *

# https://www.tutorialspoint.com/python/tk_canvas.htm

top = tkinter.Tk()
width_window, height_window = 1024, 576

C = tkinter.Canvas(top, bg="black", height=height_window, width=width_window)


def rectangle(h, k, a, b, thickness, outline, colour):
    x1 = h-a
    x2 = h+a
    y1 = k+b
    y2 = k-b

    x1_filling = h-a+thickness
    x2_filling = h+a-thickness
    y1_filling = k+b-thickness
    y2_filling = k-b+thickness

    if colour == "red":
        C.create_rectangle(x1, y1, x2, y2, fill="red")

    if colour == "blue":
        C.create_rectangle(x1, y1, x2, y2, fill="blue")

    if outline == 1:
        C.create_rectangle(x1_filling, y1_filling, x2_filling, y2_filling, fill="black")

def locator(x, y):
    rectangle(x, y, 20, 20, 0, 0, "red")


rectangle(width_window/2, height_window/2, 500*0.7, 300*0.7, 5, 1, "blue")
rectangle(width_window/2, height_window/2-167.5, 200*0.7, 60*0.7, 5, 1, "blue")

locator(165, 80)
locator(165, 80+200)
locator(165, 80+415)

locator(510, 80)
locator(510, 160)
locator(510, 80+415)

locator(860, 80)
locator(860, 80+200)
locator(860, 80+415)

C.pack(fill="both", expand=True)
top.mainloop()
