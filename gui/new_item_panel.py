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

        # Row 1
        self.name_label = tk.Label(self, text='Offered by:')
        self.name_label.grid(row=1, column=0)

        self.name_label_val = tk.Label(self)
        self.name_label_val.grid(row=1, column=1)

        # Row 2
        self.min_price_label = tk.Label(self, text='Minimum Price:')
        self.min_price_label.grid(row=2, column=0)

        self.min_price_label_val = tk.Label(self)
        self.min_price_label_val.grid(row=2, column=1)

        # Row 3
        self.descr_label = tk.Label(self, text='Description:')
        self.descr_label.grid(row=3, column=0)

        # TODO: Change this to a read-only text object, make a function to put in the text
        self.descr_label_val = tk.Label(self)
        self.descr_label_val.grid(row=3, column=1, columnspan=4)

        # Row 4
        self.highest_label = tk.Label(self, text='Highest Bid: ')
        self.highest_label.grid(row=4, column=0)

        self.highest_label_val = tk.Label(self)
        self.highest_label_val.grid(row=4, column=1)

        # Row 5
        self.bid_label = tk.Label(self, text='Amount to Bid')
        self.bid_label.grid(row=5, column=0)

        self.bid_entry = tk.Entry(self)
        self.bid_entry.grid(row=5, column=1)

        # Row 6
        self.bid_button = tk.Button(self, text='Bid', command=bid_cb)
        self.bid_button.grid(row=6, column=0)

        # Initial setting of labels
        self.update_fields()

    def update_fields(self, item_num=0, name='---', min_price=0, descr='---', highest=0):
        self.item_num_label['text'] = 'Item {}'.format(item_num)
        self.name_label_val['text'] = name
        self.min_price_label_val['text'] = '${}'.format(min_price)
        self.descr_label_val['text'] = descr
        self.highest_label_val['text'] = '${}'.format(highest)
