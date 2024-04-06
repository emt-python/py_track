#include <iostream>
#include <unordered_map>

int main()
{
    std::unordered_map<int, int> myMap;

    std::cout << "Size of the empty unordered_map: " << sizeof(myMap) << " bytes" << std::endl;

    return 0;
}
