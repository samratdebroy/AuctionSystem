import asyncio
import socket
import sys


class UDPServer:

    def __init__(self, loop, handle_receive_cb, port_number = 8888):
        self._closed = False
        self._socket = self._get_udp_server_socket(port_number)

        # Start listeners for read/write events
        loop.create_task(self._handle_receive(loop, handle_receive_cb))

    def send(self, data, addr):
        self._socket.sendto(data, addr)
        print('To {0} sent: {1}'.format(addr, data), file=sys.stderr)

    def close_socket(self):
        print('Closing socket', file=sys.stderr)
        self._closed = True
        self._socket.close()

    @staticmethod
    def _get_udp_server_socket(port_number = 8888):
        # Create a UDP socket
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # TODO: Check if we need to use sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.setblocking(False)
            print('UDP server socket created')
        except OSError as err:
            print('Failed to create server socket. Error: {0}'.format(err))
            sys.exit()

        ip_address = socket.getfqdn()  # Get fully qualified domain name
        server_address = (ip_address, port_number)

        # Bind the socket to the port
        try:
            sock.bind(server_address)
            print('Socket binded to {0}'.format(server_address), file=sys.stderr)
        except OSError as err:
            print('Binding Failed to {0}. Error: {1}'
                  .format(server_address, err), file=sys.stderr)
            sys.exit()

        return sock

    async def _handle_receive(self, loop, handle_receive_cb):
        while True:
            data, addr = await self._async_recvfrom(loop, 1024)
            print('From {0} received: {1}'.format(addr, data), file=sys.stderr)
            handle_receive_cb(data, addr)

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
            data, addr = self._socket.recvfrom(n_bytes)
        except (BlockingIOError, InterruptedError):
            loop.add_reader(sock_file, self._async_recvfrom, loop, n_bytes, future, True)
        else:
            future.set_result((data, addr))
        return future
