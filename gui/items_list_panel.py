import tkinter as tk
from gui.new_item_panel import NewItemPanel
import gui.gui_helper as helper


class ItemsListPanel(tk.Frame):

    def __init__(self, master=None, list_sel_cb=None, bid_cb=None):
        super(ItemsListPanel, self).__init__(master)
        self.master = master
        self.grid()

        # Fields
        self.list_sel_cb = list_sel_cb
        self.selected_item = ''

        # Create widgets

        # Row 0
        self.items_label = tk.Label(self, text='Items offered by others:')
        self.items_label.grid(row=0, column=0)

        # Row 1
        self.items_listbox = tk.Listbox(self)
        self.items_listbox.event_generate(helper.SELECTION_EVENT_STR)
        self.items_listbox.bind(helper.SELECTION_EVENT_STR, self.selection_cb)
        self.items_listbox.insert(tk.END, 'Item 0')
        self.items_listbox.grid(row=1, column=0)

        # Row 2
        self.new_item_panel = NewItemPanel(self, bid_cb=bid_cb)
        self.new_item_panel.grid(row=2, column=0)

    def selection_cb(self, event):
        self.selected_item = event.widget.get(event.widget.curselection())
        print(self.selected_item)  # TODO: to remove
        self.list_sel_cb(self.selected_item)  # Updates the new item panel

    def add_new_item(self, item_num):
        self.items_listbox.insert(0, item_num)
