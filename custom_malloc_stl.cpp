#include <unordered_set>
#include <numa.h>
#include <numaif.h>
#include <iostream>
#include <memory>
#include <chrono>
#include <iostream>

#define NUM 4000000
template <typename T>
class NUMAAllocator
{
public:
    using value_type = T;
    using size_type = size_t;
    using difference_type = ptrdiff_t;
    using pointer = T *;
    using const_pointer = const T *;
    using reference = T &;
    using const_reference = const T &;

    NUMAAllocator() noexcept {}

    template <typename U>
    NUMAAllocator(const NUMAAllocator<U> &) noexcept {}

    T *allocate(std::size_t n)
    {
        if (n > std::size_t(-1) / sizeof(T))
            throw std::bad_alloc();
        if (auto p = static_cast<T *>(numa_alloc_onnode(n * sizeof(T), 1)))
        {
            return p;
        }
        throw std::bad_alloc();
    }

    void deallocate(T *p, std::size_t n) noexcept
    {
        numa_free(p, n * sizeof(T));
    }

    template <typename U>
    struct rebind
    {
        using other = NUMAAllocator<U>;
    };
};

int main()
{
    if (numa_available() == -1)
    {
        std::cerr << "NUMA is not available\n";
        return 1;
    }

    std::unordered_set<int, std::hash<int>, std::equal_to<int>, NUMAAllocator<int>> mySet;
    // std::unordered_set<int> normalSet;

    auto start = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < NUM; i++)
    {
        int num = rand() % NUM;
        mySet.insert(num);
    }
    auto stop = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(stop - start);
    double runtime = duration.count() / 1000000.0; // Ensure floating-point division
    fprintf(stderr, "runtime: %.3f seconds\n", runtime);

    return 0;
}
