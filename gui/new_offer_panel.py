import tkinter as tk


class NewOfferPanel(tk.Frame):

    def __init__(self, master=None, send_offfer_cb=None):
        super(NewOfferPanel, self).__init__(master)
        self.master = master
        self.grid()

        # Create widgets

        # Row 0
        self.new_offer_label = tk.Label(self, text='New Offer');
        self.new_offer_label.grid(row=0, column=0)

        # Row 1
        self.descr_label = tk.Label(self, text='Item Description:')
        self.descr_label.grid(row=1, column=0)

        # Row 2
        self.descr_text = tk.Text(self, width=30, height=6)
        self.descr_text.grid(row=2, column=0, columnspan=2)

        # Row 3
        self.min_price_label = tk.Label(self, text='Minimum Price:')
        self.min_price_label.grid(row=3, column=0)

        self.min_price_entry = tk.Entry(self)
        self.min_price_entry.grid(row=3, column=1)

        # Row 4
        self.put_up_offer_button = tk.Button(self, text='Put up for Auction', command=send_offfer_cb)
        self.put_up_offer_button.grid(row=4, column=0, columnspan=2)

        # Row 5
        # TODO: Change to read only text, make method to fill text
        self.response_label = tk.Label(self, text='Response:')
        self.response_label.grid(row=5, column=0)

        self.response_msg_label = tk.Label(self, text='')
        self.response_msg_label.grid(row=5, column=1)
