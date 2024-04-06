#include <iostream>
#include <vector>
#include <algorithm> // for make_heap, push_heap, pop_heap

int main()
{
    std::vector<int> v = {10, 20, 30, 5, 15};

    // Convert the vector into a max heap
    std::make_heap(v.begin(), v.end());

    // Now v is a max heap
    // To verify, let's print the max element
    std::cout << "Max element: " << v.front() << std::endl;

    // If you want to sort the elements in ascending order, you can use sort_heap
    // std::sort_heap(v.begin(), v.end());
    // std::cout << "Elements after sort_heap: ";
    while (!v.empty())
    {
        std::pop_heap(v.begin(), v.end());
        // int max_element = v.back();
        v.pop_back();
        for (int i : v)
        {
            std::cout << i << " ";
        }
        std::cout << std::endl;
    }

    return 0;
}
