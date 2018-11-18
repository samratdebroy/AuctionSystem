# TODO: clients have to be independent of each other
# TODO: I/O system -> user input

from auctionsystem.udp.client import UDPClient
from auctionsystem.tcp.client import TCPClient
from auctionsystem.protocol import MESSAGE, PROTOCOL, REASON, AUCTION_CONSTS
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
        # Send registration request to server before doing anything else
        # TODO: Maybe use something more sophisticated to make realistic names (maybe should be user input)
        # Random letters and numbers
        self.client_name = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        address = self.udp_client.address
        self.send_register(self.client_name, address[0], str(address[1]))
        # TODO: Remove this while loop and replace with await self.listen_udp() or make self.run() into task
        while True:
            for item_num in list(self.bidding_items.keys()):
                item = self.bidding_items[item_num]
                self.send_bid(item_num, str(int(item['min']) + random.randint(1, 3000)))
                await asyncio.sleep(1)
            await asyncio.sleep(0.1)


    def handle_receive(self, data, addr=None):
        # TODO: Handle the case where data[0] is damaged or is None

        if data is None:
            # Other side has disconnected
            # TODO: Handle disconnection
            pass

        # Parse the data
        data = data.decode().split(PROTOCOL.DELIMITER)

        command = data[0]
        if command is 'TEST':
            return

        if command == MESSAGE.REGISTERED.value:
            self.rcv_registered(req_num=data[1], name=data[2], ip_addr=data[3], port_num=data[4])
        elif command == MESSAGE.UNREGISTERED.value:
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
        self.send_offer(self.client_name, self.udp_client.address[0], desc, random.randint(0, 300))
        print('received registered')

    def rcv_unregistered(self, req_num, reason):
        # The client could not register with the server
        msg_args = self.confirm_acknowledgement(req_num)
        if reason == REASON.ALREADY_REGISTERED.val:
            # Acknowledge the message and do nothing else
            self.confirm_acknowledgement(req_num)
            print('already registered')
        else:
            # Resend the register message - includes handling for bad IP
            print('resending register message')
            self.send_register(name=msg_args[0], ip_addr=msg_args[1], port_num=msg_args[2],
                               resending=True, req_num_resend=req_num)

    def rcv_dereg_conf(self, req_num, name, ip_addr):
        self.confirm_acknowledgement(req_num)
        self.tcp_clients.clear()  # Should close all of the connections
        self.udp_client.close_socket()
        print('received dereg conf')

    def rcv_dereg_denied(self, req_num, reason):
        # The client could not register with the server
        msg_args = self.confirm_acknowledgement(req_num)
        if reason == REASON.NOT_REGISTERED.val:
            # TODO: handle a case of not being registered - display message
            pass
        elif reason == REASON.ITEM_OFFERED.val:
            # TODO: Wait until all of your offered bidding_items have their auctions closed, stop creating new offers
            # TODO: Handle by GUI
            pass
        elif reason == REASON.ACTIVE_BID.val:
            # TODO: Wait until all of your active bids end,until no longer have highest bid for any item ; stop bidding
            # TODO: Handle by GUI
            pass
        else:
            # Resend the deregister message - includes handling for bad IP
            print('resending deregister message')
            self.send_deregister(name=msg_args[0], ip_addr=msg_args[1], resending=True, req_num_resend=req_num)

    def rcv_offer_conf(self, req_num, item_num, desc, min_price):
        # Handle UDP message to confirm registration offer was made for item
        self.confirm_acknowledgement(req_num)
        self.offers[req_num] = {'item_num': item_num, 'desc': desc, 'min': min_price}
        print('received offer conf')

    def rcv_offer_denied(self, req_num, reason):
        # The client could not register with the server
        msg_args = self.confirm_acknowledgement(req_num)
        if reason == REASON.NOT_REGISTERED.val:
            # TODO: handle a case of not being registered
            pass
        elif reason == REASON.OFFER_LIMIT.val:
            # If the server was mistaken, resend the offer message
            if len(self.offers) < AUCTION_CONSTS.OFFER_LIMIT:
                self.send_offer(name=msg_args[0], ip_addr=msg_args[1], desc=msg_args[2], min_price=msg_args[3],
                                resending=True, req_num_resend=req_num)
        else:
            # Resend offer for any other reason
            self.send_offer(name=msg_args[0], ip_addr=msg_args[1], desc=msg_args[2], min_price=msg_args[3],
                            resending=True, req_num_resend=req_num)

    def rcv_new_item(self, item_num, desc, min_price, port):
        if item_num in self.bidding_items.keys():
            # TODO: Handle server recovery
            # The server sent a new_item message for an item you already have,
            # it prolly means server went down and recovered, you have to reinit your TCP Server for this item
            # resend your last bid
            pass
        else:
            self.bidding_items[item_num] = {'item_num': item_num, 'port_num': port, 'desc': desc, 'min': min_price,
                                            'highest': False, 'highest_bid': min_price, 'last_bid': 0}
            self.tcp_clients[item_num] = TCPClient(self.loop, self.handle_receive, (self.server_address[0], int(port)))
            # TODO: Choose whether or not to bid on this item - done by GUI

    def rcv_highest(self, item_num, amount):
        if amount == self.bidding_items[item_num]['last_bid']:
            self.bidding_items[item_num]['highest'] = True
        else:
            self.bidding_items[item_num]['highest'] = False
        # TODO: Choose whether or not to bid more on this item - done by GUI

    def rcv_win(self, item_num, name, ip_addr, port_num, amount):
        self.bidding_ended(item_num)
        print("You are the winner of item {}, bought for {}!".format(item_num, amount))

    def rcv_bid_over(self, item_num, amount):
        self.bidding_ended(item_num)
        print("You are NOT the winner of item {}, bought for {}!".format(item_num, amount))

    def bidding_ended(self, item_num):
        del self.tcp_clients[item_num]
        del self.bidding_items[item_num]

    def rcv_sold_to(self, item_num, name, ip_addr, port, amount):
        # TODO: Don't do anything
        del self.offers[item_num]

    def rcv_not_sold(self, item_num, reason):
        # TODO: Choose whether or not to bid on this item
        if reason == REASON.NO_VALID_BIDS.val:
            # TODO: handle a case of not having a winner due to invalid bids - Handled by GUI
            # (Could put it up for offer again with smaller minimum amount)
            pass
        else:
            # TODO: something went wrong - throw exception or something
            pass

    # Send Messages

    def send_register(self, name, ip_addr, port_num, resending=False, req_num_resend=-1):
        #  Send UDP message to request registration to the server
        self.send_udp_message(name, ip_addr, port_num, message=MESSAGE.REGISTER,
                              resending=resending, req_num_resend=req_num_resend)

    def send_deregister(self, name, ip_addr, resending=False, req_num_resend=-1):
        #  Send UDP message to request deregistration to the server
        self.send_udp_message(name, ip_addr, message=MESSAGE.DEREGISTER,
                              resending=resending, req_num_resend=req_num_resend)

    def send_offer(self, name, ip_addr, desc, min_price, resending=False, req_num_resend=-1):
        #  Send UDP message to request deregistration to the server
        self.send_udp_message(name, ip_addr, desc, str(min_price), message=MESSAGE.OFFER,
                              resending=resending, req_num_resend=req_num_resend)

    def send_bid(self, item_num, amount):
        data_to_send = self.make_data_to_send(MESSAGE.BID.value, self.request_num_counter, item_num, amount,
                                              self.client_name)
        self.tcp_clients[item_num].send(data_to_send)
        if int(amount) > int(self.bidding_items[item_num]['last_bid']):
            self.bidding_items[item_num]['last_bid'] = amount
        self.request_num_counter += 1

    @staticmethod
    def make_data_to_send(*argv):
        # Returns encoded binary data formatted as a string with delimiters between each element
        args = []
        for arg in argv:
            args.append(str(arg))
            
        data = PROTOCOL.DELIMITER.join(args)
        return data.encode()

    def send_udp_message(self, *args, message, resending=False, req_num_resend=-1):
        #  Send UDP message to to the client
        req_num = str(self.request_num_counter if not resending else req_num_resend)
        data_to_send = self.make_data_to_send(message.value, req_num, *args)
        self.udp_client.send(data_to_send, self.server_address)
        self.loop.create_task(self.ensure_ack_received(*args, req_num=req_num, message=message, time_delay=5))
        if not resending:
            self.request_num_counter += 1

    async def ensure_ack_received(self, *args, req_num, message, time_delay):
        self.sent_messages[req_num] = args  # TODO: Assign args as a list or something to keep track of the messages

        # Wait until time-out to check if acknowledgement was received
        await asyncio.sleep(time_delay)

        if self.sent_messages[req_num]:
            # We timed-out without receiving an acknowledgement
            print('timeOut: Request number {} with args {} has not received acknowledgement'
                  .format(req_num, self.sent_messages[req_num]))
            self.send_udp_message(args, message=message, resending=True, req_num_resend=int(req_num))

    def confirm_acknowledgement(self, req_num):
        msg_args = self.sent_messages[req_num]
        self.sent_messages[req_num] = None
        return msg_args
