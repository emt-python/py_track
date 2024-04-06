#include <stdio.h>
#include <unistd.h>
#include <stdint.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/mman.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/errno.h>

int ismapped(const void *ptr, int bytes)
{
    if (ptr == NULL)
    {
        return 0;
    }
    // create a pipe
    int fd[2];
    int valid = 1;
    pipe(fd);
    if (write(fd[1], ptr, bytes) < 0)
    { // try to write it, if getting outside, SEGFAULT
        if (errno == EFAULT)
        {
            valid = 0;
        }
    }
    close(fd[0]);
    close(fd[1]);
    return valid;
}

void testptr(void *p, int bytes, char *name)
{
    printf("%s:\t%d\t%p\n", name, ismapped(p, bytes), p);
}

int main()
{
    int *junk = NULL;
    int *junk2 = (int *)((uintptr_t)0x3597679009);
    int *p = malloc(50);
    int x = 5;
    int *px = &x;

    testptr(junk, 1, "junk");
    testptr(junk2, 1, "junk2");
    testptr(px, sizeof(int), "px");
    testptr(p, 50, "p");
    // *junk = 567;
}