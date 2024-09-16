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
#include <stdbool.h>
#define EMT_RESERVE 630

#define DRAM_MASK 0
// void allocate_until_reserved_on_node_0(size_t reserved_bytes, pid_t shell_pid)
void allocate_until_reserved_on_node_0(size_t reserved_bytes, size_t kernel_reserved_bytes, bool reserve_extra, pid_t shell_pid)
{
    long long emt_metadata_bytes = 0;

    size_t gb_size = 1024 * 1024 * 1024;
    size_t mb_size = 1024 * 1024;
    size_t allocation_step = gb_size;

    long free_dram_size;
    numa_node_size(DRAM_MASK, &free_dram_size);
    size_t total_allocated = 0;

    void **allocated_mem = NULL; // Array to store pointers to allocated memory
    size_t allocated_mem_count = 0;
    if (reserve_extra)
        emt_metadata_bytes = EMT_RESERVE * mb_size; // to accomodate extra data (emt metadata + system reserve)
    printf("start reserving memory\n");
    while (free_dram_size > reserved_bytes + emt_metadata_bytes + kernel_reserved_bytes)
    {
        allocated_mem = realloc(allocated_mem, (allocated_mem_count + 1) * sizeof(void *));
        if (allocated_mem == NULL)
        {
            perror("Failed to realloc memory array");
            exit(EXIT_FAILURE);
        }

        // if (free_dram_size <= reserved_bytes + (2 * gb_size))
        if (free_dram_size <= (10 * gb_size))
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

    printf("Reserved memory threshold reached. Remaining free memory: %ld MB\n", free_dram_size / (1024 * 1024));
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

void print_usage()
{
    printf("Usage: memeater <remaining_memory_MB> <kernel_reserved_MB> [reserve_extra] [shell_pid]\n");
    printf("Arguments:\n");
    printf("  <remaining_memory_MB>: The amount of memory (in MB) you want to remain for the workload.\n");
    printf("  <kernel_reserved_MB>: The amount of memory reserved by the kernel (in MB).\n");
    printf("  [reserve_extra]: If this is \"reserve_extra\", the program will reserve an extra 630MB for EMT metadata.\n");
    printf("  [shell_pid]: (Optional) The PID of the shell that invoked memeater. Used to determine when to launch workloads.\n");
}

// argv[1]: memory (mb) you want to remain (for workload)
// argv[2]: memory you kernel reserves (obtained thru offline)
// argv[3]: if == "reserve_extra"; then reserve 630 MB for EMT metadata
// argv[4]: if not NULL, is the shell pid who invokes the memeater, used to determine when to launch workloads
int main(int argc, char *argv[])
{
    if (numa_available() == -1)
    {
        fprintf(stderr, "NUMA is not supported on this system.\n");
        exit(EXIT_FAILURE);
    }
    if (argc > 1 && strcmp(argv[1], "--help") == 0)
    {
        print_usage();
        return 0;
    }

    if (argc < 3)
    {
        fprintf(stderr, "Error: Insufficient arguments, need at least 3 args.\n");
        print_usage();
        return 1;
    }
    long reserved_mb = strtol(argv[1], NULL, 10);
    if (reserved_mb <= 0)
    {
        fprintf(stderr, "Invalid reserved memory size: %s\n", argv[1]);
        exit(EXIT_FAILURE);
    }

    long kernel_reserved_mb = strtol(argv[2], NULL, 10);
    if (kernel_reserved_mb < 0)
    {
        fprintf(stderr, "Error: Invalid value for kernel reserved memory: %s\n", argv[2]);
        exit(EXIT_FAILURE);
    }
    bool reserve_extra = false;
    if (argc > 3 && strcmp(argv[3], "reserve_extra") == 0)
    {
        reserve_extra = true;
        printf("Reserving extra memory for EMT metadata.\n");
    }
    else
    {
        printf("Do not reserve extra\n");
    }

    pid_t shell_pid = 0;
    if (argc > 4)
    {
        shell_pid = strtol(argv[4], NULL, 10);
        printf("Shell PID: %d\n", shell_pid);
    }
    else
    {
        shell_pid = 0;
    }
    // pid_t my_pid = getpid();
    // printf("memeater pid: %d\n", my_pid);

    size_t reserved_bytes = reserved_mb * 1024 * 1024;
    size_t kernel_reserved_bytes = kernel_reserved_mb * 1024 * 1024;

    allocate_until_reserved_on_node_0(reserved_bytes, kernel_reserved_bytes, reserve_extra, shell_pid);

    return 0;
}