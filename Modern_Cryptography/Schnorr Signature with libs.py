# -*- coding: utf-8 -*-
"""
Created on Sun May 26 23:34:37 2024

@author: HSK
"""

from ecdsa import SigningKey, SECP256k1
import hashlib

def hash_function(data):
    """ Creates a SHA-256 hash of the given data. """
    return int(hashlib.sha256(data).hexdigest(), 16)

def schnorr_sign(message, private_key):
    """ Generates a Schnorr signature. """
    # Generate nonce k
    k = SigningKey.generate(curve=SECP256k1)
    k_int = int.from_bytes(k.to_string(), 'big')
    
    # Compute R = kG
    R = k.get_verifying_key().pubkey.point
    R_x = R.x()
    
    # Compute the hash e = Hash(R_x | message)
    e = hash_function((str(R_x).encode() + message.encode()))
    
    # Compute s = k - xe mod order
    x = int.from_bytes(private_key.to_string(), 'big')
    s = (k_int - x * e) % SECP256k1.order
    
    return (R_x, s)

def schnorr_verify(message, signature, public_key):
    """ Verifies a Schnorr signature. """
    R_x, s = signature
    e = hash_function((str(R_x).encode() + message.encode()))
    
    # Compute sG
    sG = SECP256k1.generator * s
    
    # Compute eY
    eY = public_key.pubkey.point * e
    
    # Verify if sG + eY is R
    R = sG + eY
    return R.x() == R_x

# Usage example
sk = SigningKey.generate(curve=SECP256k1)
pk = sk.get_verifying_key()

message = 'Hello, world!'
signature = schnorr_sign(message, sk)
print("Signature:", signature)

valid = schnorr_verify(message, signature, pk)
print("Signature valid:", valid)


