<<<<<<< HEAD
from auctionsystem.udp import server as udp_server
from auctionsystem.tcp import server as tcp_server
from auctionsystem.protocol import MESSAGE
import queue

=======
from auctionsystem.udp.server import UDPServer
from auctionsystem.tcp import server as tcp_server # TODO: make TCPServer class
from auctionsystem.protocol import MESSAGE, REASON, PROTOCOL
import queue
import asyncio
>>>>>>> bf361abcf9b65c13148132ff11c3a545ebc3298a
import pickle


class AuctionServer:
    def __init__(self):

        self.loop = asyncio.get_event_loop()

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
<<<<<<< HEAD
        self.udp_socket = udp_server.get_udp_server_socket()
        self.tcp_socket = tcp_server.get_tcp_server_socket()

        # The server needs to keep track of the messages it receives in order of reception
        self.message_queue = queue.Queue()

    def __del__(self):
        self.udp_socket.close()
        self.tcp_socket.close()

    def run(self):
        # LETS DO THIS
        pass

    def listen_udp(self):
        # TODO: in an infinite while loop, listen to udp socket
        # TODO: if anything received in udp socket, add message to queue
        pass

    def listen_tcp(self):
        # TODO: in an infinite while loop, listen to tcp socket
        # TODO: if anything received in tcp socket, add message to queue
        pass
=======
        self.udp_server = UDPServer(self.loop)
        # TODO: self.tcp_socket = tcp_server.get_tcp_server_socket()

        # Run the event loop
        self.loop.run_until_complete(self.run())
        self.loop.close()

    def __del__(self):
        self.udp_server.close_socket()
        #self.tcp_socket.close()

    async def run(self):
        self.loop.create_task(self.listen_udp())
        # Check if anything was received in the UDP Server
        await self.listen_udp()

    async def listen_udp(self):
        while True:
            # If anything is received from the udp socket, handle the data
            try:
                data, addr = await self.udp_server.recv_queue.get()
                self.udp_server.recv_queue.task_done()
                self.handle_receive(data, addr)
            except asyncio.QueueEmpty:
                continue

    async def listen_tcp(self, tcp_server):
        # In an infinite while loop, listen to tcp socket
        # If anything is received from the tcp socket, handle the data
        # We're going to have to create one listen_tcp task per offered item
        while True:
            # If anything is received from the tcp socket, handle the data
            try:
                data, addr = await tcp_server.recv_queue.get()
                tcp_server.recv_queue.task_done()
                self.handle_receive(data, addr) # Todo: maybe have a different handle_receive for tcp messages
            except asyncio.QueueEmpty:
                continue
>>>>>>> bf361abcf9b65c13148132ff11c3a545ebc3298a


    def handle_receive(self, data, addr=None):
        # TODO: Handle the case where data[0] is damaged
<<<<<<< HEAD
        command = data[0]
=======

        # Parse the data
        data = data.decode().split(PROTOCOL.DELIMITER)

        command = data[0]
        if command == 'TEST':
            return

>>>>>>> bf361abcf9b65c13148132ff11c3a545ebc3298a
        req_num = data[1]

        if req_num is None:
            pass # TODO something bad if request number is not valid

<<<<<<< HEAD
        if command is MESSAGE.REGISTER:
            self.rcv_register(req_num, name=data[2], ip_addr=[3], port_num=[4])
        elif command is MESSAGE.DEREGISTER:
            self.rcv_deregister(req_num, name=[2], ip_addr=[3])
        elif command is MESSAGE.OFFER:
            self.rcv_offer(req_num, name=data[2], ip_addr=data[3], port_num=addr[1], desc=data[4], min=data[5])
        elif command is MESSAGE.BID:
            self.rcv_bid(req_num, item_num=data[2], amount=data[3], addr=addr)
        else:
            pass #TODO: Something went super wrong, this wasn't a valid command message :O

=======
        if command == MESSAGE.REGISTER.value:
            self.rcv_register(req_num, name=data[2], ip_addr=data[3], port_num=data[4])
        elif command == MESSAGE.DEREGISTER.value:
            self.rcv_deregister(req_num, name=data[2], ip_addr=data[3])
        elif command == MESSAGE.OFFER.value:
            self.rcv_offer(req_num, name=data[2], ip_addr=data[3], port_num=addr[1], desc=data[4], min=int(data[5]))
        elif command == MESSAGE.BID.value:
            self.rcv_bid(req_num, item_num=int(data[2]), amount=int(data[3]), addr=addr)
        else:
            pass #TODO: Something went super wrong, this wasn't a valid command message :O
>>>>>>> bf361abcf9b65c13148132ff11c3a545ebc3298a

    def rcv_register(self, req_num, name, ip_addr, port_num):
        # Is this a valid registration attempt?
        validity = REASON.VALID

        # The client's name is assumed to be unique, it should not already be there
        if name in self.registration_table:
            validity = REASON.ALREADY_REGISTERED

        # TODO: what if ip_address is damaged?
        bad_ip = False
        if bad_ip:
            validity = REASON.BAD_IP

        if validity is REASON.VALID:
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
            self.send_unregistered(req_num, validity.val, ip_addr, port_num)

    def rcv_deregister(self, req_num, name, ip_addr):
        #  Fetch port number since you might need it to send acks
        port_num = self.registration_table[name].port_num

        #  Is this a valid deregistration attempt?
        validity = REASON.VALID

        #  The client's name is assumed to already be in the table, else can't remove
        if name not in self.registration_table:
            validity = REASON.NOT_REGISTERED

        #  TODO: Is client offering an item for auction, is client active in bid
        offering_item = False # TODO
        if offering_item:
            validity = REASON.ITEM_OFFERED
        active_bid = False # TODO should equal whether or not client has highest bid
        if active_bid:
            validity = REASON.ACTIVE_BID

        #  TODO: what if ip_address or DEREGISTER is damaged?
        bad_ip = False
        if bad_ip:
            validity = REASON.BAD_IP

        if validity is REASON.VALID:
            #  Update the registration table by removing the entry
            del self.registration_table[name]

            #  Serialize and save the registration_data to file
            with open(self.registration_file, 'wb') as file:
                pickle.dump(self.registration_table, file)

            #  Acknowledge the deregistration to the client
            self.send_deregister_confirm(req_num, ip_addr, port_num)

        else:
            # Respond with why the client can't deregister
            self.send_deregister_denied(req_num, validity.val, ip_addr, port_num)

    def send_registered(self, req_num, name, ip_addr, port_num):
        #  Send UDP message to confirm registration to the client
        data_to_send = self.make_data_to_send(MESSAGE.REGISTERED.value, req_num, name, ip_addr, port_num)
        address = (ip_addr, int(port_num))
        self.udp_server.send(data_to_send, address)

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
        validity = REASON.VALID

        # The client needs to be registered to make an offer
        if name not in self.registration_table:
            validity = REASON.NOT_REGISTERED

        # The client is only allowed to make 3 simultaneous offers
        if len(self.registration_table[name]['offers']) > 3:
            validity = REASON.OFFER_LIMIT

        # TODO: what if ip_address or data is damaged?
        bad_ip = False
        if bad_ip:
            validity = REASON.BAD_IP

        if validity is REASON.VALID:
            # Update the registration table with the new offer
            # TODO: Should reg_table's offers only contain the item# or also description and minimum ?
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
            self.send_offer_denied(req_num, validity.val, ip_addr, port_num)

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

    @staticmethod
    def make_data_to_send(*argv):
        # Returns encoded binary data formatted as a string with delimiters between each element
        data = PROTOCOL.DELIMITER.join(argv)
        return data.encode()
