#!/usr/bin/python
# coding: latin-1
import os
import sys
try:
    import serial
except:
    print ('You need python-serial module')
try:
    import gtk
except:
    print ('You need python-gtk2 please install it...\
            \n If you are running ubuntu open a terminal and type:\
            \n sudo apt-get install python-gtk2  ')

def transfer_hex(gui,filename,port,baud,type,max_flash,family,rts,bsize):
        
    
    global s    
    s=serial.Serial(port,baud,timeout=1)
    
    pic_mem={}

    if max_flash==None:
        return  'Fail'

    try:
        f=open(filename, 'r')
    except IOError:
        print ("Can't open file:"+filename+"\n\n")
        return  'Fail'
    
    hexfile=f.readlines()
    f.close()
    le=len(hexfile)
    act=0;
    
    for rec in hexfile:
        act=act+1
       
            
        # Check for the record begining
        if rec[0]!=":":
            if rec[0]==";":
                print (rec)
                
            else:
                print ("Hex file not recognized:\nLine: "+str(act)+" File: "+filename+"\n\n")
                return  'Fail'
        if rec[0]==":":
            # Read the byte count
            byte_count=eval("0x"+rec[1:3])
                
            # Read the register address 
            # Have in mind that the phisical PIC address is half of the
            # address registered in the .hex file for the 16F familly

            address=eval("0x"+rec[3:7])
                     
            # Read the register type

            record_type=eval("0x"+rec[7:9])
          
            if rec[0:15]==':020000040030CA':
                print ('Warning: Config found just writing data')
                break
            
            if rec[0:15]==':0200000400F00A':
                print ('Warning: eeprom found just writing data')
                break

            # Only use the data register
            if record_type==0:
                for i in range(9,9+2*byte_count,2):
                    
                    data=rec[i:i+2]
                      
                    # store data in pic_mem (it uses hex file address)
                    # and move the first 4 address to the needed location
                    
                    if address < 0x08:
                        if family=="16F8XX" or family=="16F8X":
                            pic_mem[address+2*max_flash-2*bsize]=eval("0x"+data)
                            
                        if family=="18F":
                            pic_mem[address+max_flash-bsize]=eval("0x"+data)
 
                        if family=="18F" or family=="16F8XX":
                            pic_mem[address]=eval("0x"+data)
                            
                    else:
                        pic_mem[address]=eval("0x"+data)
                        
                    address=address+1
     
    # The programing block size is family dependant:
    # For the 16F8XX family the block size is 8 bytes long (check in the
    # asm file for the max block size) 
    # For the 18F family the block size is 64 byte long
  
    if family=="16F8XX":
        hblock=8 #Hex Block 8 bytes
        block=4  #PIC Block 4 instructions (8 memory positions)
        maxpos=max_flash-bsize+4
        minpos=0
        
        #searching initializaded pclath
        k=0
        pclath=0
        goto_found=0
        pic_repaid={}
        for i in range(0,8,2):
            
            if pic_mem.has_key(i):
                
                pic_repaid[k]=pic_mem[i]
                pic_repaid[k+1]=pic_mem[i+1]
                
                code=pic_mem[i+1]*0x100+pic_mem[i]
                
                #looking for a goto somewhere
                if code&0x3800==0x2800:
                    goto_found=True
                #looking clrf pclath
                elif code==0x018a:
                    pclath=2
                    
                #looking for bcf pclath,3
                elif code==0x118a:
                    pclath=pclath+1
                    
                #looking for bcf pclath,4
                elif code==0x120a:
                    pclath=pclath+1
                    
                #looking for movwf pclath
                elif code==0x008a:
                    pclath=2
                
                k=k+2
                
        if goto_found==0:
            
            message= '\n WARNING: GOTO not found in first 4 words!\
                     \n If using a compiler, maybe you should write\
                     \n some directive to enable the use of bootloaders,\
                     \n or maybe you could fix it by adding an interrupt\
                     \n handler to your program.'
            print (message)
            
            if gui != None:
                gui.write_message(message)
                
        if pclath!=2:
            
            message= '\n WARNING: PCLATH not fully initialised before GOTO! ... '
            print (message)
            
            if gui != None:
                gui.write_message(message)
                
            if k>6 or k==0:
                message= '\n could not repaid\n Maybe you should use some directive in your compiler\n to enable the use of bootloaders'
                print (message)
                if gui != None:
                    gui.write_message(message)
                        
            else:

                pic_mem[0+2*max_flash-2*bsize]=0x8a
                pic_mem[1+2*max_flash-2*bsize]=0x01
                
                if pic_repaid.has_key(0):
                    pic_mem[2+2*max_flash-2*bsize]=pic_repaid[0]
                    pic_mem[3+2*max_flash-2*bsize]=pic_repaid[1]
                    
                if pic_repaid.has_key(2):
                    pic_mem[4+2*max_flash-2*bsize]=pic_repaid[2]
                    pic_mem[5+2*max_flash-2*bsize]=pic_repaid[3]
                    
                if pic_repaid.has_key(3):
                    pic_mem[6+2*max_flash-2*bsize]=pic_repaid[4]
                    pic_mem[7+2*max_flash-2*bsize]=pic_repaid[5]           
                
                    
                message= '\n sucessfully repaired.,'
                print (message)
                if gui != None:
                    gui.write_message(message)
            
        
        #ading movlw 0x1f
        pic_mem[0]=0x1f
        pic_mem[1]=0x30
        #ading  movwf PCLATH
        pic_mem[2]=0x8a
        pic_mem[3]=0x00
        #ading goto 0x7a0
        pic_mem[4]=0xa0
        pic_mem[5]=0x2F
        

    if family=="16F8X":
        #The pic 16F87 and 16F88 do erase the program memory in blocks
        #of 32 word blocks (64 bytes)
        
        hblock=64 #Hex Block 64 bytes
        block=32  #PIC Block 32 instructions (64 memory positions)
        
        maxpos=max_flash-bsize+4
        minpos=0
        
        pic_mem[0]=0x8A
        pic_mem[1]=0x15
        pic_mem[2]=0xA0
        pic_mem[3]=0x2F
        
        
    if family=="18F":
        # The blocks have to be written using a 64 bytes boundary
        # so the first 8 bytes (reserved by TinyPic) will be re writen
        # So we have to include a goto max_flash-200+8
        goto_add=((max_flash-bsize+8)/2)
        hh_goto=(goto_add/0x10000)&0x0F
        h_goto=(goto_add/0x100)&0xFF
        l_goto=goto_add&0xFF
        
        pic_mem[0]=l_goto
        pic_mem[1]=0xEF
        pic_mem[2]=h_goto
        pic_mem[3]=0xF0+hh_goto
        block=64
        hblock=64
        maxpos=max_flash-bsize+8
        minpos=0
        
        
    l=len(pic_mem)+8
    c = l/hblock
    i=1
    
    for pic_pos in range(minpos,maxpos,block):
 
        mem_block=[255]*hblock
        write_block=False
        for j in range(0,hblock):

            #Remember .hex file address is pic_address/2 for the 16F familly
            if (family=="16F8XX") or (family == "16F8X"):
                hex_pos=2*pic_pos+j
            elif family=="18F":
                hex_pos=pic_pos+j
            else :
                print ("Error, family not suported:",family)
                return 'Fail'

            
            if pic_mem.has_key(hex_pos):
                mem_block[j]=pic_mem[hex_pos]
                write_block=True
                
        if write_block:
            
            progress = float(i)/float(c)
           
            if gui != None and progress<=1:
                gui.progress_bar.set_fraction(progress)
                
            elif gui == None and progress<=1:
                print (str(int(progress*100)) + '%  Writed')
            i=i+1
            ret=write_mem(pic_pos,mem_block,family,rts)
            if ret!="K":
                return 'Fail'
   
    s.close()
    
    return 'OK'
                
                
                
