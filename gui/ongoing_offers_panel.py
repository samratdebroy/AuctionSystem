import tkinter as tk


class OngoingOffersPanel(tk.Frame):

    def __init__(self, master=None):
        super(OngoingOffersPanel, self).__init__(master)
        self.master = master
        self.grid()

        # Create Widgets

        # Row 0
        self.ongoing_offers_label = tk.Label(self, text='My Offered Items - Ongoing Auction')
        self.ongoing_offers_label.grid(row=0, column=0)

        # Row 1
        self.offers_listbox = tk.Listbox(self)
        self.offers_listbox.grid(row=1, column=0)
