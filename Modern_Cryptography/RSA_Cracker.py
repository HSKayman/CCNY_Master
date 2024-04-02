import sys
import math
import random
from math import sqrt, ceil
def WeirdFactor(n):
    N = n
    n = int(n**0.5)+1
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False  # 0 and 1 are not prime numbers
    
    primes = []
    square_n = int(n**0.5) + 1
    p=2
    while p < square_n :  # Check up to the square root of n
        if is_prime[p]:
            primes.append(p)
            for i in range(p*p, n + 1, p):  # Mark multiples of p as not prime
                is_prime[i] = False
        #print("Operation Finding Primes Up to N is %{:03.2f} Completed".format((p/square_n)*100),end="\r")
        p += 1
    # Append the remaining primes
    primes.extend([p for p in range(int(n**0.5) + 1, n + 1) if is_prime[p]])
    
    primesLenght=len(primes)
    print("\nFound Primes Amount :", primesLenght)
    
    i = 0
    q = 1
    while i < primesLenght:
        if(N % primes[i] == 0):
            q = primes[i]
            break
        #print("Operation Finding Matched Primes is %{:03.2f} Completed".format((i/primesLenght)*100),end="\r")
        i += 1
    p = int( N / q )
    return [q , p] if N != q else [0 , 0]

def TrialDivision(n):
    """A naive and impractical factorization method."""
    factors = []
    # Check for even numbers
    if n % 2 == 0:
        factors.extend([2])
        while n % 2 == 0:
            n //= 2
    # Check for odd factors
    p = 3
    while p * p <= n:
        if n % p == 0:
            factors.extend([p])
            while n % p == 0:
                n //= p
        p += 2
    if n > 1:
        factors.extend([n])
    return factors

N = 926767 * 925523 
print("\nResult: {} {}:".format(N, WeirdFactor(N)))
print("Result: {} {}:".format(N, TrialDivision(N)))

