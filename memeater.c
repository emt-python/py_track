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
#include <pthread.h>
// #define EMT_RESERVE 630 // this is with obj_temp 16 bytes
#define EMT_RESERVE 790 // this is with obj_temp 20 bytes

#define DRAM_MASK 0
void **allocated_mem = NULL;
size_t allocated_mem_count = 0;
size_t mb_size = 1024 * 1024;
unsigned int seed;
int thread_safe_rand(unsigned int *seed)
{
    return rand_r(seed);
}
int num_threads = 1; // Number of threads (adjust as needed)
void *thread_access(void *arg)
{
    int thread_id = *(int *)arg;
    size_t block_size = allocated_mem_count / num_threads;
    size_t start = thread_id * block_size;
    size_t end = (thread_id == num_threads - 1) ? allocated_mem_count : start + block_size;
    printf("block_size: %ld, start: %ld, end %ld\n", block_size, start, end);
    unsigned int local_seed = time(NULL) + thread_id;
    // while (1)
    {
        for (size_t i = start; i < end; i++)
        {
            // Generate a thread-safe random index in the range [start, end)
            int random_index = start + (thread_safe_rand(&local_seed) % (end - start));
            if (random_index < 300)
                continue;
            printf("random_index: %d, allocated_mem addr: %p\n", random_index, allocated_mem[random_index]);
            if (allocated_mem[random_index] != NULL)
            {
                memset(allocated_mem[random_index], 1, mb_size);
            }
        }
    }
    return NULL;
}
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
void allocate_until_reserved_on_node_0(size_t reserved_bytes, size_t kernel_reserved_bytes, bool reserve_extra, pid_t shell_pid)
{
    long long emt_metadata_bytes = 0;

    size_t gb_size = 1024 * 1024 * 1024;
    size_t allocation_step = mb_size;

    long free_dram_size;
    numa_node_size(DRAM_MASK, &free_dram_size);

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

        void *mem = numa_alloc_onnode(allocation_step, 0);
        if (mem == NULL)
        {
            perror("numa_alloc_onnode failed");
            exit(EXIT_FAILURE);
        }
        memset(mem, 1, allocation_step);
        allocated_mem[allocated_mem_count] = mem;
        allocated_mem_count++;

        numa_node_size(DRAM_MASK, &free_dram_size);
    }
    for (int i = 0; i < allocated_mem_count; i++)
    {
        memset(allocated_mem[i], 1, allocation_step);
    }

    printf("Reserved memory threshold reached. Remaining free memory: %ld MB\n", free_dram_size / (1024 * 1024));
    printf("allocated_mem_count: %ld\n", allocated_mem_count);
    // pthread_t threads[num_threads];
    // int thread_ids[num_threads];
    // for (int i = 0; i < num_threads; i++)
    // {
    //     thread_ids[i] = i;
    //     if (pthread_create(&threads[i], NULL, thread_access, &thread_ids[i]) != 0)
    //     {
    //         perror("Failed to create thread");
    //         exit(EXIT_FAILURE);
    //     }
    // }
    if (shell_pid != 0)
        kill(shell_pid, SIGUSR1);
    while (1)
    {

        for (int i = 0; i < allocated_mem_count; i++)
        {
            int random_index = rand() % allocated_mem_count;
            // memset(allocated_mem[random_index], 1, mb_size);
            intensive_memory_operation(allocated_mem[random_index], mb_size);
        }
    }
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
    pid_t my_pid = getpid();
    printf("memeater pid: %d\n", my_pid);

    size_t reserved_bytes = reserved_mb * 1024 * 1024;
    size_t kernel_reserved_bytes = kernel_reserved_mb * 1024 * 1024;

    allocate_until_reserved_on_node_0(reserved_bytes, kernel_reserved_bytes, reserve_extra, shell_pid);

    return 0;
}