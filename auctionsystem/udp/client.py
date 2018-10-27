import socket
import sys


def get_udp_client_socket(server_address):
    # Create a UDP socket
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print('UDP client socket created')
    except OSError as err:
        print('Failed to create client socket. Error: {0}'.format(err))
        sys.exit()

    return sock


def send(sock, msg, server_address):
    #  Send message
    sock.sendto(msg.encode(), server_address)
    print('To {0} sent: {1}'.format(server_address, msg), file=sys.stderr)


def receive(sock):
    #  Wait to receive response
    data, addr = sock.recvfrom(1024)
    print('From {0} received: {1}'.format(addr, data), file=sys.stderr)
    return data, addr


def close_socket(sock):
        print('Closing socket', file=sys.stderr)
        sock.close()
