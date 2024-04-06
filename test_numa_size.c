#include <stdio.h>
#include <numa.h>
#include <numaif.h>
#include <unistd.h>
#define DRAM_MASK (1 << 0)
#define TRIGGER_SCAN_WM 35
int main()
{
    if (numa_available() == -1 || numa_num_configured_nodes() < 2)
    {
        fprintf(stderr, "CXL offloading is not supported!\n");
        return 1;
    }
    long long total_dram_size, free_dram_size;
    total_dram_size = numa_node_size(DRAM_MASK, NULL);
    while (1)
    {
        if (numa_node_size(DRAM_MASK, &free_dram_size) <= 0)
        {
            fprintf(stderr, "Failed to get NUMA node size\n");
            return 1;
        }
        double freePercentage = ((double)free_dram_size / total_dram_size) * 100.0;

        if (freePercentage < TRIGGER_SCAN_WM) // 35%
        {
            fprintf(stderr, "Start triggering scan\n");
            break;
        }
        double freeMB = free_dram_size / 1048576.0;
        fprintf(stderr, "freePercentage: %.2f, no need to offload, free_dram_size: %.2f\n", freePercentage, freeMB);
        usleep(1000000);
    }

    return 0;
}
