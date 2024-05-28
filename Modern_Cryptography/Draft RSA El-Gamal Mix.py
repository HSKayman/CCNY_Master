# -*- coding: utf-8 -*-
"""
Created on Sun May 26 18:55:42 2024

@author: HSK
"""

import random
import hashlib

def hash_function(message, value):
    return int.from_bytes(hashlib.sha256((str(message) + str(value)).encode()).digest(), byteorder='big')

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

def generate_keys(number_of_bit, noofuser):
    while True:
        while True:
            p = random.getrandbits(number_of_bit) 
            if is_prime(p):
                break
            
        while True:
            q = random.getrandbits(number_of_bit) 
            if is_prime(q):
                break
        N = p * q
        phi_N = (p - 1)*(q - 1)
        e = random.randint(2, phi_N - 1)  
        d = mod_inverse(e,phi_N)
        if d is not None:
            break
    
    g = random.randint(2, N - 1)   # find_primitive_root(p) 
    
    xi = []
    yi = []
    for user in range(noofuser):
        x = random.randint(1, N - 1)
        v = pow(g,x,N)
        y = pow(v, d, N)
        xi.append(x)
        yi.append(y)
    
    return g, xi, yi, N


def sign(g, N, xlist, message):
    r_list = []
    s_list = []
    for x in xlist: 
        while True:
            k = random.randint(1, N-1)
            # if gcd(k, p-1) == 1:# k must be relatively prime to p-1
            if mod_inverse(k, N-1) is not None:
                break
   
        r = pow(g, k, N)
        r_list.append(r)
    R = 1
    for ri in r_list:
        R = (R * ri) % N
        
    for i, xi in enumerate(xlist):
        si = (r_list[i] + xi * hash_function(message, R)) % N
        s_list.append(si)
    
    S = sum(s_list) % N
    return R, S

def verify(g, y, N, message, R, S, y_list):
    Y = 1
    for yi in y_list:
        Y = (Y * yi) % N
    v1 = pow(g, S, N)
    v2 = (R * pow(Y, hash_function(message, R), N)) % N
    return v1 == v2


#EXAMPLE
g, x, y, N = generate_keys(32,2)
print("Public key (g, y, N):",g, y, N)
print("Private key x:", x)

message = 12336576
R, S = sign(g, N, x, message)

valid = verify(g, y, N, message, R, S, y)
print("Is the signature valid?", valid)


