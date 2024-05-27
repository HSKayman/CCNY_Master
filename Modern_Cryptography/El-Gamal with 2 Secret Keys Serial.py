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

def generate_keys(noofbits,noofusers):
    while True:
        p = random.getrandbits(noofbits) 
        if is_prime(p):
            break
    #while True:
    #    q = random.getrandbits(noofbits) 
    #    if is_prime(q):
    #        break    
    q = (p-1)

    g = find_primitive_root(p) 
    xi = []
    yi = []
    for keys in range(noofusers):
        x = random.randint(1, p-2)  
        y = pow(g, x, p)# Public key y = g^x mod p
        xi.append(x)
        yi.append(y)
        
    return p, g, q, xi, yi # Checked and Done

def generate_r(p, q, g, xi): 
    k = [ 0 for i in range(len(xi))]
    r = [ 0 for i in range(len(xi))]
    
    while True:
        k[0] = random.randint(1, q-1)
        if gcd(k[0], p-1) == 1:# k must be relatively prime to p-1
       # if mod_inverse(k, p-1) is not None:
           break
       
    r[0] = pow(g,k[0],p)
    
    for i in range(1,len(xi)):
        while True:
            k[i] = random.randint(1, q-1)
            r[i] =  (pow(r[i-1], xi[i], p) * pow(g, k[i], p)) % p
            if gcd(r[i], p-1) == 1:# r[i] must be relatively prime to p-1
           # if mod_inverse(k, p-1) is not None:
               break
    return r[-1], k, r # Checked and Done

def sign(p, q, g, xi, yi, r, k, message,rlist):
    s = [ 0 for _ in range(len(xi))]
    
    s[0] = (xi[0] + k[0] * r * message) % q
    for i in range(0, len(xi)):
        if pow(g, s[i-1], p) == pow(yi[i-1], pow(rlist[i-1], r * message, p), p): #Problem here
            print("I am in at i = ",i)
            s[i] = ((s[i-1] + 1) * xi[i] + k[i] * r * message ) % q
    return s[-1]

def verify(p, q, g, y, message, r, s):
    if not (1 <= r <= p-1):
        return False
    v1 = pow(g, message, p)
    v2 = pow(y[-1], pow(r, r * message, p), p) #Problem here
    return v1 == v2


#EXAMPLE
p, g, q, x, y = generate_keys(20,2)
print("Public key (p, g, y):", p, g, y)
print("Private key x:", x)

message = 123365765754674
r, k ,rlist= generate_r(p, q, g, x)
s = sign(p, q, g, x, y, r, k, message,rlist)

print("Group Signature (r, s):", r, s)

valid = verify(p, q, g, y, message, r, s)
print("Is the signature valid?", valid)


