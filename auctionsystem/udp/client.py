import asyncio
import socket
import sys


class UDPClient():

    def __init__(self, loop, server_address):
        self._write_queue = asyncio.Queue(loop=loop)
        self.recv_queue = asyncio.Queue(loop=loop)
        self._closed = False
        self._socket, self.client_address = self._get_udp_client_socket(server_address)

        # Start listeners for read/write events
        loop.create_task(self._handle_send())
        loop.create_task(self._handle_receive(loop))

    def send(self, data, addr):
        self._write_queue.put_nowait((data, addr))

    def close_socket(self):
        print('Closing socket', file=sys.stderr)
        self._closed = True
        self._socket.close()

    async def _handle_receive(self, loop):
        while True:
            data, addr = await self._async_recvfrom(loop, 1024)
            print('From {0} received: {1}'.format(addr, data), file=sys.stderr)
            await self.recv_queue.put((data, addr))

    def _async_recvfrom(self, loop, n_bytes, future=None, registered=False):
        # asyncio doesn't have an asynchronous version of recvfrom so this is an implementation of it

        # Get the socket's file number so that it can be monitored for change
        sock_file = self._socket.fileno()

        # Only create a new Future object if there isn't already one
        if future is None:
            future = loop.create_future()

        # Avoid adding the same reader multiple times
        if registered:
            loop.remove_reader(sock_file)

        # Check and see if the data and address have been received, else wait on future values
        try:
            # TODO: Should add another exception for ConnectionResetError when server goes down
            data, addr = self._socket.recvfrom(n_bytes)
        except (BlockingIOError, InterruptedError):
            loop.add_reader(sock_file, self._async_recvfrom, loop, n_bytes, future, True)
        else:
            future.set_result((data, addr))
        return future

    async def _handle_send(self):
        while True:
            # Wait until something is put in the write_queue and then send it
            data, addr = await self._write_queue.get()
            self._socket.sendto(data, addr)
            self._write_queue.task_done()
            print('To {0} sent: {1}'.format(addr, data), file=sys.stderr)

    @staticmethod
    def _get_udp_client_socket(server_address):
        # Create a UDP socket
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Do we need this?
            sock.setblocking(False)
            print('UDP client socket created')
        except OSError as err:
            print('Failed to create client socket. Error: {0}'.format(err))
            sys.exit()

        # You need at least one sendto for the client before calling any "recvfrom"
        # otherwise it doesn't know where the host is
        sock.sendto(b'TEST::Starting connection', server_address)  # TODO: find soln to hack
        print('To {0} sent: {1}'.format(server_address, b'Starting connection'), file=sys.stderr)

        # Get client socket's address and port number
        client_ip_address = socket.getfqdn()  # Get fully qualified domain name
        client_port_num = sock.getsockname()[1]

        return sock, (client_ip_address, client_port_num)
