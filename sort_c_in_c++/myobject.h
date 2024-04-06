#include <stddef.h>
#include <stdint.h>
typedef struct MyObject
{
    int id;
    long hotness;
} MyObject;
#ifndef MYOBJECT_H
#define MYOBJECT_H
#ifdef __cplusplus
extern "C"
{
#endif

    void sortMyObjects(MyObject *objects, size_t numObjects);
    void cppTopKSortObjects(MyObject *pointers, size_t k, size_t n);
    void parallelSort(MyObject *objects, size_t n);

    void sortRawAddr(uintptr_t *pointers, size_t n);
    void cppTopKSort(uintptr_t *pointers, size_t k, size_t n);

#ifdef __cplusplus
}
#endif

#endif /* MYOBJECT_H */
