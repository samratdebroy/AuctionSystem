import tkinter as tk
import string
import random
from auctionsystem.protocol import *


# Auxiliary functions
def get_truncated_entry(entry, length):
    # Truncate the text
    text = entry.get()
    text = text[:length]
    # Ensure that the Protocol delimiter is not inputted into the text
    # Otherwise clients could manipulate bit data like SQL injections
    text = text.replace(PROTOCOL.DELIMITER, '')
    entry['text'] = text
    return text


def gen_rand_str(length):
    rand_name = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    return rand_name
