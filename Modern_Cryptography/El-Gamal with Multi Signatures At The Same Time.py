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

def generate_keys():
    while True:
        p = random.getrandbits(20) 
        if is_prime(p):
            break
    g = find_primitive_root(p) 
    x = random.randint(1, p-2)  
    y = pow(g, x, p)# Public key y = g^x mod p
    return p, g, x, y

def split_keys(p, x, noofusers): # Not Sure it is safe need to be tested
    xi = []
    for i in range(noofusers):
        xi.append(random.randint(1, p-2)) # find strong random
    
    initial_sum = sum(xi)
    requirment = ((initial_sum // (p-2))*(p-2) + x) - initial_sum

    for i in range(noofusers):
        if requirment == 0:
            break
        if i == noofusers - 1:  
            xi[i] = (xi[i] + requirment) % (p-2)
            requirment = 0
        else:
            if requirment < 0:
                add_value = random.randint(0,abs(requirment)+1) * -1# find strong random
            else:
                add_value = random.randint(0,abs(requirment) + 1)# find strong random
            xi[i] = (xi[i] +add_value) % (p-2)
            requirment = (requirment - add_value) % (p-2)
    
    #Check Duplicate Element
    return xi

def sign(p, g, x, message):
    while True:
        k = random.randint(1, p-2)
       # if gcd(k, p-1) == 1:# k must be relatively prime to p-1
        if mod_inverse(k, p-1) is not None:
            print(k)
            break
   
    r = pow(g, k, p)
    k_inv = mod_inverse(k, p-1)
    s = (k_inv * (message - (sum(x)%(p-2)) * r)) % (p-1)
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
print("Private key x:", x,"Destroyed")

xi = split_keys(p,x,1000)#1000 people 
print("splited keys xi:", xi)
message = 123365765754674
r, s = sign(p, g, xi, message)
print("Group Signature (r, s):", r, s)
#s[-1] -= 1 
#r, s = sign(p, g, x, message)
#print("Normal Signature (r, s):", r, s)

valid = verify(p, g, y, message, r, s)
print("Is the signature valid?", valid)



