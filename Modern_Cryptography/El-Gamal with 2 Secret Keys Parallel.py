# -*- coding: utf-8 -*-
"""
Created on Sun May 26 18:55:42 2024

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

def find_prime_factors(n):
    s = set()
    while n % 2 == 0:
        s.add(2)
        n = n // 2
    for i in range(3, int(n**0.5) + 1, 2):
        while n % i == 0:
            s.add(i)
            n = n // i
    if n > 2:
        s.add(n)
    return s

def find_primitive_root(p):
    if not is_prime(p):
        return None
    phi = p - 1  
    prime_factors = find_prime_factors(phi)
    for g in range(2, phi + 1):
        flag = False
        for prime_factor in prime_factors:
            # Check if g^((phi)/prime) mod p is 1
            if pow(g, phi // prime_factor, p) == 1:
                flag = True
                break
        if not flag:
            return g
    return None

def generate_keys(noofuser):
    while True:
        p = random.getrandbits(20) 
        if is_prime(p):
            break
    g = find_primitive_root(p) 
    
    xi = []
    yi = []
    for user in range(noofuser):
        x = random.randint(1, p - 2)
        y = pow(g, x, p)
        xi.append(x)
        yi.append(y)

    return p, g, xi, yi

def sign(p, g, xi, message):
    ri = []
    si = []
    for x in xi:
        while True:
            k = random.randint(1, p-2)
           # if gcd(k, p-1) == 1:# k must be relatively prime to p-1
            if mod_inverse(k, p-1) is not None: 
                break
       
        r = pow(g, k, p)
        k_inv = mod_inverse(k, p-1)
        s = (k_inv * (message - x * r)) % (p-1)
        ri.append(r)
        si.append(s)
    return ri, si

def verify(p, g, y, message, ri, si):
    for i in range(len(ri)):
        if not (1 <= ri[i] <= p-1):
            return False
        v1 = pow(g, message, p)
        v2 = (pow(y[i], ri[i], p) * pow(ri[i], s[i], p)) % p
        if v1 != v2:
            return False
    
    return True


#EXAMPLE
p, g, x, y = generate_keys(2)
print("Public key (p, g, y):", p, g, y)
print("Private key x:", x)


message = 123365765754674
r, s = sign(p, g, x, message)
print("First Group Signature (r, s):", r, s)

r, s = sign(p, g, x, message)
print("Normal Signature (r, s):", r, s)

valid = verify(p, g, y, message, r, s)
print("Is the signature valid?", valid)



