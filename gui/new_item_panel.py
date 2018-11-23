import tkinter as tk


class NewItemPanel(tk.Frame):

    def __init__(self, master=None, bid_cb=None):
        super(NewItemPanel, self).__init__(master)
        self.master = master
        self.grid()

        # Create widgets

        # Row 0
        self.item_num_label = tk.Label(self)
        self.item_num_label.grid(row=0, column=0)

        self.name_label = tk.Label(self)
        self.name_label.grid(row=0, column=1)

        self.min_price_label = tk.Label(self)
        self.min_price_label.grid(row=0, column=2)

        # Row 1
        self.descr_label = tk.Label(self, text='Description:')
        self.descr_label.grid(row=1, column=0)

        # TODO: Change this to a read-only text object, make a function to put in the text
        self.descr_val_label = tk.Label(self)
        self.descr_val_label.grid(row=1, column=1, columnspan=2)

        # Row 2
        self.highest_label = tk.Label(self)
        self.highest_label.grid(row=2, column=0, columnspan=3)

        # Row 3
        self.bid_label = tk.Label(self, text='Bid')
        self.bid_label.grid(row=3, column=0)

        self.bid_entry = tk.Entry(self)
        self.bid_entry.grid(row=3, column=1)

        # Initial setting of labels
        self.update_fields()

    def update_fields(self, item_num=0, name='', min_price=0, descr='', highest=0):
        self.item_num_label['text'] = 'Item {}'.format(item_num)
        self.name_label['text'] = 'Offered by: {}'.format(name)
        self.min_price_label['text'] = 'Min: ${}'.format(min_price)
        self.descr_val_label['text'] = descr
        self.highest_label['text'] = 'Highest bid: ${}'.format(highest)
