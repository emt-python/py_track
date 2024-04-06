#include "myobject.h"

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <time.h>
#define NUM 20

// Function to compare two integers for qsort
int compare(const void *a, const void *b)
{
    const uintptr_t *pa = (const uintptr_t *)a;
    const uintptr_t *pb = (const uintptr_t *)b;
    if (*pa < *pb)
        return -1;
    if (*pa > *pb)
        return 1;
    return 0;
}

// Function to generate an array of unique page start addresses
void *unique_page_starts(uintptr_t *pointers, size_t n, size_t *num_unique)
{
    double elapsed;
    if (n == 0 || pointers == NULL)
    {
        *num_unique = 0;
        return NULL;
    }

    for (size_t i = 0; i < n; i++)
    {
        pointers[i] &= ~((uintptr_t)4095);
    }
    struct timespec start, end;
    clock_gettime(CLOCK_REALTIME, &start);
    // qsort(pointers, n, sizeof(uintptr_t), compare);
    sortRawAddr(pointers, n);
    // cppTopKSort(pointers, n / 2, n);
    clock_gettime(CLOCK_REALTIME, &end);
    elapsed = end.tv_sec - start.tv_sec;
    elapsed += (end.tv_nsec - start.tv_nsec) / 1000000000.0;
    printf("c++ default sort: %.3f seconds\n", elapsed);

    // uintptr_t *unique_starts = malloc(n * sizeof(uintptr_t));
    // if (!unique_starts)
    // {
    //     *num_unique = 0;
    //     return NULL;
    // }

    // unique_starts[j++] = pointers[0];
    // for (size_t i = 1; i < n; i++)
    // {
    //     if (pointers[i] != pointers[i - 1])
    //     {
    //         unique_starts[j++] = pointers[i];
    //     }
    // }

    size_t j = 0;
    for (size_t i = 1; i < n; ++i)
    {
        if (pointers[j] != pointers[i])
        {
            pointers[++j] = pointers[i];
        }
    }
    // clock_gettime(CLOCK_REALTIME, &start);
    if (*num_unique < n)
        pointers = realloc(pointers, j * sizeof(uintptr_t));
    *num_unique = j + 1;
    // clock_gettime(CLOCK_REALTIME, &end);
    // elapsed = end.tv_sec - start.tv_sec;
    // elapsed += (end.tv_nsec - start.tv_nsec) / 1000000000.0;
    // printf("realloc time: %.3f seconds\n", elapsed);
    printf("allocated: %ld, real: %ld\n", n, *num_unique);
}

int main()
{
    uintptr_t *pointers = calloc(NUM, sizeof(uintptr_t));
    for (size_t i = 0; i < NUM; i++)
    {
        pointers[i] = (uintptr_t)rand() % 10000000 + 1;
    }
    // void *pointers[] = {(void *)5986, (void *)116893, (void *)6000, (void *)13000};
    size_t num_unique = 0;

    unique_page_starts(pointers, NUM, &num_unique);

    if (0)
    {
        printf("Unique page starts:\n");
        for (size_t i = 0; i < num_unique; i++)
        {
            printf("%lu\n", pointers[i]);
        }
    }
    free(pointers);

    return 0;
}
