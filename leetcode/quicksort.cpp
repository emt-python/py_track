#include <iostream>
#include <vector>

int partition(std::vector<int> &v, int low, int high)
{
    int pivot = v[high];
    int i = (low);
    for (int j = low; j < high; j++)
    {
        if (v[j] <= pivot)
        {
            std::swap(v[i], v[j]);
            i++;
        }
    }
    std::swap(v[i], v[high]);
    return i;
}
void quickSort(std::vector<int> &v, int low, int high)
{
    if (low < high)
    {
        int p = partition(v, low, high);
        quickSort(v, low, p - 1);
        quickSort(v, p + 1, high);
    }
}

int main()
{
    std::vector<int> v = {10, 20, 30, 5, 15};
    int arrSize = v.size();
    quickSort(v, 0, v.size() - 1);
    std::cout << "Sorted Array: ";
    for (int i = 0; i < arrSize; i++)
    {
        std::cout << v[i] << " ";
    }
    std::cout << std::endl;
}
