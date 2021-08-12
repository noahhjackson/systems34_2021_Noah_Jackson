import tkinter
from tkinter import *
import time

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

    C.create_rectangle(x1, y1, x2, y2, fill=colour)

    if outline == 1:
        C.create_rectangle(x1_filling, y1_filling, x2_filling, y2_filling, fill="black")


class Locator:
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name
        rectangle(self.x, self.y, 20, 20, 0, 0, "red")
        C.create_text(self.x, self.y, fill="white", font="Times 15 italic bold", text=self.name)

    def detection(self):
        rectangle(self.x, self.y, 20, 20, 0, 0, "green")

        # https://www.codegrepper.com/code-examples/python/display+a+string+in+canvas+python+tkinter
        C.create_text(self.x, self.y, fill="white", font="Times 15 italic bold", text=self.name)

    def un_detection(self):
        rectangle(self.x, self.y, 20, 20, 0, 0, "red")

        # https://www.codegrepper.com/code-examples/python/display+a+string+in+canvas+python+tkinter
        C.create_text(self.x, self.y, fill="white", font="Times 15 italic bold", text=self.name)

def test():
    T1.detection()

def un_test():
    T1.un_detection()


rectangle(width_window/2, height_window/2, 500*0.7, 300*0.7, 5, 1, "blue")
rectangle(width_window/2, height_window/2-167.5, 200*0.7, 60*0.7, 5, 1, "blue")

T6 = Locator(165, 80, "T6")
T5 = Locator(165, 80+200, "T5")
T4 = Locator(165, 80+415, "T4")

T7 = Locator(510, 80, "T7")
T8 = Locator(510, 160, "T8")
T3 = Locator(510, 80+415, "T3")

T9 = Locator(860, 80, "T9")
T1 = Locator(860, 80+200, "T1")
T2 = Locator(860, 80+415, "T2")


Button(top,text='Test',command=lambda:test()).pack(expand=True)  # https://pythonguides.com/python-tkinter-mainloop/
Button(top,text='UN Test',command=lambda:un_test()).pack(expand=True)

C.pack(fill="both", expand=True)
top.mainloop()
