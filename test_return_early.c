#include <stdio.h>
#include <time.h>
#include <unistd.h>

int main()
{
    // Duration limit in seconds
    int duration_limit = 2;

    // Setup timers
    struct timespec start_time, current_time;
    clock_gettime(CLOCK_MONOTONIC, &start_time);

    // For loop
    for (int i = 0; i < 10000000; i++)
    {
        // Example operation
        int x = i * i;
        usleep(100);

        // Check the elapsed time every 10 iterations
        if (i % 10 == 0)
        {
            clock_gettime(CLOCK_MONOTONIC, &current_time);

            // Calculate elapsed time
            double elapsed = (current_time.tv_sec - start_time.tv_sec) + (current_time.tv_nsec - start_time.tv_nsec) / 1.0e9;

            // Break the loop if the duration limit is exceeded
            if (elapsed > duration_limit)
            {
                printf("Stopping loop early at iteration %d\n", i);
                break;
            }
        }
    }

    // Continue with the rest of the code
    printf("Loop has been exited\n");

    return 0;
}
