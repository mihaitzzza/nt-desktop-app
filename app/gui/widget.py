import tkinter
from app.gui.order_frame import OrderFrame


class Widget:
    def __init__(self):
        self.window = tkinter.Tk()
        self.window.geometry('800x600')
        self.window.winfo_toplevel().title('Python Pizza')

    def draw(self):
        order_frame = OrderFrame(self.window)
        order_frame.draw()
        order_frame.pack()

        self.window.mainloop()
