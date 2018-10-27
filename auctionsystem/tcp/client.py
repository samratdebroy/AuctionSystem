import socket
import sys


def get_tcp_client_socket(server_address):
    # Create a TCP socket
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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


def send(sock, msg):
    #  Send message
    sock.sendall(msg.encode())
    print('sent: {0}'.format(msg), file=sys.stderr)


def receive(sock):
    #  Wait to receive response
    data = sock.recvfrom(1024)
    print('received: {0}'.format(data), file=sys.stderr)
    return data


def close_socket(sock):
        print('Closing socket', file=sys.stderr)
        sock.close()
