try: 
    import serial 
except ImportError:
    raise ImportError("Se requiere el modulo python-serial")

import gtk
import sys
import time

class Terminal():
        
    def __init__(self): 
        pass
              
        
    def open(self,gui,port,speed):
       
        print ('Opening port: '+port +' at '+ str(speed))
        while gtk.events_pending(): gtk.main_iteration()
        gui.close=True
        global ser
        
        ser=serial.Serial(port,speed,timeout=0.1)
        
        while self.reader(gui)==True:
            pass
        ser.flushInput()
        ser.flushOutput()
        ser.close()
        print ('Terminal Closed')
        while gtk.events_pending(): gtk.main_iteration()
            

    def close(self,gui):
        gui.close=False

    def reader(self,gui):
       
        data = ser.read(1)   
        if len(data)!=0:
            if gui.rx_type_combo.get_active_text()=='char':   
                #sys.stdout.write(data)
                self.write_message(gui,data)
            else:
                hexa_data=str(hex(ord(data)))[2:]+' '
                if len(hexa_data)==2:
                    hexa_data='0'+hexa_data
                self.write_message(gui,hexa_data) 
                
        if gui.close==False:
            return False
        
        while gtk.events_pending(): gtk.main_iteration()    
        return True
    
    def terminal_type(self,data):
        ser.write(chr(data))

    def clear_terminal(self,gui):
        #get message buffer
        buffer=gui.terminal.get_buffer()
        start, end = buffer.get_selection_bounds()
        textbuffer.delete(start, end)
        
    def send_data(self,data):
        for i in range(0,len(data)):
            ser.write(data[i])
            time.sleep(0.1)
            while gtk.events_pending(): gtk.main_iteration()
            
    def write_message(self,gui,message):

        try:
            #get message buffer
            buffer=gui.terminal.get_buffer()
            #get end iter
            end=buffer.get_end_iter()
            #insert message to buffer
            buffer.insert(end,message)
            #scroll down message tab
            gui.terminal.scroll_mark_onscreen(buffer.get_insert())
        except:
            return


