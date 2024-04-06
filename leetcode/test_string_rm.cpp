#include <iostream>
#include <string>

int main()
{
    std::string str = "0123456789";
    int index_to_remove = 5; // Index of the character to be removed

    if (index_to_remove >= 0 && index_to_remove < str.length())
    {
        // Use erase to remove the character at the specified index
        str.erase(index_to_remove, 1);

        std::cout << "Modified string: " << str << std::endl;
    }
    else
    {
        std::cout << "Invalid index to remove." << std::endl;
    }

    return 0;
}
