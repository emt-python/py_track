#include "myobject.h"
#include <stdlib.h>
#include <stdio.h>
#include <time.h>

int compareMyObjects(const void *a, const void *b)
{
    const MyObject *A = (const MyObject *)a;
    const MyObject *B = (const MyObject *)b;
    return A->hotness - B->hotness;
}
#define NUM 40000000

MyObject *populate()
{
    MyObject *objects = (MyObject *)calloc(NUM, sizeof(MyObject));
    for (size_t i = 0; i < NUM; ++i)
    {
        objects[i].id = i;
        objects[i].hotness = rand() % 10000000 + 1;
    }
    return objects;
}
int main()
{
    struct timespec start, end;
    double elapsed;
    MyObject *objects;
    // objects = populate();
    // clock_gettime(CLOCK_REALTIME, &start);
    // qsort(objects, NUM, sizeof(MyObject), compareMyObjects);
    // clock_gettime(CLOCK_REALTIME, &end);

    // elapsed = end.tv_sec - start.tv_sec;
    // elapsed += (end.tv_nsec - start.tv_nsec) / 1000000000.0;
    // printf("C qsort: %.3f seconds\n", elapsed);

    free(objects);
    objects = populate();
    clock_gettime(CLOCK_REALTIME, &start);
    // sortMyObjects(objects, NUM);
    cppTopKSortObjects(objects, NUM / 3, NUM);
    clock_gettime(CLOCK_REALTIME, &end);
    elapsed = end.tv_sec - start.tv_sec;
    elapsed += (end.tv_nsec - start.tv_nsec) / 1000000000.0;
    printf("C++ partial sort: %.3f seconds\n", elapsed);

    // free(objects);
    // objects = populate();
    // clock_gettime(CLOCK_REALTIME, &start);
    // parallelSort(objects, NUM);
    // clock_gettime(CLOCK_REALTIME, &end);
    // elapsed = end.tv_sec - start.tv_sec;
    // elapsed += (end.tv_nsec - start.tv_nsec) / 1000000000.0;
    // printf("C++ parallel sort: %.3f seconds\n", elapsed);

    // Clean up after sorting
    free(objects);
    return 0;
}
