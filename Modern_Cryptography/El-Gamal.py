# -*- coding: utf-8 -*-
"""
Created on Sun May 26 17:41:46 2024

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

def generate_keys():
    while True:
        p = random.getrandbits(20) 
        if is_prime(p):
            break
    g = random.randint(2, p-2)  
    x = random.randint(1, p-2)  
    y = pow(g, x, p)# Public key y = g^x mod p
    return p, g, x, y

def sign(p, g, x, message):
    while True:
        k = random.randint(1, p-2)
        if gcd(k, p-1) == 1:# k must be relatively prime to p-1
            break
    r = pow(g, k, p)
    k_inv = mod_inverse(k, p-1)
    s = (k_inv * (message - x * r)) % (p-1)
    return r, s

def verify(p, g, y, message, r, s):
    if not (1 <= r <= p-1):
        return False
    v1 = pow(g, message, p)
    v2 = (pow(y, r, p) * pow(r, s, p)) % p
    return v1 == v2

#EXAMPLE
p, g, x, y = generate_keys()
print("Public key (p, g, y):", p, g, y)
print("Private key x:", x)

message = 123365765754674
r, s = sign(p, g, x, message)
print("Signature (r, s):", r, s)

valid = verify(p, g, y, message, r, s)
print("Is the signature valid?", valid)
