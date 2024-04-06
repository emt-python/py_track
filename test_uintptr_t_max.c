#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

int main()
{
    uintptr_t max_value = UINTPTR_MAX;
    void *someptr = malloc(50);
    printf("Maximum value of uintptr_t: %lu\n", max_value);
    if ((uintptr_t)someptr < max_value)
        printf("someptr is less than max_value\n");
    else
        printf("someptr is greater than max_value\n");

    return 0;
}
