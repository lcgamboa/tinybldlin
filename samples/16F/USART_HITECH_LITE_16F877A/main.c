#include <stdio.h>
#include <pic.h>
#include "usart.h"

//Add an interruption to make tinybldlin works
void interrupt isr()
{
}

void main(void){
	unsigned char input;

	INTCON=0;	// purpose of disabling the interrupts.

	init_comms();	// set up the USART - settings defined in usart.h

	// Output a message to prompt the user for a keypress
	printf("\nThis programs was writed using Hi-tech PICC-Lite C compiler");	
	printf("\rPress a key and I will echo it back:\n");
	while(1){
		input = getch();	// read a response from the user
		printf("\rI detected [%c]",input);	// echo it back
	}
}
