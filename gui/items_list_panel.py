import tkinter as tk
from gui.new_item_panel import NewItemPanel


class ItemsListPanel(tk.Frame):

    def __init__(self, master=None, bid_cb=None):
        super(ItemsListPanel, self).__init__(master)
        self.master = master
        self.grid()

        # Member variables
        self.items_list = []

        # Create widgets

        # Row 0
        self.items_label = tk.Label(self, text='Items offered by others:')
        self.items_label.grid(row=0, column=0)

        # Row 1
        self.items_listbox = tk.Listbox(self)
        self.items_listbox.grid(row=1, column=0)

        # Row 2
        self.new_item_panel = NewItemPanel(self, bid_cb=bid_cb)
        self.new_item_panel.grid(row=2, column=0)
