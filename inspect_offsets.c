#include <stdio.h>
#include <stddef.h>

typedef struct
{
    int field1;
    double field2;
    char field3;
} MyStruct;

int main()
{
    size_t offset_field1 = offsetof(MyStruct, field1);
    size_t offset_field2 = offsetof(MyStruct, field2);
    size_t offset_field3 = offsetof(MyStruct, field3);

    printf("Offset of field1: %zu\n", offset_field1);
    printf("Offset of field2: %zu\n", offset_field2);
    printf("Offset of field3: %zu\n", offset_field3);

    return 0;
}
