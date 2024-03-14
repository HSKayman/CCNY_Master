#include <stdio.h>

#define A 1664525
#define C 1013904223
#define M 4294967296 // 2^32

unsigned long seed = 1;

void srand(unsigned long s) {
    seed = s;
}

unsigned long rand(void) {
    seed = (A * seed + C) % M;
    return seed;
}

int main() {
    // Set initial seed
    srand(1234);

    for (int i = 0; i < 10; ++i) {
        printf("%lu", rand());
    }

    return 0;
}
