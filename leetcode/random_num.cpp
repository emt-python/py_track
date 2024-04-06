#include <iostream>
#include <cstdlib> // for rand and srand
#include <ctime>   // for time

int main()
{
    int count = 3; // Example range: Select a number from 1 to 9

    // Seed the random number generator
    srand(time(0));

    // Generate and print a random number in the range 1 to count-1
    int randomNumber = 1 + rand() % (count);
    std::cout << "Random Number: " << randomNumber << std::endl;

    return 0;
}