#include <sparsehash/sparse_hash_set>
#include <iostream>

// Define the hash set type
typedef google::sparse_hash_set<int> MyHashSet;

int main()
{
    // Create an instance of the hash set
    MyHashSet hash_set;

    // Insert elements into the hash set
    hash_set.insert(42);
    hash_set.insert(123);
    hash_set.insert(567);

    // Check if an element exists in the hash set
    if (hash_set.find(42) != hash_set.end())
    {
        // Element 42 exists in the hash set
        std::cout << "Element 42 found in the hash set." << std::endl;
    }

    // Iterate through the hash set
    for (const auto &element : hash_set)
    {
        std::cout << "Element: " << element << std::endl;
    }
    hash_set.clear();

    // Check if the hash set is empty
    if (hash_set.empty())
    {
        std::cout << "The hash set is now empty." << std::endl;
    }

    return 0;
}
