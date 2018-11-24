import tkinter as tk
from auctionsystem.client import AuctionClient
from gui.register_panel import RegisterPanel
from gui.deregister_panel import DeregisterPanel
from gui.items_list_panel import ItemsListPanel
from gui.my_offers_panel import MyOffersPanel
from gui.new_offer_panel import NewOfferPanel
from auctionsystem.protocol import *


# TODO: Add the callbacks as args to the constructor
class AuctionClientGui(tk.Frame):

    def __init__(self, master=None):
        super(AuctionClientGui, self).__init__(master)
        self.master = master
        self.grid()

        # Fields
        self.client = None

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

        self.non_reg_panels = [self.dereg_panel, self.items_list_panel, self.ongoing_offers_panel, self.new_offer_panel]
        # self.activate_client_interface(False)

    # Recursively sets a widget and all of its children disabled or non-disabled
    def set_disabled(self, widget, disable):

        state = tk.DISABLED if disable else tk.NORMAL

        # Frame instances don't have this configuration
        if 'state' in widget.config():
            widget.configure(state=state)

        for child in widget.winfo_children():
            self.set_disabled(child, disable)

    # Button callbacks

    def register_cb(self, name, server_ip, port_num):
        self.client = AuctionClient(name=name, server_address=(server_ip, int(port_num)), gui_cb=self.rcv_msg)
        # self.client.send_register()

    def default_cb(self):
        print('Default callback!')

    def rcv_msg(self, command, *args):

        if command == MESSAGE.REGISTERED.value:
            self.activate_client_interface(True)
        elif command == MESSAGE.UNREGISTERED.value:
            self.rcv_unregistered(reason=args[0])
        elif command == MESSAGE.DEREGISTER_CONFIRM.value:
            self.activate_client_interface(False)
        elif command == MESSAGE.DEREGISTER_DENIED.value:
            self.rcv_dereg_denied(reason=args[0])
        elif command == MESSAGE.OFFER_CONFIRM.value:
            self.rcv_offer_conf(item_num=args[0])
        elif command == MESSAGE.OFFER_DENIED.value:
            self.rcv_offer_denied(reason=args[0])
        elif command == MESSAGE.NEW_ITEM.value:
            self.rcv_new_item(item_num=args[0])
        elif command == MESSAGE.HIGHEST.value:
            self.rcv_highest(item_num=args[0])
        elif command == MESSAGE.WIN.value:
            self.rcv_win(item_num=args[0], amount=args[1])
        elif command == MESSAGE.BID_OVER.value:
            self.rcv_bid_over(item_num=args[0], amount=args[1])
        elif command == MESSAGE.SOLD_TO.value:
            self.rcv_sold_to(item_num=args[0], name=args[1], ip_addr=args[2], port=args[3], amount=args[4])
        elif command == MESSAGE.NOT_SOLD.value:
            self.rcv_not_sold(item_num=args[0], reason=args[1])

    # Message Functions

    # Called when receiving registered or dereg confirmed messages
    def activate_client_interface(self, activate):

        # When the interface is active, the register panel is inaccessible and the rest is
        # vice-versa when it's no longer active

        self.set_disabled(self.reg_panel, activate)

        for panel in self.non_reg_panels:
            self.set_disabled(panel, not activate)

    def rcv_unregistered(self, reason):
        self.reg_panel.set_response_text(reason)

    def rcv_dereg_denied(self, reason):
        self.dereg_panel.set_response_text(reason)

    def rcv_offer_conf(self, item_num):
        pass

    def rcv_offer_denied(self, reason):
        self.new_offer_panel.set_response_text(reason)

    def rcv_new_item(self, item_num):
        pass

    def rcv_highest(self, item_num):
        pass

    def rcv_win(self, item_num, amount):
        pass

    def rcv_bid_over(self, item_num, amount):
        pass

    def rcv_sold_to(self, item_num, name, ip_addr, port, amount):
        pass

    def rcv_not_sold(self, item_num, reason):
        pass


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Auction Client')
    app = AuctionClientGui(master=root)
    app.mainloop()
