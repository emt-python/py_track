#include "sparse_wrapper.h"
#include <stdio.h>
#include <stdint.h>
// SparseHashSetHandle sparse_set = NULL;
int main()
{
    // sparse_set = create_sparse_hash_set();
    // sparse_hash_set_insert(sparse_set, 42);
    // sparse_hash_set_insert(sparse_set, 21);

    // if (sparse_hash_set_contains(sparse_set, 42))
    // {
    //     printf("Set contains 42\n");
    // }

    // delete_sparse_hash_set(sparse_set);
    insert_into_set((uintptr_t)49643534);
    if (check_in_set((uintptr_t)49643534))
    {
        printf("Set contains 49643534\n");
    }
    int size = get_set_size();
    printf("Set size is %d\n", size);
    // free_set();
    erase_from_set((uintptr_t)49643534);
    size = get_set_size();
    printf("Set size is %d\n", size);
    return 0;
}
