from auctionsystem.udp import server as udp_server
from auctionsystem.tcp import server as tcp_server
import pickle

class AuctionServer:
    def __init__(self):

        # File path for registration table file
        self.registration_file = 'registration_file.pickle'

        # Load the registration_table from file if it exists, else create it
        try:
            self.registration_table = pickle.load(open(self.registration_file, "rb"))
        except (OSError, IOError) as e:
            self.registration_table = dict()
            pickle.dump(self.registration_table, open(self.registration_file, "wb"))

        # Keep track of item numbers to ensure they're all unique
        self.next_item_number = 0

        # Setup sockets
        self.udp_socket = udp_server.get_udp_server_socket()
        self.tcp_socket = tcp_server.get_tcp_server_socket()


    def rcv_register(self, req_num, name, ip_addr, port_num):
        # Is this a valid registration attempt?
        validity = 'valid'

        # The client's name is assumed to be unique, it should not already be there
        if name in self.registration_table:
            validity = 'Client name is already in the registration table'

        # TODO: what if ip_address is damaged?
        bad_ip = False
        if bad_ip:
            validity = 'ip_address is not valid or is damaged'

        if validity is 'valid':
            #  Update the registration table with the new entry
            registration_data = {'req_num': req_num, 'ip_addr': ip_addr,
                                 'port_num': port_num, 'bids': list(), 'offers': list()}
            self.registration_table[name] = registration_data

            #  Serialize and save the registration_data to file
            with open(self.registration_file, 'wb') as file:
                pickle.dump(self.registration_table, file)

            #  Acknowledge the registration to the client
            self.send_registered(req_num, name, ip_addr, port_num)

        else:
            # Respond with why the client can't register
            self.send_unregistered(req_num, validity, ip_addr, port_num)

    def rcv_deregister(self, req_num, name, ip_addr):
        #  Fetch port number since you might need it to send acks
        port_num = self.registration_table[name].port_num

        #  Is this a valid deregistration attempt?
        validity = 'valid'

        #  The client's name is assumed to already be in the table, else can't remove
        if name not in self.registration_table:
            validity = 'Client name not found in the registration table, might not have been registered at all'

        #  TODO: Is client offering an item for auction, is client active in bid
        offering_item = False # TODO
        if offering_item:
            validity = 'An item is currently being offered for auction'
        active_bid = False # TODO should equal whether or not client has highest bid
        if active_bid:
            validity = 'Client is currently leading with the highest bid for at least one item'

        #  TODO: what if ip_address or DEREGISTER is damaged?
        bad_ip = False
        if bad_ip:
            validity = 'ip_address is not valid or is damaged, cannot deregister'

        if validity is 'valid':
            #  Update the registration table by removing the entry
            self.registration_table.remove(name)

            #  Serialize and save the registration_data to file
            with open(self.registration_file, 'wb') as file:
                pickle.dump(self.registration_table, file)

            #  Acknowledge the deregistration to the client
            self.send_deregister_confirm(req_num, ip_addr, port_num)

        else:
            # Respond with why the client can't deregister
            self.send_deregister_denied(req_num, validity, ip_addr, port_num)


    def send_registered(self, req_num, name, ip_addr, port_num):
        #  TODO: Send UDP message to confirm registration to the client
        pass


    def send_unregistered(self, req_num, validity, ip_addr, port_num):
        #  TODO: send UDP message with req_unm and validity reason for unregistrating client
        pass


    def send_deregister_confirm(self, req_num, ip_addr, port_num):
        #  TODO: Send UDP message to confirm deregistration to the client
        pass


    def send_deregister_denied(self, req_num, validity, ip_addr, port_num):
        #  TODO: send UDP message with req_num and validity reason for not deregistering client
        pass

    def rcv_offer(self, req_num, name, ip_addr, port_num, desc, min):
        # Is this a valid offer attempt?
        validity = 'valid'

        # The client needs to be registered to make an offer
        if name not in self.registration_table:
            validity = 'Client name is not in the registration table. They must be registered to make an offer'

        # The client is only allowed to make 3 simultaneous offers
        if len(self.registration_table[name]['offers']) > 3:
            validity = 'Client cannot have more than 3 items offered for bidding simultaneously'

        # TODO: what if ip_address or data is damaged?
        bad_ip = False
        if bad_ip:
            validity = 'ip_address is not valid or is damaged'

        if validity is 'valid':
            # Update the registration table with the new offer
            # Todo: Should reg_table's offers only contain the item# or also description and minimum ?
            # TODO: Should we store the start time of the item's auction in the offer?
            offer = (self.next_item_number, desc, min)
            self.registration_table[name]['offers'].append(offer)
            self.next_item_number += 1

            # TODO: Should table be saved to file for EACH offer or only during registration/deregistration?
            #  Serialize and save the registration_data to file
            # with open(self.registration_file, 'wb') as file:
            #     pickle.dump(self.registration_table, file)

            # Acknowledge the offer to the client
            self.send_offer_confirm(req_num, name, offer)

            # Inform all clients that a new item is offered at the auction
            self.sendall_new_item(offer)

        else:
            # Respond with why the client can't offer the item
            self.send_offer_denied(req_num, validity, ip_addr, port_num)


    def send_offer_confirm(self, req_num, name, offer):
        #  TODO: Send UDP message to confirm offer to the client ; use name to get their address
        pass


    def sendall_new_item(self, offer):
        #  TODO: Create new TCP socket to handle bidding for this item ; send to all clients
        pass


    def send_offer_denied(self, req_num, validity, ip_addr, port_num):
        #  TODO: Send UDP message to deny offer to the client and explain why
        pass


    def rcv_bid(self, req_num, item_num, amount, addr):
        #  TODO: receive bid, maybe directly get address from tcp receive or name or something
        #  TODO: If the bid is the highest one yet for the item, then sendall_highest_bid
        #  TODO: confirm No need to handle lost bid requests bc they'll just send more, but reject bids less than min
        pass


    def sendall_highest_bid(self, item_num, amount):
        #  TODO: Use TCP socket to send new highest bid to all clients
        pass

    def send_winner(self, item_num, name, ip_addr, port_num,  amount):
        #  TODO: Use TCP socket to send winner new item details
        #  TODO: sendall_bid_over + send_sold_to
        #  TODO: Transfer item from one client to another in the table
        pass

    def send_sold_to(self, item_num, name, ip_addr, port_num,  amount):
        #  TODO: Use TCP socket to send seller details about winner
        #  TODO: Transfer item from one client to another in the table
        pass

    def send_not_sold(self, item_num, reason):
        #  TODO: Use TCP socket to tell seller that no one bought their item
        #  TODO: rip
        pass

    def sendall_bid_over(self, item_num):
        #  TODO: Use TCP socket to send bid end to all clients
        #  TODO: Remove all bids of each client for this item in the table
        pass