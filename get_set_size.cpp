#include <iostream>
#include <unordered_set>

int main()
{
    std::unordered_set<int> mySet;

    // Adding elements to the set
    mySet.insert(1);
    mySet.insert(2);
    mySet.insert(3);

    // Getting the size of the set
    int setSize = mySet.size();

    std::cout << "The set contains " << setSize << " elements." << std::endl;

    return 0;
}
