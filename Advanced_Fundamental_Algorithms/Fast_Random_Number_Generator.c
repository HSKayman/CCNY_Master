#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

// Implement the BIT_RAND function here, which returns 0 or 1 with equal probability.
int BIT_RAND() {
    // Replace this with your implementation of BIT_RAND.
    return rand() % 2;
}
#include<stdio.h>
long long int RAND(long long int a, long long int b) {
    if(a>b){
        b=a+b;
        a=b-a;
        b=b-a;
    }
    long long int range= b- a;
    long long int distance = range;
    long long int randomNumber=0;
    randomNumber=BIT_RAND();
    while(distance>1){
        ++distance;
        distance/=2;
        randomNumber=(randomNumber << 1)| BIT_RAND();
        if(randomNumber>range){
            randomNumber = randomNumber >> 1;
            break;    
        }
    }
    return randomNumber + a;
}

int main() {
    srand(time(NULL)); // Seed the random number generator.

   

    return 0;
}
