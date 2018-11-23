import tkinter as tk


class MyOffersInfoPanel(tk.Frame):

    def __init__(self, master=None, reoffer_cb=None):
        super(MyOffersInfoPanel, self).__init__(master)
        self.master = master
        self.grid()

        # Create widgets

        # Row 0
        self.item_num_label = tk.Label(self)
        self.item_num_label.grid(row=0, column=0)

        # Row 1
        self.min_price_label = tk.Label(self, text='Minimum Price:')
        self.min_price_label.grid(row=1, column=0)

        self.min_price_label_val = tk.Label(self)
        self.min_price_label_val.grid(row=1, column=1)

        # Row 2
        self.status_label = tk.Label(self, text='Status:')
        self.status_label.grid(row=2, column=0)

        self.status_label_val = tk.Label(self)
        self.status_label_val.grid(row=2, column=1)

        # Row 3
        self.reoffer_button = tk.Button(text="Re-offer")
        self.reoffer_button.grid(row=3, column=0)

        # Initial setting of fields
        self.update_fields()

    def update_fields(self, item_num=0, min_price=0, status='---'):
        self.item_num_label['text'] = 'Item {}'.format(item_num)
        self.min_price_label_val['text'] = '${}'.format(min_price)
        self.status_label_val['text'] = status
