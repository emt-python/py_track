#include <iostream>
#include <algorithm>
#include <vector>

int main()
{
    std::vector<int> v = {3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5};
    int n = v.size();
    int k = 6; // Number of top elements to sort

    // Partially sort the first k elements
    // This will put the top k elements in sorted order at the beginning of the vector
    std::partial_sort(v.begin(), v.begin() + k, v.end(), std::greater<int>()); // greater: desc; less: asc
    std::partial_sort(v.begin(), v.begin() + k, v.begin() + n);

    std::cout << "Top " << k << " elements sorted: ";
    for (int i = 0; i < v.size(); ++i)
    {
        std::cout << v[i] << ' ';
    }
    std::cout << '\n';

    return 0;
}
