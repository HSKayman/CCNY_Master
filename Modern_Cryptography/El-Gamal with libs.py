import random
from Crypto.Util.number import getPrime, GCD, inverse

def key_gen(G, P):
    # Private Key X in [1, P-2]
    X = gen_rand(1, P-2)
    # Public Key g^x mod p
    Y = pow(G, X, P)
    return X, Y

def gen_rand(min, max):
    return random.randint(min, max)

# message
M = 20240422
print("Message:", M)

# key length
N = 8
print("Key Length:", N)

# prime number
P = getPrime(N)
print("Prime Number:", P)

# generator G in [2, P-1]
G = gen_rand(2, P-1)
print("Generator:", G)

# Key generator
X, Y = key_gen(G, P)
print("Private Key:", X)
print("Public Key:", Y)

# Sign
# K in [2, P-2]
K = 0
while True:
    K = gen_rand(2, P-2)
    if GCD(K, P-1) == 1:
        break

R = pow(G, K, P)
print("Alpha:", R)
S = (M - X * R) % (P - 1)
K_inv = inverse(K, P - 1)
S = (S * K_inv) % (P - 1)
print("Signature:", S)

# Verify
GHM = pow(G, M, P)
YRRS = (pow(Y, R, P) * pow(R, S, P)) % P
verify = "False"
if GHM == YRRS:
    verify = "True"
print("Verify?", verify)

