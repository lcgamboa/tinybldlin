#include <pic18f452.h>

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
	PORTBbits.RB0=0X01;
	while(1)
	{
		delay();
		PORTBbits.RB0=PORTBbits.RB0^1;

	}

}
