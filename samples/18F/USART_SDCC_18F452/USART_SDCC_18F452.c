#include <pic18f452.h>
#include "usart.h"

void main() {

	unsigned char input;

	init_comms();
	puts("\nThis program was writed using SDCC compiler");
	puts("\rPress a key and I will echo it back:\n");
	while(1)
	{
		input = getch();	// read a response from the user
		puts("\rI detected [");
		putch(input);
		putch(']');

	}

}