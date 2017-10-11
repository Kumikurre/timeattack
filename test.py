from string import digits, ascii_uppercase, ascii_lowercase
from itertools import product

chars = digits + ascii_uppercase + ascii_lowercase

def password_generator():
    for n in range(1, 4 + 1):
        for comb in product(chars, repeat=n):
            yield(''.join(comb))

passwords = password_generator()

for password in passwords:
    timer = input("")
    print(password)
