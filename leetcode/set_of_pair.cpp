#include <iostream>
#include <unordered_set>
#include <utility>

// Custom hash function for std::pair<int, int>
struct PairHash
{
    template <class T1, class T2>
    std::size_t operator()(const std::pair<T1, T2> &p) const
    {
        // Combine hashes of the two elements in the pair
        std::hash<T1> hash1;
        std::hash<T2> hash2;
        return hash1(p.first) ^ hash2(p.second);
    }
};

int main()
{
    std::unordered_set<std::pair<int, int>, PairHash> mySet;

    // Insert elements into the set
    mySet.insert(std::make_pair(1, 2));
    mySet.insert(std::make_pair(1, 3));
    mySet.insert(std::make_pair(5, 6));

    // Check if an element exists in the set
    std::pair<int, int> keyToFind = std::make_pair(3, 4);
    if (mySet.find(keyToFind) != mySet.end())
    {
        std::cout << "Element found in the set." << std::endl;
    }
    else
    {
        std::cout << "Element not found in the set." << std::endl;
    }

    return 0;
}
