#include <18f452.h>
#fuses HS,NOWDT,PUT,NOPROTECT
#use delay(clock=20000000)

void main(void)
{

	while(TRUE){

		delay_ms(100);
		output_high(PIN_B0);
		delay_ms(100);
		output_low(PIN_B0);

		
	}
}