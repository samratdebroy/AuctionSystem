import socket
import sys


def get_tcp_server_socket(port_number = 10000):
    ip_address = b'localhost'
    server_address = (ip_address, port_number)

    # Create a TCP socket
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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

    # TODO: expand this to support multiple clients
    sock.listen(1)
    conn, addr = sock.accept()
    return conn, addr


def receive(conn):
    data = conn.recv(1024)
    print('Received: {0}'.format(data), file=sys.stderr)
    return data


def send(conn, data):
    conn.sendall(data)
    print('To all sent: {0}'.format(data), file=sys.stderr)


def close_connection(conn):
    print('Closing connection', file=sys.stderr)
    conn.close()