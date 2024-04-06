#include <stdio.h>
#include <stdint.h>

int main()
{
    uint32_t max_value = UINT32_MAX;
    uint32_t new_val = max_value + 1;
    uint32_t diff = new_val - max_value;
    printf("The largest value of uint32_t is: %d\n", max_value);
    printf("plus 1 is: %u\n", new_val);
    printf("diff is: %u\n", diff);

    return 0;
}
