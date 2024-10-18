#include <stdio.h>
#include <stdint.h>

int main()
{
	char *kernel_data_addr = (char*)0xfa153000; 
	char kernel_data = *kernel_data_addr; 
	printf("I have reached here.\n"); 
	return 0;
}
