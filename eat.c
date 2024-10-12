#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
// #include <numa.h>
// #include <numaif.h>
#include <signal.h>

int main(int argc, char *argv[])
{
    size_t mb_size = 1024L * 1024L;
    char *memory;
    void **allocated_mem = NULL;
    size_t allocated_mem_count = 0;
    for (int i = 0; i < 4096; i++)
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