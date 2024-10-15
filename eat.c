#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
// #include <numa.h>
// #include <numaif.h>
#include <signal.h>
void intensive_memory_operation(void *mem_block, size_t size)
{
    unsigned char *block = (unsigned char *)mem_block;
    for (size_t i = 0; i < size; i++)
    {
        unsigned char value = block[i];
        value = (value + 13) % 256;
        block[i] = value;
    }
}

int main(int argc, char *argv[])
{
    size_t mb_size = 1024L * 1024L;
    char *memory;
    void **allocated_mem = NULL;
    size_t allocated_mem_count = 0;
    for (int i = 0; i < 2048; i++)
    {
        allocated_mem = realloc(allocated_mem, (allocated_mem_count + 1) * sizeof(void *));
        void *mem = (char *)malloc(mb_size);
        // void *mem = (char *)numa_alloc_onnode(mb_size, 1);
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
    pid_t shell_pid = 0;
    if (argc > 1)
    {
        shell_pid = strtol(argv[1], NULL, 10);
        printf("Shell PID: %d\n", shell_pid);
    }
    if (shell_pid != 0)
        kill(shell_pid, SIGUSR1);
    while (1)
    {

        for (int i = 0; i < allocated_mem_count; i++)
        {
            int random_index = rand() % allocated_mem_count;
            intensive_memory_operation(allocated_mem[random_index], mb_size);
        }
    }
    for (size_t i = 0; i < allocated_mem_count; i++)
    {
        free(allocated_mem[i]);
    }
    free(allocated_mem);

    // free(memory);
    return 0;
}
