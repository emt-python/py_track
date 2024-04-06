#define _GNU_SOURCE
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <numaif.h> // For move_pages
#include <unistd.h> // For syscall
#include <time.h>
#include <numa.h>
#include <stdint.h>
#include <sched.h>

#define NUM_PAGES 1310720 // Example number of pages
// 10: 2621440
// 5: 1310720
// 4: 1048576
// 3: 786432
// 2: 524288
// 1: 262144
// 0.5: 131072

// Structure to hold arguments for move_pages_thread function
typedef struct
{
    unsigned long count;
    void **pages;
    int *nodes;
    int *status;
} MovePagesArgs;

// Thread function to perform move_pages
void *move_pages_thread(void *arg)
{
    MovePagesArgs *mp_args = (MovePagesArgs *)arg;

    // Call move_pages in the separate thread
    int result = move_pages(0, mp_args->count, mp_args->pages, mp_args->nodes, mp_args->status, MPOL_MF_MOVE);

    if (result < 0)
    {
        perror("move_pages failed");
    }
    else
    {
        // Optionally, handle successful move here or check status array
        for (int i = 0; i < mp_args->count; i++)
        {
            if (mp_args->status[i] < 0)
            {
                printf("Page %d failed to move with error %d\n", i, mp_args->status[i]);
            }
            // else
            // {
            //     printf("%d\n", mp_args->status[i]);
            // }
        }
    }
    // free(mp_args->pages);
    // free(mp_args->nodes);
    // free(mp_args->status);
    // free(mp_args);

    return NULL; // Thread completed
}

int main()
{
    pthread_t thread_id1, thread_id2;
    MovePagesArgs args1, args2;
    args1.count = args2.count = NUM_PAGES / 2;
    struct timespec start, end;
    double elapsed;

    void *addr = numa_alloc_onnode((long)NUM_PAGES * 4096, 1);
    memset(addr, 1, (long)NUM_PAGES * 4096);
    void **pageBoundaries = (void **)malloc(NUM_PAGES * sizeof(void *));
    for (size_t i = 0; i < NUM_PAGES; i++)
    {
        uintptr_t pageBoundary = (uintptr_t)addr + i * 4096;
        pageBoundaries[i] = (void *)pageBoundary;
    }
    args1.pages = pageBoundaries;
    args2.pages = pageBoundaries + NUM_PAGES / 2;
    int *nodes = malloc(NUM_PAGES * sizeof(int));
    for (int i = 0; i < NUM_PAGES; i++)
    {
        nodes[i] = 0;
    }
    int *status = malloc(NUM_PAGES * sizeof(int));
    args1.nodes = nodes;
    args2.nodes = nodes + NUM_PAGES / 2;
    args1.status = status;
    args2.status = status + NUM_PAGES / 2;
    if (pthread_create(&thread_id1, NULL, move_pages_thread, (void *)&args1) != 0)
    {
        perror("Failed to create thread 1");
        return -1;
    }
    if (pthread_create(&thread_id2, NULL, move_pages_thread, (void *)&args2) != 0)
    {
        perror("Failed to create thread 2");
        return -1;
    }

    // Set affinity for thread 1 to core 1
    // cpu_set_t cpuset1;
    // CPU_ZERO(&cpuset1);
    // CPU_SET(0, &cpuset1); // Assuming core IDs start at 0
    // if (pthread_setaffinity_np(thread_id1, sizeof(cpu_set_t), &cpuset1) != 0)
    // {
    //     perror("Failed to set thread 1 affinity");
    // }

    // // Set affinity for thread 2 to core 2
    // cpu_set_t cpuset2;
    // CPU_ZERO(&cpuset2);
    // CPU_SET(1, &cpuset2); // Assuming core IDs start at 0
    // if (pthread_setaffinity_np(thread_id2, sizeof(cpu_set_t), &cpuset2) != 0)
    // {
    //     perror("Failed to set thread 2 affinity");
    // }

    // Continue with the rest of the program
    // Optionally, wait for the thread to finish...
    clock_gettime(CLOCK_REALTIME, &start);
    pthread_join(thread_id1, NULL);
    pthread_join(thread_id2, NULL);
    clock_gettime(CLOCK_REALTIME, &end);
    elapsed = end.tv_sec - start.tv_sec;
    elapsed += (end.tv_nsec - start.tv_nsec) / 1000000000.0;
    printf("migrate time: %.3f\n", elapsed);

    free(pageBoundaries);
    free(nodes);
    free(status);
    numa_free(addr, (long)NUM_PAGES * 4096);

    return 0;
}
