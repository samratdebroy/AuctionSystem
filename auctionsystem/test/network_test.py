import unittest
from multiprocessing import Process
from auctionsystem import client, server


# class NetworkTests(unittest.TestCase):
#     pass


def start_server():
    server.AuctionServer()


def start_client():
    client.AuctionClient()


if __name__ == '__main__':
    process_server = Process(target=start_server)
    process_client = Process(target=start_client)

    process_server.start()
    process_client.start()


