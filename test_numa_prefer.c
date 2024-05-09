#include <numa.h>
#include <numaif.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <time.h>

int main()
{
    // Check if NUMA is available
    if (numa_available() == -1)
    {
        fprintf(stderr, "NUMA is not available on this system.\n");
        return EXIT_FAILURE;
    }

    // Set the preferred NUMA node to 0
    numa_set_preferred(1);

    // Allocate memory using malloc
    size_t size = 1024 * 1024 * 1024 * 1; // For example, 1G
    char *data = (char *)malloc(size);
    if (!data)
    {
        perror("malloc failed");
        return EXIT_FAILURE;
    }

    // Initialize memory with memset
    memset(data, 0, size);

    printf("Memory allocated and initialized on NUMA node 0.\n");
    sleep(5);

    // Clean up
    free(data);
    numa_set_localalloc(); // Reset memory allocation policy to default
    return EXIT_SUCCESS;
}
