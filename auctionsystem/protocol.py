from enum import Enum

class PROTOCOL():
    DELIMITER = ':::'

class MESSAGE(Enum):
    REGISTER = 'REGISTER'
    REGISTERED = 'REGISTERED'
    UNREGISTERED = 'UNREGISTERED'
    DEREGISTER = 'DEREGISTER'
    DEREGISTER_CONFIRM = 'DEREG-CONF'
    DEREGISTER_DENIED = 'DEREG-DENIED'
    OFFER = 'OFFER'
    OFFER_CONFIRM = 'OFFER-CONF'
    OFFER_DENIED = 'OFFER-DENIED'
    NEW_ITEM = 'NEW-ITEM'
    BID = 'BID'
    BID_OVER = 'BID-OVER'
    HIGHEST = 'HIGHEST'
    WIN = 'WIN'
    SOLD_TO = 'SOLDTO'
    NOT_SOLD = 'NOT-SOLD'



class REASON(Enum):
    VALID = (b'VALID', 'valid')
    ALREADY_REGISTERED = (b'ALRD_REGISTERED',
                          'Client name is already in the registration table')
    BAD_IP = (b'BAD-IP',
              'ip_address is not valid or is damaged')
    NOT_REGISTERED = (b'NOT_REGISTERED',
                      'Client name not found in the registration table, might not have been registered at all')
    ITEM_OFFERED = (b'ITEM_OFFERED',
                    'An item is currently being offered for auction')
    ACTIVE_BID = (b'ACTIVE_BID',
                  'Client is currently leading with the highest bid for at least one item')
    OFFER_LIMIT = (b'OFFER_LIMIT',
                   'Client cannot have more than 3 bidding_items offered for bidding simultaneously')
    NO_VALID_BIDS = (b'NO_VALID_BIDS',
                     'No valid bid exceeding the bidding_items minimum purchase price was made on the offered item')

    def __init__(self, val, string):
        self.val = val
        self.str = string

