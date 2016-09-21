#include <16f877A.h>
#include <stdio.h>
#fuses HS,NOWDT,PUT,NOPROTECT
#use delay(clock=20000000)
#use rs232(baud=9600, xmit=PIN_C6, rcv=PIN_C7)

void main(void)
{
	unsigned char input;

	printf("\nThis programs was writed using CCS PICC compiler");	
	printf("\rPress a key and I will echo it back:\n");
	
	while(TRUE){

		input = getch();	// read a response from the user
		printf("\rI detected [%c]",input);	// echo it back

		
	}
}