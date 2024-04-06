#include <stdio.h>
static int myStaticVar;
void myFunction()
{
    myStaticVar++;
    printf("myStaticVar = %d\n", myStaticVar);
}

void incFunc()
{
    myStaticVar++;
    printf("myStaticVar = %d\n", myStaticVar);
}

int main()
{
    myFunction();
    myFunction();
    incFunc();
    return 0;
}
