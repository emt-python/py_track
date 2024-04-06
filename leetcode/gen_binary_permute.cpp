#include <iostream>
#include <string>
#include <vector>

class Solution
{
public:
    std::vector<std::string> generateBinaryPermutations(int n)
    {
        std::vector<std::string> result;
        std::string current;
        generatePermutations(n, 0, current, result);
        return result;
    }

private:
    void generatePermutations(int n, int index, std::string &current, std::vector<std::string> &result)
    {
        if (index == n)
        {
            result.push_back(current);
            return;
        }

        // Append '0' to the current string and recurse
        current.push_back('0');
        generatePermutations(n, index + 1, current, result);
        current.pop_back(); // Backtrack

        // Append '1' to the current string and recurse
        current.push_back('1');
        generatePermutations(n, index + 1, current, result);
        current.pop_back(); // Backtrack
    }
};

int main()
{
    int n = 3;
    Solution solution;
    std::vector<std::string> permutations = solution.generateBinaryPermutations(n);

    for (const std::string &perm : permutations)
    {
        std::cout << perm << " ";
    }
    std::cout << std::endl;

    return 0;
}
