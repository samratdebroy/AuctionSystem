import tkinter as tk
from gui.my_offers_info_panel import MyOffersInfoPanel


class MyOffersPanel(tk.Frame):

    def __init__(self, master=None, reoffer_cb=None):
        super(MyOffersPanel, self).__init__(master)
        self.master = master
        self.grid()

        # Create Widgets

        # Row 0
        self.ongoing_offers_label = tk.Label(self, text='My Offered Items')
        self.ongoing_offers_label.grid(row=0, column=0)

        # Row 1
        self.ongoing_offers_label = tk.Label(self, text='Ongoing Auction')
        self.ongoing_offers_label.grid(row=1, column=0)

        self.ended_offers_label = tk.Label(self, text='Auction Ended')
        self.ended_offers_label.grid(row=1, column=1)

        # Row 2
        self.ongoing_offers_listbox = tk.Listbox(self)
        self.ongoing_offers_listbox.grid(row=2, column=0)

        self.ended_offers_listbox = tk.Listbox(self)
        self.ended_offers_listbox.grid(row=2, column=1)

        # Row 3
        self.info_panel = MyOffersInfoPanel(self, reoffer_cb)
        self.info_panel.grid(row=3, column=0)
