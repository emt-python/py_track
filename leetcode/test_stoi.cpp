#include <iostream>
#include <sstream>
#include <string>
using namespace std;

void extractInfo(const std::string &s, int &function_id, std::string &type, int &timestamp)
{
    function_id = stoi(s.substr(0, s.find(':')));
    timestamp = stoi(s.substr(s.rfind(':') + 1));
}

int main()
{
    std::string log = "0:start:3";
    int function_id;
    std::string type;
    int timestamp;

    extractInfo(log, function_id, type, timestamp);

    std::cout << "Function ID: " << function_id << std::endl;
    // std::cout << "Type: " << type << std::endl;
    std::cout << "Timestamp: " << timestamp << std::endl;

    return 0;
}
