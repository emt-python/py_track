#include <sys/time.h>
#include <stdio.h>

#include <time.h>
#include <unistd.h>

int main()
{
    // clock_t update_prev_refcnt_start = clock();
    // usleep(1000000);
    // clock_t update_prev_refcnt_end = clock();
    // double update_prev_refcnt_time = (double)(update_prev_refcnt_end - update_prev_refcnt_start);
    // printf("%f\n", update_prev_refcnt_time);

    // struct timeval start, end;
    // unsigned int elapsedTime;
    // double elapsedTime_sec;

    // gettimeofday(&start, NULL);

    // usleep(1000000);

    // gettimeofday(&end, NULL);

    // elapsedTime = (end.tv_sec - start.tv_sec) * 1000000;
    // elapsedTime += (end.tv_usec - start.tv_usec);

    // elapsedTime_sec = (end.tv_sec - start.tv_sec) + (end.tv_usec - start.tv_usec) / 1000000.0;

    // printf("Elapsed time: %u microseconds\n", elapsedTime);
    // printf("Elapsed time: %lf seconds\n", elapsedTime_sec);
    unsigned int a = 9;
    unsigned int b = 18;
    int c = a - b;
    printf("%d\n", c);

    return 0;
}
