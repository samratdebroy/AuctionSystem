import tkinter as tk
from gui.register_panel import RegisterPanel


# TODO: Add the callbacks as args to the constructor
class AuctionClientGui(tk.Frame):

    def __init__(self, master=None):
        super(AuctionClientGui, self).__init__(master)
        self.master = master
        self.grid()

        # TODO: Create and add each individual panel here
        reg_panel = RegisterPanel(master=master, register_cb=default_cb)
        reg_panel.grid()


def default_cb():
    print('Default callback!')


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Auction Client')
    app = AuctionClientGui(master=root)
    app.mainloop()
