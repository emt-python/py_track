#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#define buffer_size 8
const char *perf_stat_file = "perf_stat.log";
const char *bw_file = "parsed_bw.txt";
double dram_bw_arr[buffer_size];
double cxl_bw_arr[buffer_size];
double llc_miss_arr[buffer_size];
char llc_line[256];
char bw_line[128];
double llc_load_miss_percent = 0.0, avg_llc_miss = 0.0;
double dram_bw = 0.0, cxl_bw = 0.0, avg_cxl_bw = 0.0;
int main()
{

    int index = 0;
    while (1)
    {
        FILE *file1 = fopen(perf_stat_file, "r");
        FILE *file2 = fopen(bw_file, "r");

        if (file1 == NULL || file2 == NULL)
        {
            perror("Unable to open file");
            sleep(2);
            continue;
        }
        llc_load_miss_percent = 0.0;
        cxl_bw = 0.0;

        // read perf stat to get llc miss rate
        while (fgets(llc_line, sizeof(llc_line), file1))
        {
            if (strstr(llc_line, "LLC-load-misses") != NULL)
            {
                sscanf(llc_line, "%*[^#]# %lf%%", &llc_load_miss_percent);
                break;
            }
        }
        fclose(file1);
        if (llc_load_miss_percent == 0.0)
        {
            printf("LLC-load-misses percentage not found.\n");
        }

        // parse bw file
        if (fgets(bw_line, sizeof(bw_line), file2) != NULL)
        {
            if (sscanf(bw_line, "%lf %lf", &dram_bw, &cxl_bw) == 2)
            {
                printf("dram_bw = %.2lf, cxl_bw = %.2lf\n", dram_bw, cxl_bw);
            }
            else
            {
                printf("Failed to parse the line: %s\n", bw_line);
            }
        }
        else
        {
            fprintf(stderr, "Error reading the first line of bw file.\n");
        }
        fclose(file2);

        int num_non_zero_llc_miss = 0;
        int num_non_zero_bw = 0;
        double total_llc_miss = 0.0;
        double total_cxl_bw = 0.0;
        for (int i = 0; i < buffer_size; i++)
        {
            if (llc_miss_arr[i] != 0.0)
            {
                total_llc_miss += llc_miss_arr[i];
                num_non_zero_llc_miss++;
            }
            if (cxl_bw_arr[i] != 0.0)
            {
                total_cxl_bw += cxl_bw_arr[i];
                num_non_zero_bw++;
            }
        }
        // before new data comes, calculate average
        avg_llc_miss = (num_non_zero_llc_miss > 0) ? (total_llc_miss / num_non_zero_llc_miss) : 0.0;
        avg_cxl_bw = (num_non_zero_bw > 0) ? (total_cxl_bw / num_non_zero_bw) : 0.0;

        llc_miss_arr[index] = llc_load_miss_percent;
        cxl_bw_arr[index] = cxl_bw;
        index = (index + 1) % buffer_size;
        // if(llc_load_miss_percent >> avg_llc_miss) // do something later

        // printing
        for (int i = 0; i < buffer_size; i++)
        {
            printf("%.2lf ", llc_miss_arr[i]);
        }
        printf("\n");
        for (int i = 0; i < buffer_size; i++)
        {
            printf("%.2lf ", cxl_bw_arr[i]);
        }
        printf("\n");
        printf("index: %d, num_non_zero: %d, avg llc miss: %.2lf, avg cxl bw: %.2lf\n", index, num_non_zero_llc_miss, avg_llc_miss, avg_cxl_bw);
        printf("\n");
        sleep(1);
    }

    return 0;
}