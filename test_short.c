#include <stdio.h>
#include <stdlib.h> // for abs function
#include <limits.h> // for SHRT_MIN and SHRT_MAX

int main()
{
    long int num1 = 1000; // Example values
    long int num2 = 3000;
    short result;

    // Perform subtraction
    long int subtraction_result = abs(num1 - num2);

    // Take absolute value
    if (subtraction_result > SHRT_MAX)
    // if (result > SHRT_MAX)
    {
        // Handle overflow or underflow
        result = -1;
    }
    else
    {
        result = (short)(subtraction_result);
    }
    printf("%d\n", result);

    return 0;
}
