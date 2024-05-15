#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <numa.h>
#include <numaif.h>
#include <unistd.h>

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <memory in GB>\n", argv[0]);
        return 1;
    }

    double gigabytes = atof(argv[1]);
    size_t size = gigabytes * 1024 * 1024 * 1024;  // Calculate bytes

    // char *memory = malloc(size);
    char *memory = numa_alloc_onnode(size, 0);
    if (memory == NULL) {
        fprintf(stderr, "Failed to allocate %f GB of memory.\n", gigabytes);
        return 1;
    }

    // Initialize memory
    memset(memory, 0, size);
    fprintf(stderr, "%f GB of memory allocated...\n", gigabytes);
    while(1)
    {
        sleep(1);
    }

    // getchar();  // Wait for user input

    // numa_free(memory, size);
    // printf("Memory freed.\n");

    return 0;
}
