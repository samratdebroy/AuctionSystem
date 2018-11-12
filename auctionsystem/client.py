# TODO: clients have to be independent of each other
# # TODO: I/O system -> automated or user input

from auctionsystem.udp.client import UDPClient
from auctionsystem.tcp.client import TCPClient
from auctionsystem.protocol import MESSAGE, PROTOCOL, REASON
import asyncio

# To generate random name for client
import string
import random

# Just to get fully qualified domain name
import socket

class AuctionClient:
    def __init__(self, server_address=(socket.getfqdn(), 8888)):

        self.loop = asyncio.get_event_loop()

        # Setup sockets
        self.server_address = server_address
        self.udp_client = UDPClient(self.loop, self.handle_receive, self.server_address)
        self.tcp_clients = dict()

        self.client_name = ''
        self.sent_messages = dict()
        self.bidding_items = dict()
        self.offers = dict()

        self.request_num_counter = 0

        # Run the event loop
        self.loop.run_until_complete(self.run())
        self.loop.close()

    def __del__(self):
        if self.udp_client is not None:
            self.udp_client.close_socket()

    async def run(self):
        i = 0

        # Send registration request to server before doing anything else
        # TODO: Maybe use something more sophisticated to make realistic names (maybe should be user input)
        self.client_name = ''.join(random.choices(string.ascii_letters + string.digits, k=10))  # Random letters and numbers
        address = self.udp_client.address
        self.send_register(self.request_num_counter, self.client_name, address[0], str(address[1]))
        self.request_num_counter += 1

        # TODO: Remove this while loop and replace with await self.listen_udp() or make self.run() into task
        while True:
            for item_num, item in self.bidding_items.items():
                self.send_bid(self.request_num_counter, item_num, str(int(item['min']) + random.randint(1, 3000)))
                await asyncio.sleep(1)
            self.request_num_counter += 1
            await asyncio.sleep(0.1)

    def handle_receive(self, data, addr=None):
        # TODO: Handle the case where data[0] is damaged or is None

        # Parse the data
        data = data.decode().split(PROTOCOL.DELIMITER)

        command = data[0]
        if command is 'TEST':
            return

        if command == MESSAGE.REGISTERED.value:
            self.rcv_registered(req_num=data[1], name=data[2], ip_addr=data[3], port_num=data[4])
        if command == MESSAGE.UNREGISTERED.value:
            self.rcv_unregistered(req_num=data[1], reason=data[2])
        elif command == MESSAGE.DEREGISTER_CONFIRM.value:
            self.rcv_dereg_conf(req_num=data[1], name=data[2], ip_addr=data[3])
        elif command == MESSAGE.DEREGISTER_DENIED.value:
            self.rcv_dereg_denied(req_num=data[1], reason=data[2])
        elif command == MESSAGE.OFFER_CONFIRM.value:
            self.rcv_offer_conf(req_num=data[1], item_num=data[2], desc=data[3], min_price=data[4])
        elif command == MESSAGE.OFFER_DENIED.value:
            self.rcv_offer_denied(req_num=data[1], reason=data[2])
        elif command == MESSAGE.NEW_ITEM.value:
            self.rcv_new_item(item_num=data[1], desc=data[2], min_price=data[3], port=data[4])
        elif command == MESSAGE.HIGHEST.value:
            self.rcv_highest(item_num=data[1], amount=data[2])
        elif command == MESSAGE.WIN.value:
            self.rcv_win(item_num=data[1], name=data[2], ip_addr=data[3], port_num=data[4], amount=data[5])
        elif command == MESSAGE.BID_OVER.value:
            self.rcv_bid_over(item_num=data[1], amount=data[2])
        elif command == MESSAGE.SOLD_TO.value:
            self.rcv_sold_to(item_num=data[1], name=data[2], ip_addr=data[3], port=data[4], amount=data[5])
        elif command == MESSAGE.NOT_SOLD.value:
            self.rcv_not_sold(item_num=data[1], reason=data[2])
        else:
            pass  # TODO: Something went super wrong, this wasn't a valid command message :O

    def rcv_registered(self, req_num, name, ip_addr, port_num):
        # TODO: Handle UDP message to confirm registration for the client
        self.confirm_acknowledgement(req_num)
        # TODO: REMOVE THIS, CONTROLLER STUFF SHOULD BE ELSEWHERE
        desc = ''.join(random.choices(string.ascii_letters + string.digits, k=30))  # Random letters and numbers
        self.send_offer(self.request_num_counter, self.client_name, self.udp_client.address[0],
                        desc, random.randint(0, 300))
        self.request_num_counter += 1

        print('received registered')

    def rcv_unregistered(self, req_num, reason):
        # The client could not register with the server
        self.confirm_acknowledgement(req_num)
        if reason == REASON.BAD_IP.val:
            # TODO: handle a case of bad ip
            pass
        elif reason == REASON.ALREADY_REGISTERED.val:
            # TODO: do nothing since you're already registered?
            pass
        else:
            # TODO: something went wrong - throw exception or something
            pass

    def rcv_dereg_conf(self, req_num, name, ip_addr):
        # TODO: Handle UDP message to confirm registration for the client
        self.confirm_acknowledgement(req_num)
        print('received dereg conf')

    def rcv_dereg_denied(self, req_num, reason):
        # The client could not register with the server
        self.confirm_acknowledgement(req_num)
        if reason == REASON.NOT_REGISTERED.val:
            # TODO: handle a case of not being registered
            pass
        elif reason == REASON.ITEM_OFFERED.val:
            # TODO: Wait until all of your offered bidding_items have their auctions closed, stop creating new offers
            pass
        elif reason == REASON.ACTIVE_BID.val:
            # TODO: Wait until all of your active bids end,until no longer have highest bid for any item ; stop bidding
            pass
        else:
            # TODO: something went wrong - throw exception or something
            pass

    def rcv_offer_conf(self, req_num, item_num, desc, min_price):
        # Handle UDP message to confirm registration offer was made for item
        self.confirm_acknowledgement(req_num)
        self.offers[req_num] = {'item_num': item_num, 'desc': desc, 'min': min_price}
        print('received dereg conf')

    def rcv_offer_denied(self, req_num, reason):
        # The client could not register with the server
        self.confirm_acknowledgement(req_num)
        if reason == REASON.NOT_REGISTERED.val:
            # TODO: handle a case of not being registered
            pass
        elif reason == REASON.OFFER_LIMIT.val:
            # TODO: The server thinks you already have more than three active offers, is this correct?
            pass
        elif reason == REASON.BAD_IP.val:
            # TODO: IP address sent to server was invalid or damaged
            pass
        else:
            # TODO: something went wrong - throw exception or something
            pass

    def rcv_new_item(self, item_num, desc, min_price, port):
        self.bidding_items[item_num] = {'port_num': port, 'desc': desc, 'min': min_price,
                                        'highest': False, 'highest_bid': min_price, 'last_bid': 0}
        self.tcp_clients[item_num] = TCPClient(self.loop, self.handle_receive, (self.server_address[0], int(port)))
        # TODO: Choose whether or not to bid on this item

    def rcv_highest(self, item_num, amount):
        if amount == self.bidding_items[item_num]['last_bid']:
            self.bidding_items[item_num]['highest'] = True
        else:
            self.bidding_items[item_num]['highest'] = False
        # TODO: Choose whether or not to bid more on this item

    def rcv_win(self, item_num, name, ip_addr, port_num, amount):
        # TODO: Handle victory? ...
        print("You are the winner of item {}, bought for {}!".format(item_num, amount))

    def rcv_bid_over(self, item_num, amount):
        del self.tcp_clients[item_num]
        del self.bidding_items[item_num]
        print("You are NOT the winner of item {}, bought for {}!".format(item_num, amount))

    def rcv_sold_to(self, item_num, name, ip_addr, port, amount):
        # TODO: Don't do anything
        del self.offers[item_num]
        pass

    def rcv_not_sold(self, item_num, reason):
        # TODO: Choose whether or not to bid on this item
        if reason == REASON.NO_VALID_BIDS.val:
            # TODO: handle a case of not having a winner due to invalid bids
            # (Could put it up for offer again with smaller minimum amount)
            pass
        else:
            # TODO: something went wrong - throw exception or something
            pass

    # Send Messages

    def send_register(self, req_num, name, ip_addr, port_num):
        #  Send UDP message to request registration to the server
        self.send_udp_message(name, ip_addr, port_num, req_num=req_num, message=MESSAGE.REGISTER)

    def send_deregister(self, req_num, name, ip_addr):
        #  Send UDP message to request deregistration to the server
        self.send_udp_message(name, ip_addr, req_num=req_num, message=MESSAGE.DEREGISTER)

    def send_offer(self, req_num, name, ip_addr, desc, min_price):
        #  Send UDP message to request deregistration to the server
        self.send_udp_message(name, ip_addr, desc, str(min_price), req_num=req_num, message=MESSAGE.OFFER)

    def send_bid(self, req_num, item_num, amount):
        data_to_send = self.make_data_to_send(MESSAGE.BID, str(req_num), item_num, str(amount))
        self.tcp_clients[item_num].send(data_to_send)

    @staticmethod
    def make_data_to_send(*argv):
        # Returns encoded binary data formatted as a string with delimiters between each element
        args = []
        for arg in argv:
            args.append(str(arg))
            
        data = PROTOCOL.DELIMITER.join(args)
        return data.encode()

    def send_udp_message(self, *args, req_num, message):
        #  Send UDP message to to the client
        data_to_send = self.make_data_to_send(message.value, str(req_num), *args)
        self.udp_client.send(data_to_send, self.server_address)
        self.loop.create_task(self.ensure_ack_received(*args, req_num=req_num, message=message, time_delay=5))

    async def ensure_ack_received(self, *args, req_num, message, time_delay):
        self.sent_messages[req_num] = args  # TODO: Assign args as a list or something to keep track of the messages

        # Wait until time-out to check if acknowledgement was received
        await asyncio.sleep(time_delay)

        if self.sent_messages[req_num]:
            # We timed-out without receiving an acknowledgement
            print('timeOut')
            # TODO: Handle timeouts - resend the same info

    def confirm_acknowledgement(self, req_num):
        self.sent_messages[req_num] = None
