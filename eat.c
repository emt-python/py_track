#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int main()
{
    size_t mb_size = 1024L * 1024L;
    char *memory;
    void **allocated_mem = NULL;
    size_t allocated_mem_count = 0;
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

    printf("Allocated memory, allocated_mem_count: %ld\n", allocated_mem_count);
    int bit = 0;
    while (1)
    {

        for (int i = allocated_mem_count - 1; i >= 0; i--)
        // for (int i = 0; i < allocated_mem_count - 1; i++)
        {
            memset(allocated_mem[i], bit, mb_size);
        }
        bit = !bit;
    }

    // free(memory);
    return 0;
}