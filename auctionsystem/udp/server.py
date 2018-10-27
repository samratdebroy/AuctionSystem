import socket
import sys


def get_udp_server_socket(port_number = 10000):
    ip_address = b'localhost'
    server_address = (ip_address, port_number)

    # Create a UDP socket
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print('UDP server socket created')
    except OSError as err:
        print('Failed to create server socket. Error: {0}'.format(err))
        sys.exit()

    # Bind the socket to the port
    try:
        sock.bind(server_address)
        print('Socket binded to {0}'.format(server_address), file=sys.stderr)
    except OSError as err:
        print('Binding Failed to {0}. Error: {2}'
              .format(server_address, err), file=sys.stderr)
        sys.exit()

    return sock


def receive(sock):
        data, addr = sock.recvfrom(1024)
        print('From {0} received: {1}'.format(addr, data), file=sys.stderr)
        return data, addr


def send(sock, data, addr):
        sock.sendto(data, addr)
        print('To {0} sent: {1}'.format(addr, data), file=sys.stderr)


def close_socket(sock):
    print('Closing socket', file=sys.stderr)
    sock.close()