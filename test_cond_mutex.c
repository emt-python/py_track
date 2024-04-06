#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t cond = PTHREAD_COND_INITIALIZER;
int state = 1; // Shared state: 1 means func1 runs, 2 means func2 runs
static int terminate_flag;
void func1()
{
    pthread_mutex_lock(&mutex); // blocked if fast holds the lock
    while (state != 1)
    {
        pthread_cond_wait(&cond, &mutex);
    }

    // func1's work here
    printf("slow is running, fast must wait\n");

    state = 2;                  // Set state to 2, indicating func2 should run next
    pthread_cond_signal(&cond); // Signal func2

    pthread_mutex_unlock(&mutex);
}

void *func2(void *arg)
{
    while (!terminate_flag)
    {
        pthread_mutex_lock(&mutex);

        while (state != 2)
        {
            pthread_cond_wait(&cond, &mutex);
        }

        // func2's work here
        printf("fast is running, slow must wait\n");

        state = 1;                  // Set state back to 1, indicating func1 should run next
        pthread_cond_signal(&cond); // Signal func1

        pthread_mutex_unlock(&mutex);
        usleep(150000);
    }
    terminate_flag = 0;
    return NULL;
}

int main()
{
    terminate_flag = 0;
    pthread_t t2;
    pthread_create(&t2, NULL, &func2, NULL);

    for (int i = 1; i < 100; i++)
    {
        func1();
        usleep(250000);
    }
    terminate_flag = 1;
    printf("main exit\n");

    pthread_join(t2, NULL);

    return 0;
}
