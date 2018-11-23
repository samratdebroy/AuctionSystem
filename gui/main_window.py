import tkinter as tk
from gui.register_panel import RegisterPanel
from gui.deregister_panel import DeregisterPanel
from gui.items_list_panel import ItemsListPanel
from gui.ongoing_offers_panel import OngoingOffersPanel
from gui.new_offer_panel import NewOfferPanel


# TODO: Add the callbacks as args to the constructor
class AuctionClientGui(tk.Frame):

    def __init__(self, master=None):
        super(AuctionClientGui, self).__init__(master)
        self.master = master
        self.grid()

        # TODO: Create and add each individual panel here
        # Row 0
        self.reg_panel = RegisterPanel(master=self, register_cb=default_cb)
        self.reg_panel.grid(row=0, column=0)

        self.dereg_panel = DeregisterPanel(master=self, dereg_cb=default_cb)
        self.dereg_panel.grid(row=0, column=1)

        # Row 1
        self.items_list_panel = ItemsListPanel(master=self)
        self.items_list_panel.grid(row=1, column=0)

        self.ongoing_offers_panel = OngoingOffersPanel(master=self)
        self.ongoing_offers_panel.grid(row=1, column=1)

        self.new_offer_panel = NewOfferPanel(master=self, send_offfer_cb=default_cb)
        self.new_offer_panel.grid(row=1, column=2)  # TODO: Change column index so that it is on left most


def default_cb():
    print('Default callback!')


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Auction Client')
    app = AuctionClientGui(master=root)
    app.mainloop()
