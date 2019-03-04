try:
    import serial 
except ImportError:
    raise ImportError("Se requiere el modulo python-serial")
    
import glob


def detect():
    
    port_list=[]
    #TODO: recognzed other OS
    ports = glob.glob('/dev/tty[A-Za-z]*')  
    ports += glob.glob('/dev/tnt*')  

    #test if the program can use any of this ports
    for i in ports: 
     #TinyBldLin Will try to open the and send a string   
        try:
            ser=serial.Serial(i,19200,timeout=0.1)
            ser.close()
            #If TinyBldLin can open a port it will be placed in the port list
            port_list.append(i)
        except:
            continue
    return port_list
    
