import requests

def primary_attack(address, start_str, resultname, mode):
    """ address = address of the target device
        start_str = where the attack string id begins
        resultname = how should the results be named
    """
    for x in range(100000000):
        
