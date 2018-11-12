import asyncio
import socket
import sys


class TCPServer:

    class Connection:

        def __init__(self, loop, connection, address, handle_receive_cb):
            self.addr = address
            self.sock = connection
            self._send_queue = asyncio.Queue(loop=loop)
            self.tasks = []

            # Create listener to receive data
            self.tasks.append(loop.create_task(self._handle_receive(loop, handle_receive_cb)))
            self.tasks.append(loop.create_task(self._handle_send(loop)))

        def send(self, data):
            # Add data to async queue to ensure it's sent in order
            # TODO: handle exception where send_queue is full
            self._send_queue.put_nowait(data)

        async def _handle_receive(self, loop, handle_receive_cb):
            while True:
                data = await loop.sock_recv(self.sock, 1024)
                print('Received: {0} from {1}'.format(data, self.addr), file=sys.stderr)
                handle_receive_cb(data, self.addr)

        async def _handle_send(self, loop):
            while True:
                # Send data to client asynchronously
                data = await self._send_queue.get()
                await loop.sock_sendall(self.sock, data)
                print('Sent: {0} to {1}'.format(data, self.addr), file=sys.stderr)
                self._send_queue.task_done()

    def __init__(self, loop, handle_receive_cb, port_number=8888):

        self.conn = {}  # List of all valid connections
        self._socket = self.get_tcp_server_socket(port_number)

        # Start listener for new connections
        self.receive_task = loop.create_task(self._handle_new_connections(loop, handle_receive_cb))

    def __del__(self):
        self.close_connections()

    @staticmethod
    def get_tcp_server_socket(port_number = 10000):
        ip_address = b'localhost'
        server_address = (ip_address, port_number)

        # Create a TCP socket
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setblocking(False)
            print('TCP server socket created')
        except OSError as err:
            print('Failed to create server socket. Error: {0}'.format(err))
            sys.exit()

        # Bind the socket to the port
        try:
            sock.bind(server_address)
            print('Socket binded to {0}'.format(server_address), file=sys.stderr)
        except OSError as err:
            print('Binding Failed to {0}. Error: {1}'
                  .format(server_address, err), file=sys.stderr)
            sys.exit()

        # Listen for new incoming connection requests
        sock.listen(8)
        return sock

    async def _handle_new_connections(self, loop, handle_receive_cb):
        while True:
            conn, addr = await loop.sock_accept(self._socket)
            connection = self.Connection(loop, conn, addr, handle_receive_cb)
            self.conn[addr] = connection

    def close_connections(self):
        print('Closing connections to this TCP server', file=sys.stderr)
        # Stop listening for new connections to this socket
        self.receive_task.cancel()

        # Close each client connection
        for conn in self.conn.values():
            # Stop listening for new data to send or receive
            for task in conn.tasks:
                task.close()
            conn.sock.close()

        # Close this server's socket
        self._socket.close()

    def get_port_number(self):
        return str(self._socket.getsockname()[1])

