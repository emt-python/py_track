#include <stdio.h>
#include <stdlib.h>

#define PAGE_SIZE 4096

typedef struct
{
    int start;
    int end;
} Interval;

int isBoundaryPresent(int boundary, int *boundaries, int size)
{
    for (int i = 0; i < size; ++i)
    {
        if (boundaries[i] == boundary)
        {
            return 1;
        }
    }
    return 0;
}

int *getPageBoundaries(Interval *intervals, int intervalSize, int *boundarySize)
{
    int *boundaries = malloc(intervalSize * 2 * sizeof(int)); // Allocate maximum possible size
    *boundarySize = 0;

    for (int i = 0; i < intervalSize; ++i)
    {
        for (int j = intervals[i].start; j < intervals[i].end; j += PAGE_SIZE)
        {
            if (!isBoundaryPresent(j, boundaries, *boundarySize))
            {
                boundaries[*boundarySize] = j;
                (*boundarySize)++;
            }
        }
    }

    return realloc(boundaries, *boundarySize * sizeof(int)); // Resize to actual size
}

int main()
{
    Interval staticSet[] = {
        {4096, 12288},
        {8192, 16384}};
    int size = sizeof(staticSet) / sizeof(staticSet[0]);

    int boundarySize;
    int *boundaries = getPageBoundaries(staticSet, size, &boundarySize);

    printf("Page Boundaries:\n");
    for (int i = 0; i < boundarySize; ++i)
    {
        printf("%d\n", boundaries[i]);
    }

    free(boundaries); // Free the dynamically allocated array
    return 0;
}
