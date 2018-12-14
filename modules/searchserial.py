try: 
    import serial 
except ImportError:
    raise ImportError("Se requiere el modulo python-serial")


def detect():
    
    port_list=[]
    #TODO: recognzed other OS
       
    #test if the program can use any of this ports
    for i in ("/dev/ttyS0","/dev/ttyS1","/dev/ttyS2","/dev/ttyS3","/dev/ttyS4","/dev/ttyUSB0","/dev/ttyUSB1","/dev/ttyUSB2","/dev/ttyUSB3","/dev/ttyUSB4"):     
        #TinyBldLin Will try to open the and send a string   
        try:
            ser=serial.Serial(i,19200)
            ser.write("P")
            ser.close()
            #If TinyBldLin can open a port it will be placed in the port list
            port_list.append(i)
           
        except:
            continue
 
    return port_list
    
