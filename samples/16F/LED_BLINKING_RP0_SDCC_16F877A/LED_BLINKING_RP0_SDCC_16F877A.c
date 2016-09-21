#include <pic16f877a.h>

void delay(){

	long i=0x1fff;
	while(i>0)
	{

		i--;	

	}
}


void main() 
{

	TRISB=0XFE;
	RB0=0X01;
	while(1)
	{
		delay();
		RB0=RB0^1;

	}

}
