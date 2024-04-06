#include <algorithm> // For std::sort
#include <vector>
#include <execution> // For execution policies
#include <iostream>

int main()
{
    std::vector<int> vec = {9, 3, 5, 1, 4, 8, 6, 2, 7};

    // Parallel sort
    std::sort(std::execution::par, vec.begin(), vec.end());

    // Output the sorted vector
    for (int num : vec)
    {
        std::cout << num << ' ';
    }
    std::cout << '\n';

    return 0;
}
