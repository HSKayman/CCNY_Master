import numpy as np
import cmath

def FFT(P, w):
    n = len(P)
    if n == 1:
        return P
    P_even = FFT(P[::2], w*w)
    P_odd = FFT(P[1::2], w*w)
    twiddle_factors = [w**i for i in range(n)]
    return [P_even[i] + twiddle_factors[i]*P_odd[i] for i in range(n//2)] + [P_even[i] - twiddle_factors[i]*P_odd[i] for i in range(n//2)]

def IFFT(P, w):
    n = len(P)
    return [p/n for p in FFT(P, w.conjugate())]

def multiply_polynomials(P, Q):
    n = len(P) + len(Q) - 1
    w = cmath.exp(2j * cmath.pi / n)
    P += [0] * (n - len(P)+1)
    Q += [0] * (n - len(Q)+1)

    P_val = FFT(P, w)
    Q_val = FFT(Q, w)
    R_val = [P_val[i] * Q_val[i] for i in range(n)]
    return [round(p.real) for p in IFFT(R_val, w)]

def find_polynomial(sequence):
    P = [1]
    for a in sequence:
        Q = [1, -a]
        P = multiply_polynomials(P, Q)
        print(P,Q)
    return P

sequence = [1, 2,3,4,5,6,7,8]
coefficients = find_polynomial(sequence)
print(coefficients)
def a(a,seq):
    j=0
    result=0
    for i in seq:
        result+=(a**j)*i
        j+=1
    return result
    