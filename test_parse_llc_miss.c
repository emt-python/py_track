#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h> // For sleep()
#define buffer_size 8
int main()
{
    const char *filename = "perf_stat.log";
    double llc_miss_arr[buffer_size];
    char line[256];
    double llc_load_miss_percent = 0.0, avg_llc_miss = 0.0;
    int index = 0;

    while (1)
    {
        FILE *file = fopen(filename, "r");

        if (file == NULL)
        {
            // If the file cannot be opened, print an error and wait for 2 seconds
            perror("Unable to open file");
            sleep(2); // Wait for 2 seconds before retrying
            continue;
        }
        llc_load_miss_percent = 0.0;

        // Read the file line by line
        while (fgets(line, sizeof(line), file))
        {
            // Look for the line that contains "LLC-load-misses"
            if (strstr(line, "LLC-load-misses") != NULL)
            {
                // Extract the percentage after the `#` symbol
                sscanf(line, "%*[^#]# %lf%%", &llc_load_miss_percent);
                break; // Exit the loop after finding the line
            }
        }

        fclose(file);
        int num_non_zero = 0;
        double total_llc_miss = 0.0;
        for (int i = 0; i < buffer_size; i++)
        {
            if (llc_miss_arr[i] != 0.0)
            {
                total_llc_miss += llc_miss_arr[i];
                num_non_zero++;
            }
        }
        // before new data comes, calculate average
        avg_llc_miss = (num_non_zero > 0) ? (total_llc_miss / num_non_zero) : 0.0;

        llc_miss_arr[index] = llc_load_miss_percent;
        // if(llc_load_miss_percent >> avg_llc_miss) // do something
        index = (index + 1) % buffer_size;
        if (llc_load_miss_percent == 0.0)
        {
            printf("LLC-load-misses percentage not found.\n");
        }
        // printing
        for (int i = 0; i < buffer_size; i++)
        {
            printf("%.2lf ", llc_miss_arr[i]);
        }
        printf("num_non_zero: %d, avg: %.2lf\n", num_non_zero, avg_llc_miss);
        sleep(2);
    }

    return 0;
}