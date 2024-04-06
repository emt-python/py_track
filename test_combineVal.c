#include <stdio.h>

int main()
{
    // Define a 4-byte variable
    unsigned int combinedValue = 0;
    unsigned int *combinedValuePtr = &combinedValue;

    // Set the most significant 2 bytes (depth)
    unsigned int depth = 123;       // Replace 123 with your desired depth value
    combinedValue |= (depth << 16); // Shift depth 16 bits to the left and set it

    // Set the lower 2 bytes (length)
    unsigned int length = 456;   // Replace 456 with your desired length value
    *combinedValuePtr |= length; // Set length directly
    *combinedValuePtr += (1 << 16);

    unsigned int length2 = 7;
    *combinedValuePtr &= 0xFFFF0000;
    // *combinedValuePtr |= length2;
    // (*combinedValuePtr)++;
    *combinedValuePtr = (*combinedValuePtr & 0xFFFF0000) | (*combinedValuePtr & 0xFFFF) + 1;

    // Extract depth and length
    unsigned int extractedDepth = (*combinedValuePtr >> 16) & 0xFFFF;
    unsigned int extractedLength = *combinedValuePtr & 0xFFFF;

    // Print the values
    // printf("Combined Value: %u\n", combinedValue);
    printf("Extracted Depth: %u\n", extractedDepth);
    printf("Extracted Length: %u\n", extractedLength);

    return 0;
}
