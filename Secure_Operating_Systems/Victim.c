#include <stdio.h>
#include <unistd.h>

const char *secret = "TopSecretFBI";

int main() {
    FILE *f = fopen("secret_address.txt", "w");
    if (f == NULL) {
        perror("fopen");
        return 1;
    }

    printf("Victim process PID: %d\n", getpid());
    printf("Secret string address: %p\n", (void *)secret);
    fprintf(f, "%p\n", (void *)secret);
    fclose(f);

    fflush(stdout); 
    while (1) {
        sleep(1);
    }
    return 0;
}
