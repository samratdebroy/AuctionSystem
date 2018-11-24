import tkinter as tk
from gui.register_panel import RegisterPanel
from gui.deregister_panel import DeregisterPanel
from gui.items_list_panel import ItemsListPanel
from gui.my_offers_panel import MyOffersPanel
from gui.new_offer_panel import NewOfferPanel


# TODO: Add the callbacks as args to the constructor
class AuctionClientGui(tk.Frame):

    def __init__(self, master=None):
        super(AuctionClientGui, self).__init__(master)
        self.master = master
        self.grid()

        # Row 0
        self.reg_panel = RegisterPanel(master=self, register_cb=self.register_cb)
        self.reg_panel.grid(row=0, column=0)

        self.dereg_panel = DeregisterPanel(master=self, dereg_cb=self.default_cb)
        self.dereg_panel.grid(row=0, column=1)

        # Row 1
        self.items_list_panel = ItemsListPanel(master=self, bid_cb=self.default_cb)
        self.items_list_panel.grid(row=1, column=0)

        self.ongoing_offers_panel = MyOffersPanel(master=self, reoffer_cb=self.default_cb)
        self.ongoing_offers_panel.grid(row=1, column=1)

        self.new_offer_panel = NewOfferPanel(master=self, send_offer_cb=self.default_cb)
        self.new_offer_panel.grid(row=1, column=2)
        self.new_offer_panel.winfo_children()

        self.non_reg_panels = [self.dereg_panel, self.items_list_panel, self.ongoing_offers_panel, self.new_offer_panel]

    # Recursively sets a widget and all of its children disabled or non-disabled
    def set_disabled(self, widget, disable):

        state = tk.DISABLED if disable else tk.NORMAL

        # Frame instances don't have this configuration
        if 'state' in widget.config():
            widget.configure(state=state)

        for child in widget.winfo_children():
            self.set_disabled(child, disable)

    # Client Functions

    # To be called with True by the client when it receives the "registered" message
    # To be called with False by the client when it receives the "dereg_conf" message
    def activate_client_interface(self, activate):

        # When the interface is active, the register panel is inaccessible and the rest is
        # vice-versa when it's no longer active

        self.set_disabled(self.reg_panel, activate)

        for panel in self.non_reg_panels:
            self.set_disabled(panel, not activate)

    # To be called by the client it receives the "unregistered" message, pass in the reason
    def rcv_unregistered(self, response):
        self.reg_panel.set_response_text(response)

    # Button callbacks

    def register_cb(self, name, server_ip):
        print('Name = {0}, Server IP = {1}'.format(name, server_ip))

    def default_cb(self):
        print('Default callback!')


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Auction Client')
    app = AuctionClientGui(master=root)
    app.mainloop()
