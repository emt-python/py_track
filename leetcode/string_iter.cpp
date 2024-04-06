#include <iostream>
#include <string>

int main()
{
    std::string str = "Hello, World!";
    std::string::iterator it = str.begin();

    while (it != str.end())
    {
        if (*it == 'o')
        {
            // Erase the 'o' character from the string and advance the iterator.
            it = str.erase(it);
        }
        else
        {
            // Move to the next character.
            ++it;
        }
    }

    std::cout << "Modified String: " << str << std::endl;

    return 0;
}
