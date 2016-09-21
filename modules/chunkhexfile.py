from hexage import gethexage

#TODO: Make this function faster...is tooooo slooooooow 

def chunk_hexfile(filename):
    
    INHX='INX8M'
    message=''
    pic_series='16Fcode'
    message_crc=''
    cfg=''
    eeprom=''
              
    try:
        f=open(filename, 'r')
    except IOError:
        message="Can't open file:"+filename+"\n\n"
        return None
    
    age=gethexage(filename)
    hexfile=f.readlines()
    f.close()
    row_counter=1
    total=0
    
    for rec in hexfile: 
        
        if rec[0:15]==':020000040000FA':
            total=total-2

        try:
            # Read Byte count
            byte_count=eval("0x"+rec[1:3])
            
            #Calculate total bytes
            total=total+byte_count
                
            # Read register address 
            address=eval("0x"+rec[3:7])
            if address==0x400E and pic_series=='16Fcode':
                cfg='+cfg'
                
            if address>0x4200 and pic_series=='16Fcode':
                eeprom='+eeprom'
         
            # Read record type
            record_type=eval("0x"+rec[7:9])
            
            #Read Crc
            crc=eval("0x"+rec[9+2*byte_count:11+2*byte_count])
            
            # Calculate checksum
            chs=byte_count+eval("0x"+rec[3:5])+eval("0x"+rec[5:7])+record_type
            
            #Only for record data type         
            if record_type==0x00:
                pass
           
                #Check pic series mask and file check sum
                for i in range(9,9+2*byte_count,4):
                    
                    #check sun for each line
                    chs=chs+eval('0x'+rec[i:i+2])+eval('0x'+rec[i+2:i+4])
                    
                    #checkin mask of hexfile
                    mask=eval('0x'+rec[i:i+4])
                    mask=(mask)&(0x00ff)
                       
                    if mask>0x3f:
                        pic_series='18Fcode' 
                        
                #two's complement sum of the values of all fields
                chs= (1+~chs)&0xff
                 
                #Check if chs calculated an check sum readed from file are the same      
                if chs!=crc:
                    
                    message_crc ='\n Warning! CRC failed on line '+str(row_counter)+'\n'
                    print '\n Warning! CRC failed on line '+str(row_counter)+'\n',
                    
            elif record_type==0x02 and INHX!='INX32M':
                INHX='INX16M'
                
            elif record_type==0x03 or record_type==0x04:
                INHX='INX32M'
                if rec[0:15]==':020000040030CA':
                    cfg='+cfg'
                if rec[0:15]==':0200000400F00A':
                    eeprom='+eeprom'
                                    
            row_counter=row_counter+1
            
        except:
            #Check end hexfile line
            if rec[0:11] == ':00000001FF':
                pass

            # Check Hex file Start code
            if rec[0]!=":":

                if rec[0]==";":
                    message=str(rec)
                    print message,
                    
                else:
                    message="Hex file not recognized:\nLine: "+str(row_counter)+ " File: "+filename+"\n\n"
                    print message
                    return None
        
    message ='\n HEX:'+ age+' old,'+ INHX + ','+pic_series+cfg+eeprom+',total='+str(total)+ ' bytes.'
    return message

