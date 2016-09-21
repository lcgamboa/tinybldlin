    #include <p18f452.inc>

CBLOCK 0X20
	ContadorA
	ContadorB
	ContadorC
ENDC

	ORG	0
	goto MAIN
	

MAIN

	BCF	TRISB,0

LOOP

	BCF	PORTB,0

	CALL DELAY
	
	BSF	PORTB,0

	CALL DELAY
	
	GOTO LOOP

DELAY

; Código de retardo generado por PikLoops (dom ago-2009-16 14:12:58)
; Tiempo de retardo = 0.09999960  con  Osc = 20.00000000MHz

retraso_.1_seg
	movlw	D'3'
	movwf	ContadorC
retraso_.1_seg_bucle
	call	sub_delay_.1_seg
	decfsz	ContadorC,1
	goto	retraso_.1_seg_bucle
	return

sub_delay_.1_seg
	movlw	D'217'
	movwf	ContadorB
	movlw	D'111'
	movwf	ContadorA
sub_delay_.1_seg_bucle
	decfsz	ContadorA,1
	goto	sub_delay_.1_seg_bucle
	decfsz	ContadorB,1
	goto	sub_delay_.1_seg_bucle
	return

	GOTO $

END

