#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <stdint.h>

// Function prototypes
int gcd(int a, int b);
int modInverse(int a, int m);
int power(int a, int b, int mod);

// RSA key generation, encryption, and decryption
void rsa(int message) {
    int p = 3;//101081; // First prime number
    int q = 5;//201083; // Second prime number
    int n = p * q; // Modulus for public key and private key
    int phi = (p - 1) * (q - 1); // Totient 1203408 for p = 1097 and q = 1099  2, 2, 2, 2, 3, 3, 61, 137
    int e; // Public key exponent
    int d; // Private key exponent

    // Choose e
    for (e = 2; e < phi; e++) {  // e is 5
        if (gcd(e, phi) == 1)
            break;
    }

    // Calculate d
    d = modInverse(e, phi); //d is 722045
    
    // Encryption c = (m^e) % n
    int c = power(message, e, n);

    // Decryption m = (c^d) % n
    int m = power(c, d, n);

    printf("Original Message: %d\n", message);
    printf("Encrypted message: %d\n", c);
    printf("Decrypted message: %d\n", m);
}

// Function to calculate Greatest Common Divisor
int gcd(int a, int b) {
    if (b == 0)
        return a;
    else
        return gcd(b, a % b);
}

// Function to find modular inverse
int modInverse(int a, int m) {
    a = a % m;
    for (int x = 1; x < m; x++) {
        if ((a * x) % m == 1)
            return x;
    }
    return 1; // Should not reach here
}

// Function to perform fast exponentiation
int power(int a, int b, int mod) {
    int result = 1;
    a = a % mod; 
    while (b > 0) {
        if (b % 2 == 1)
            result = (result * a) % mod;
        b = b >> 1;
        a = (a * a) % mod;
    }
    return result;
}

int main() {
    int message = 12; // Example message
    rsa(message);
    return 0;
}
