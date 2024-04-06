#include "myobject.h"
#include <algorithm> // for std::sort
#include <cstddef>   // for size_t

// for parallel sort
// #include "parallel_sort.h"
#include <execution>

extern "C" void sortMyObjects(MyObject *objects, size_t numObjects)
{
    std::sort(objects, objects + numObjects, [](const MyObject &a, const MyObject &b)
              {
                  return a.hotness < b.hotness; // <: ascending order; >: descending orders
              });
}

extern "C" void cppTopKSortObjects(MyObject *objects, size_t k, size_t n)
{
    std::partial_sort(
        objects, objects + k, objects + n, [](const MyObject &a, const MyObject &b)
        {
            return a.hotness < b.hotness; // <: ascending order; >: descending orders
        });
}

extern "C" void parallelSort(MyObject *objects, size_t n)
{
    std::sort(
        std::execution::par, objects, objects + n, [](const MyObject &a, const MyObject &b)
        { return a.hotness < b.hotness; });
}

// sort addr
extern "C" void sortRawAddr(uintptr_t *pointers, size_t n)
{
    std::sort(pointers, pointers + n, [](const uintptr_t &a, const uintptr_t &b)
              {
                  return a < b; // <: ascending order; >: descending orders
              });
}
extern "C" void cppTopKSortAddr(uintptr_t *pointers, size_t k, size_t n)
{
    std::partial_sort(
        pointers, pointers + k, pointers + n, [](const uintptr_t &a, const uintptr_t &b)
        {
            return a < b; // <: ascending order; >: descending orders
        });
}