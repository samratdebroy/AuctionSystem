import asyncio
import socket
import sys


class TCPClient:

    def __init__(self, loop, handle_receive_cb, server_address=('', 8888)):
        self.server_address = server_address
        self._socket = self.get_tcp_client_socket(self.server_address[1])
        self._send_queue = asyncio.Queue(loop=loop)

        self.tasks = []
        # Create listener to receive data
        self.tasks.append(loop.create_task(self._handle_receive(loop, handle_receive_cb)))
        self.tasks.append(loop.create_task(self._handle_send(loop)))

    def __del__(self):
        self.close_connections()

    def close_connections(self):
        print('Closing connections to this TCP client', file=sys.stderr)
        # Stop listening for new data to send or receive
        for task in self.tasks:
            task.close()

        # Close this client's socket
        self._socket.close()

    def get_port_number(self):
        return str(self._socket.getsockname()[1])

    @staticmethod
    def get_tcp_client_socket(server_address):
        # Create a TCP socket
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setblocking(False)
            print('TCP client socket created')
        except OSError as err:
            print('Failed to create client socket. Error: {0}'.format(err))
            sys.exit()

        # Connect the TCP socket
        try:
            sock.connect(server_address)
            print('TCP client socket connected to server')
        except OSError as err:
            print('Failed to connect client socket. Error: {0}'.format(err))
            sys.exit()

        return sock

    def send(self, data):
        # Add data to async queue to ensure it's sent in order
        # TODO: handle exception where send_queue is full
        self._send_queue.put_nowait(data)

    async def _handle_receive(self, loop, handle_receive_cb):
        while True:
            data = await loop.sock_recv(self._socket, 1024)
            print('Received: {0} from {1}'.format(data, self.server_address), file=sys.stderr)
            handle_receive_cb(data, self.server_address)

    async def _handle_send(self, loop):
        while True:
            # Send data to client asynchronously
            data = await self._send_queue.get()
            await loop.sock_sendall(self._socket, data)
            print('Sent: {0} to {1}'.format(data, self.server_address), file=sys.stderr)
            self._send_queue.task_done()

