#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int main()
{
    size_t mb_size = 1024L * 1024L;
    // size_t memory_size = 2L * 1024L * mb_size;
    char *memory;
    void **allocated_mem = NULL;
    size_t allocated_mem_count = 0;
    // Allocate 2 GB of memory
    for (int i = 0; i < 4096; i++)
    {
        allocated_mem = realloc(allocated_mem, (allocated_mem_count + 1) * sizeof(void *));
        void *mem = (char *)malloc(mb_size);
        if (mem == NULL)
        {
            perror("malloc failed");
            exit(EXIT_FAILURE);
        }
        memset(mem, 1, mb_size);
        allocated_mem[allocated_mem_count] = mem;
        allocated_mem_count++;
    }

    printf("Allocated 2 GB of memory.\n");

    // Use the memory by filling it with a pattern
    // memset(memory, 0, memory_size);
    // printf("Filled 2 GB of memory.\n");

    // printf("Memory is allocated and filled. Press Ctrl+C to terminate the program.\n");
    while (1)
    {
        sleep(10); // Keep the program running and holding onto the memory
    }

    // free(memory);
    return 0;
}