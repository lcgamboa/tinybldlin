#ifndef _SERIAL_H_
#define _SERIAL_H_

#define BAUD 9600      
#define FOSC 20000000L
#define RX_PIN TRISCbits.TRISC7
#define TX_PIN TRISCbits.TRISC6

#define NINE 0     /* Use 9bit communication? FALSE=8bit */

#define DIVIDER ((int)(FOSC/(16UL * BAUD) -1))
#define HIGH_SPEED 1

#if NINE == 1
#define NINE_BITS 0x40
#else
#define NINE_BITS 0
#endif

#if HIGH_SPEED == 1
#define SPEED 0x4
#else
#define SPEED 0
#endif

/* Serial initialization */
#define init_comms()\
	RX_PIN = 1;	\
	TX_PIN = 1;		  \
	SPBRG = DIVIDER;     	\
	RCSTA = (NINE_BITS|0x90);	\
	TXSTA = (SPEED|NINE_BITS|0x20)

void 
putch(unsigned char byte) 
{
	/* output one byte */
	while(!PIR1bits.TXIF)	/* set when register is empty */
		continue;
	TXREG = byte;
}

unsigned char 
getch() {
	/* retrieve one byte */
	while(!PIR1bits.RCIF)	/* set when register is not empty */
		continue;
	return RCREG;	
}

unsigned char
getche(void)
{
	unsigned char c;
	putch(c = getch());
	return c;
}

void 
puts(unsigned char *str)
{ 
  unsigned char i=0;
  
  while (str[i]!=0) {
    putch(str[i]);
    i++;
  }  
}
#endif
