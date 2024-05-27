# -*- coding: utf-8 -*-
"""
Created on Sun May 26 19:06:27 2024

@author: HSK
"""
import random

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(a, m):
    gcd, x, _ = extended_gcd(a, m)
    if gcd == 1:
        return x % m  
    else:
        return None

def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6   
    return True


def generate_keys(key_size):
    e = 65537
    p = q = 1
    # while not is_prime(p):
    #     p = random.randrange(2**(key_size//2), 2**(key_size//2 + 1))
    # while not is_prime(q) or p == q:
    #     q = random.randrange(2**(key_size//2), 2**(key_size//2 + 1))
    # p = 17087896287367280659160173621749326217267278844161313900219344892915400724841504636696352281067519
    # q = 481038258978798030536962935020929474236904519597637596991740376376903149974516114977626535060895685012940964979164321
    # https://en.wikipedia.org/wiki/RSA_numbers
    p = 37975227936943673922808872755445627854565536638199
    q = 40094690950920881030683735292761468389214899724061
    n = p * q
    phi_n = (p-1) * (q-1)
    d = mod_inverse(e, phi_n) #GCD(e,phi) == 1
    return ((e, n), (d, n))

def split_private_key(d, n):
    d1 = random.randint(1, d-1)
    d2 = (d - d1) % (n - 1)
    return (d1, d2)

def sign(message, d, n):
    message_int = int.from_bytes(message.encode('utf-8'), 'big')
    signature = pow(message_int, d, n)
    return signature

def partial_sign(message, d_part, n):
    message_int = int.from_bytes(message.encode('utf-8'), 'big')
    partial_signature = pow(message_int, d_part, n)
    return partial_signature

def verify_signature(message, signature, e, n):
    message_int = int.from_bytes(message.encode('utf-8'), 'big')
    verification = pow(signature, e, n)
    return verification == message_int

public_key, private_key = generate_keys(1024)
d, n = private_key
e, _ = public_key

d1, d2 = split_private_key(d, n)

message = "Hello, RSA Signature!"
part_sig1 = partial_sign(message, d1, n)
part_sig2 = partial_sign(message, d2, n)

# In RSA, because (m^d1 % n) * (m^d2 % n) = m^(d1+d2) % n = m^d % n,
# you can multiply partial signatures directly to get the valid signature.
full_signature = (part_sig1 * part_sig2) % n

# Verification
valid = verify_signature(message, full_signature, e, n)
print("Signature valid:", valid)



