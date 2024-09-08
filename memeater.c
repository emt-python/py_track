#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <numa.h>
#include <numaif.h>
#include <errno.h>
#include <string.h>
#include <unistd.h>
#include <sys/sysinfo.h>
#include <signal.h>

#define DRAM_MASK 0

void allocate_until_reserved_on_node_0(size_t reserved_bytes, pid_t shell_pid)
{
    if (numa_available() == -1)
    {
        fprintf(stderr, "NUMA is not supported on this system.\n");
        exit(EXIT_FAILURE);
    }

    size_t gb_size = 1024 * 1024 * 1024;
    size_t mb_size = 1024 * 1024;
    size_t allocation_step = gb_size;

    long long free_dram_size;
    numa_node_size(DRAM_MASK, &free_dram_size);
    size_t total_allocated = 0;

    void **allocated_mem = NULL; // Array to store pointers to allocated memory
    size_t allocated_mem_count = 0;
    long long noisy_mem_bytes = 1030 * mb_size; // to accomodate extra data (400 for metadata in emt + 630 for kernel reserve)
    printf("start reserving memory\n");
    while (free_dram_size > reserved_bytes + noisy_mem_bytes)
    {
        allocated_mem = realloc(allocated_mem, (allocated_mem_count + 1) * sizeof(void *));
        if (allocated_mem == NULL)
        {
            perror("Failed to realloc memory array");
            exit(EXIT_FAILURE);
        }

        if (free_dram_size <= reserved_bytes + (2 * gb_size))
        {
            allocation_step = mb_size;
        }

        void *mem = numa_alloc_onnode(allocation_step, 0);
        if (mem == NULL)
        {
            perror("numa_alloc_onnode failed");
            exit(EXIT_FAILURE);
        }
        memset(mem, 1, allocation_step);
        allocated_mem[allocated_mem_count] = mem;
        allocated_mem_count++;

        total_allocated += allocation_step;
        numa_node_size(DRAM_MASK, &free_dram_size);
        // printf("Allocated %zu MB so far. Free memory: %lld MB. Step size: %zu MB\n",
        //        total_allocated / (1024 * 1024), free_dram_size / (1024 * 1024), allocation_step / (1024 * 1024));
    }

    printf("Reserved memory threshold reached. Remaining free memory: %lld MB\n", free_dram_size / (1024 * 1024));
    // printf("Memory allocation completed. Total allocated: %zu MB\n", total_allocated / (1024 * 1024));
    if (shell_pid != 0)
        kill(shell_pid, SIGUSR1);
    while (1)
        sleep(1);
    for (size_t i = 0; i < allocated_mem_count; i++)
    {
        numa_free(allocated_mem[i], allocation_step);
    }
    free(allocated_mem);
}

int main(int argc, char *argv[])
{
    pid_t shell_pid = 0;
    if (argc != 3)
    {
        shell_pid = 0;
    }
    else
    {
        shell_pid = strtol(argv[2], NULL, 10);
    }

    size_t reserved_mb = strtoul(argv[1], NULL, 10);
    if (reserved_mb == 0)
    {
        fprintf(stderr, "Invalid reserved memory size: %s\n", argv[1]);
        exit(EXIT_FAILURE);
    }

    size_t reserved_bytes = reserved_mb * 1024 * 1024;

    allocate_until_reserved_on_node_0(reserved_bytes, shell_pid);

    return 0;
}