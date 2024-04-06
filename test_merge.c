#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <stdint.h>

#define PAGE_SIZE 4096
#define PAGE_MASK (~(PAGE_SIZE - 1))

typedef struct
{
    int start;
    int end;
} PyObj_range;

int compareIntervals(const void *a, const void *b)
{
    PyObj_range *A = (PyObj_range *)a;
    PyObj_range *B = (PyObj_range *)b;
    return A->start - B->start; // Compare by start time
}
static inline int max(uintptr_t a, uintptr_t b)
{
    return a > b ? a : b;
}

static void mergeIntervals(PyObj_range **intervalsPtr, int *size)
{
    // PyObj_range *intervals = *intervalsPtr;
    fprintf(stderr, "old_size: %d\n", *size);
    qsort(*intervalsPtr, *size, sizeof(PyObj_range), compareIntervals);

    PyObj_range *new_ranges = (PyObj_range *)malloc(*size * sizeof(PyObj_range));
    if (!new_ranges)
    {
        printf("Malloc new_ranges failed\n");
        return;
    }

    new_ranges[0].start = (*intervalsPtr)[0].start & PAGE_MASK;
    new_ranges[0].end = ((*intervalsPtr)[0].end + PAGE_SIZE - 1) & PAGE_MASK;

    int mergedIndex = 0;

    for (int i = 1; i < *size; ++i)
    {
        uintptr_t alignedStart = (*intervalsPtr)[i].start & PAGE_MASK;
        uintptr_t alignedEnd = ((*intervalsPtr)[i].end + PAGE_SIZE - 1) & PAGE_MASK;

        if (alignedStart <= new_ranges[mergedIndex].end)
        {
            new_ranges[mergedIndex].end = max(new_ranges[mergedIndex].end, alignedEnd);
        }
        else
        {
            mergedIndex++;
            // if (mergedIndex >= *size)
            // { // Added a check to prevent out-of-bounds access
            //     break;
            // }
            new_ranges[mergedIndex].start = alignedStart;
            new_ranges[mergedIndex].end = alignedEnd;
            fprintf(stderr, "start: %d, end: %d\n", new_ranges[mergedIndex].start, new_ranges[mergedIndex].end);
        }
    }

    *size = mergedIndex + 1;
    PyObj_range *newIntervals = realloc(new_ranges, (*size) * sizeof(PyObj_range));
    if (newIntervals == NULL)
    {
        free(new_ranges);
    }
    else
    {
        // free(*intervalsPtr);
        *intervalsPtr = newIntervals;
    }
    fprintf(stderr, "new_size: %d\n", *size);
}

int main()
{
    // Example usage
    PyObj_range *intervals = malloc(5 * sizeof(PyObj_range));
    intervals[1] = (PyObj_range){.start = 3000, .end = 8000};
    intervals[2] = (PyObj_range){.start = 1003420, .end = 1011866};
    intervals[0] = (PyObj_range){.start = 12288, .end = 16713};
    intervals[3] = (PyObj_range){.start = 2006840, .end = 2031416};

    int size = 4;
    mergeIntervals(&intervals, &size);

    printf("after merge\n");
    for (int i = 0; i < size; i++)
    {
        printf("Interval %d: start = %d, end = %d\n", i, intervals[i].start, intervals[i].end);
    }

    free(intervals);
    return 0;
}
