import tkinter as tk
import gui.gui_helper as helper


class NewItemPanel(tk.Frame):

    def __init__(self, master=None, bid_cb=None):
        super(NewItemPanel, self).__init__(master)
        self.master = master
        self.grid()

        # Fields
        self.bid_cb = bid_cb

        # Create widgets

        # Row 0
        self.item_num_label = tk.Label(self, text='Item:')
        self.item_num_label.grid(row=0, column=0)

        self.item_num_label_val = tk.Label(self)
        self.item_num_label_val.grid(row=0, column=1)

        # Row 1
        self.min_price_label = tk.Label(self, text='Minimum Price:')
        self.min_price_label.grid(row=1, column=0)

        self.min_price_label_val = tk.Label(self)
        self.min_price_label_val.grid(row=1, column=1)

        # Row 2
        self.descr_label = tk.Label(self, text='Description:')
        self.descr_label.grid(row=2, column=0)

        self.descr_label_val = tk.Label(self)
        self.descr_label_val.grid(row=2, column=1, columnspan=4)

        # Row 3
        self.highest_label = tk.Label(self, text='Highest Bid: ')
        self.highest_label.grid(row=3, column=0)

        self.highest_label_val = tk.Label(self)
        self.highest_label_val.grid(row=3, column=1)

        # Row 4
        self.bid_label = tk.Label(self, text='Amount to Bid')
        self.bid_label.grid(row=4, column=0)

        self.bid_entry = tk.Entry(self)
        self.bid_entry.grid(row=4, column=1)

        # Row 5
        self.bid_button = tk.Button(self, text='Bid', command=self.bid_cmnd)
        self.bid_button.grid(row=5, column=0)

        # Row 6
        self.response_label = tk.Label(self, text='Response:')
        self.response_label.grid(row=6, column=0)

        self.response_label_val = tk.Label(self)
        self.response_label_val.grid(row=6, column=1)

        # Initial setting of labels
        self.update_fields()

    def update_fields(self, item_num='---', min_price='---', descr='---', highest='---'):
        self.item_num_label_val['text'] = item_num
        self.min_price_label_val['text'] = '${}'.format(min_price)
        self.descr_label_val['text'] = helper.get_formatted_display_text(descr)
        self.highest_label_val['text'] = '${}'.format(highest)

    def set_response_text(self, response=''):
        self.response_label_val['text'] = helper.get_formatted_display_text(response)

    def bid_cmnd(self):
        item_num = self.item_num_label_val['text']
        bid = helper.get_truncated_entry(self.bid_entry, 10)
        if bid.isdigit():
            self.bid_cb(item_num, bid)
        else:
            self.set_response_text('Invalid minimum price. Please enter a valid number (< 10 digits).')

    def clear(self):
        self.update_fields()  # Default args are 'empty'
        self.bid_entry.delete(0, tk.END)