def write_mem(pic_pos,mem_block,family,rts):
    
    s.flushInput()
        
    hm=(pic_pos/256)&255
    lm=(pic_pos&255)
    rl=len(mem_block)

    if (family=="16F8XX")or(family=="16F8X"):
        # Calculate checksum
        chs=hm+lm+rl
        s.write(chr(hm)+chr(lm)+chr(rl))
        for i in range(0,rl):
        
            # Calculate checksum
            chs=chs+mem_block[i]
            
            s.write(chr(mem_block[i]))
            
        chs=((-chs)&255)
        s.write(chr(chs))

    if family=="18F":
        # Calculate checksum
        chs=hm+lm+rl
        # the pic receives 3 byte memory address
        # U TBLPTRH TBLPTRL
        # Todo: Check if U can be different to 0
        #           U TBLPTRH TBLPTRL
        s.write(chr(0)+chr(hm)+chr(lm)+chr(rl))
        for i in range(0,rl):
            # Calculate checksum
            chs=chs+mem_block[i]
            
            s.write(chr(mem_block[i]))
    
        chs=((-chs)&255)
        s.write(chr(chs))

    ret=s.read(1)
    #ret="K"
    
    if ret!="K":
        print ("Error writing to the memory position: "+ hex(pic_pos)+"\n\n")
        
    while gtk.events_pending():
        gtk.main_iteration()
        
    return ret

        
