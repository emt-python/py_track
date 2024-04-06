#include <iostream>
#include <vector>
#include <algorithm>

int main()
{
    std::vector<int> nums = {1, 2, 2, 3, 3, 4, 4, 5, 6, 6};

    // Use std::unique to remove consecutive duplicates
    std::vector<int>::iterator it = std::unique(nums.begin(), nums.end());

    // Calculate the index to which 'it' points
    int index = std::distance(nums.begin(), it);

    std::cout << "Index to which 'it' points: " << index << std::endl;

    // Print the vector after removing duplicates
    for (int num : nums)
    {
        std::cout << num << " ";
    }

    return 0;
}
