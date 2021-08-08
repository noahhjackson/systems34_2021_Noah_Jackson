import tkinter as tk


# a subclass of Canvas for dealing with resizing of windows
class ResizingCanvas(tk.Canvas):
    def __init__(self, parent, **kwargs):
        tk.Canvas.__init__(self, parent, **kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def on_resize(self, event):
        # determine the ratio of old width/height to new width/height
        wscale = event.width/self.width
        hscale = event.height/self.height
        self.width = event.width
        self.height = event.height
        # rescale all the objects
        self.scale("all", 0, 0, wscale, hscale)


def main():
    root = tk.Tk()
    myframe = tk.Frame(root)
    myframe.pack(fill=tk.BOTH, expand=tk.YES)
    mycanvas = ResizingCanvas(myframe,width=850, height=400, bg="light blue")#, highlightthickness=0)
    mycanvas.pack(fill=tk.BOTH, expand=tk.YES)

    # add some widgets to the canvas
    mycanvas.create_line(0, 0, 200, 100)
    mycanvas.create_line(0, 100, 200, 0, fill="red", dash=(4, 4))
    mycanvas.create_rectangle(50, 25, 150, 75, fill="blue")

    # tag all of the drawn widgets
    root.mainloop()


if __name__ == "__main__":
    main()
