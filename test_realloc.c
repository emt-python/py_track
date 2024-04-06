#include <stdio.h>
#include <stdlib.h>

int main()
{
    int initialSize = 5;
    int newSize = 10;
    int i;

    // Initial allocation
    int *array = malloc(initialSize * sizeof(int));
    if (array == NULL)
    {
        perror("Initial malloc failed");
        return EXIT_FAILURE;
    }

    // Populate the array
    for (i = 0; i < initialSize; ++i)
    {
        array[i] = i;
    }

    // Resize the array
    printf("before realloc array: %p\n", array);
    int *temp = realloc(array, newSize * sizeof(int));
    printf("after realloc array: %p\n", array);
    printf("after realloc temp: %p\n", temp);
    if (temp == NULL)
    {
        perror("realloc failed");
        free(array); // Free the original array to avoid memory leak
        return EXIT_FAILURE;
    }
    array = temp;

    // Initialize new elements
    for (i = initialSize; i < newSize; ++i)
    {
        array[i] = i;
    }

    // Use the array
    for (i = 0; i < newSize; ++i)
    {
        printf("%d ", array[i]);
    }
    printf("\n");

    // Free the memory
    free(array);

    return EXIT_SUCCESS;
}
