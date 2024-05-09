#include <numa.h>
#include <numaif.h>
#include <unordered_map>
#include <iostream>
#include <thread>
#include <chrono>

#define num_entry 50000000

int main()
{
    // Check if NUMA is available
    if (numa_available() == -1)
    {
        std::cerr << "NUMA is not available on this system." << std::endl;
        return 1;
    }

    // Set the NUMA memory allocation policy to bind to node 1
    numa_set_preferred(0);

    // Optionally, check the current node
    int current_node = numa_preferred();
    std::cout << "Current preferred node: " << current_node << std::endl;

    // Create an unordered_map (after setting NUMA policies)
    std::unordered_map<int, int> myMap;

    // Populate the unordered_map
    for (size_t i = 0; i < num_entry; ++i)
    {
        myMap[i] = i * i;
    }
    std::this_thread::sleep_for(std::chrono::seconds(5));

    std::cout << "Unordered map has been populated on NUMA node " << current_node << std::endl;

    // Reset NUMA allocation to default
    numa_set_localalloc();

    return 0;
}
