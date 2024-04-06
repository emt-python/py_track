#define _GNU_SOURCE
#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <numaif.h>
#include <numa.h>
#include <stdint.h>
#include <errno.h>
#include <unistd.h>

#define num_pages 1310720
// 10: 2621440
// 5: 1310720
// 4: 1048576
// 3: 786432
// 2: 524288
// 1: 262144
// 0.5: 131072
int main()
{
    // int nodes[num_pages];
    int *nodes = (int *)malloc(num_pages * sizeof(int));
    if (nodes == NULL)
    {
        // Handle memory allocation failure
        return -1;
    }
    for (int i = 0; i < num_pages; i++)
    {
        nodes[i] = 0;
    }
    // int status[num_pages];
    int *status = (int *)malloc(num_pages * sizeof(int));

    void *addr = numa_alloc_onnode((long)num_pages * 4096, 1);
    // void *addr = malloc((long)num_pages * 4096);
    // Must first populate the allocated memory with some known data to
    // ensure pages are actually allocated and that they have a known state.
    memset(addr, 1, (long)num_pages * 4096);
    void **pageBoundaries = (void **)malloc(num_pages * sizeof(void *));
    for (size_t i = 0; i < num_pages; i++)
    {
        uintptr_t pageBoundary = (uintptr_t)addr + i * 4096;
        pageBoundaries[i] = (void *)pageBoundary;
    }

    // Move the pages (assuming current process, hence 0)
    // status[0] = EACCES; // 13
    // status[1] = EBUSY;  // 16
    // status[2] = EFAULT; // 14
    // status[3] = EIO;    // 5
    // status[4] = EINVAL; // 22
    // status[5] = ENOENT; // 2
    // status[6] = ENOMEM; // 12
    // printf("before moving...\n");
    // fflush(stdout);
    // usleep(5000000);
    struct timespec start, end;
    double elapsed;
    clock_gettime(CLOCK_REALTIME, &start);
    long ret = move_pages(0, num_pages, pageBoundaries, nodes, status, MPOL_MF_MOVE);
    clock_gettime(CLOCK_REALTIME, &end);
    elapsed = end.tv_sec - start.tv_sec;
    elapsed += (end.tv_nsec - start.tv_nsec) / 1000000000.0;

    if (ret < 0)
    {
        perror("move_pages fault");
        return 1;
    }
    printf("migrate time: %.3f\n", elapsed);

    // printf("after moving...\n");
    // fflush(stdout);
    // usleep(5000000);
    // int not_moved = 0;
    for (unsigned long i = 0; i < num_pages; ++i)
    {
        if (status[i] < 0)
        {
            printf("Page %lu not moved: %d\n", i, status[i]);
        }
        // else if (status[i] > 0)
        // {
        // fprintf(stderr, "%d\n", status[i]);
        // not_moved++;
        // }
    }
    // fprintf(stdout, "Pages not moved: %d\n", not_moved);

    // Clean up
    free(pageBoundaries);
    free(status);
    free(nodes);
    numa_free(addr, (long)num_pages * 4096);
    // free(addr);

    return 0;
}
