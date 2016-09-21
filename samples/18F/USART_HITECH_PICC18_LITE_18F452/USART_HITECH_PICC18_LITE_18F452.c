#include <htc.h>
#include <stdio.h>
#include "usart.h"

//Add an interruption to make tinybldlin works
void interrupt isr(){}

void main(void)
{
	unsigned char input;

	init_comms();

	printf("\nThis programs was writed using HITECH PICC LITE compiler");	
	printf("\rPress a key and I will echo it back:\n");
	
	while(1){

		input = getch();	// read a response from the user
		printf("\rI detected [%c]",input);	// echo it back

		
	}
}
