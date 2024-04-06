#include <stdio.h>

int main()
{
    short var = 0; // Example short variable

    // Set the 2nd MSB to 1
    var |= (1 << 14);
    printf("After setting 2nd MSB: %d\n", var);
    if (var & (1 << 14))
    {
        printf("The 2nd MSB is 1\n");
    }
    else
    {
        printf("The 2nd MSB is 0\n");
    }

    // Clear the 2nd MSB to 0
    var &= ~(1 << 14);
    printf("After clearing 2nd MSB: %d\n", var);
    if (var & (1 << 14))
    {
        printf("The 2nd MSB is 1\n");
    }
    else
    {
        printf("The 2nd MSB is 0\n");
    }

    // Toggle the 2nd MSB (from 0 to 1 in this case)
    var ^= (1 << 14);
    printf("After toggling 2nd MSB: %d\n", var);
    if (var & (1 << 14))
    {
        printf("The 2nd MSB is 1\n");
    }
    else
    {
        printf("The 2nd MSB is 0\n");
    }

    return 0;
}
