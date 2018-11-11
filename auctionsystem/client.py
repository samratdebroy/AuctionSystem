# TODO: clients have to be independent of each other
# # TODO: I/O system -> automated or user input

from auctionsystem.udp import client as udp_client
from auctionsystem.protocol import MESSAGE, PROTOCOL
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
        self.udp_client = udp_client.UDPClient(self.loop, self.server_address)

        # Run the event loop
        self.loop.run_until_complete(self.run())
        self.loop.close()

    def __del__(self):
        if self.udp_client is not None:
            self.udp_client.close_socket()
        #self.tcp_client.close()

    async def run(self):
        i = 0

        # Send registration request to server before doing anything else
        # TODO: Maybe use something more sophisticated to make realistic names (maybe should be user input)
        client_name = ''.join(random.choices(string.ascii_letters + string.digits, k=10))  # Random letters and numbers
        address = self.udp_client.client_address
        self.send_register('0', client_name, address[0], str(address[1]))

        # Asynchronously check if anything was received in the UDP Client
        self.loop.create_task(self.listen_udp())

        # TODO: Remove this while loop and replace with await self.listen_udp() or make self.run() into task
        while True:
            self.udp_client.send('TEST{}Hey there from the client message {}'.format(PROTOCOL.DELIMITER, i).encode(),
                                                                                    self.server_address)
            i += 1
            await  asyncio.sleep(5)

    async def listen_udp(self):
        while True:
            # If anything is received from the udp socket, handle the data
            try:
                data, address = await self.udp_client.recv_queue.get()
                self.udp_client.recv_queue.task_done()
                self.handle_receive(data, address)
            except asyncio.QueueEmpty:
                continue

    def handle_receive(self, data, addr=None):
        # TODO: Handle the case where data[0] is damaged

        # Parse the data
        data = data.decode().split(PROTOCOL.DELIMITER)

        command = data[0]
        if command is 'TEST':
            return

        req_num = data[1]

        if req_num is None:
            pass # TODO something bad if request number is not valid

        if command == MESSAGE.REGISTERED.value:
            self.rcv_registered(req_num, name=data[2], ip_addr=data[3], port_num=data[4])
        # elif command == MESSAGE.DEREGISTER.val:
        #     self.rcv_deregister(req_num, name=data[2], ip_addr=data[3])
        # elif command == MESSAGE.OFFER.val:
        #     self.rcv_offer(req_num, name=data[2], ip_addr=data[3], port_num=addr[1], desc=data[4], min=int(data[5]))
        # elif command == MESSAGE.BID.val:
        #     self.rcv_bid(req_num, item_num=int(data[2]), amount=int(data[3]), addr=addr)
        else:
            pass #TODO: Something went super wrong, this wasn't a valid command message :O

    def rcv_registered(self, req_num, name, ip_addr, port_num):
        # TODO: Handle UDP message to confirm registration for the client
        print('received registered')

    def send_register(self, req_num, name, ip_addr, port_num):
        #  Send UDP message to request registration to the server
        data_to_send = self.make_data_to_send(MESSAGE.REGISTER.value, req_num, name, ip_addr, port_num)
        address = self.server_address
        self.udp_client.send(data_to_send, address)

    @staticmethod
    def make_data_to_send(*argv):
        # Returns encoded binary data formatted as a string with delimiters between each element
        data = PROTOCOL.DELIMITER.join(argv)
        return data.encode()
