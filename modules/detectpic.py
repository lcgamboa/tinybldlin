#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
##detectpic.py Writed by Fernando Juarez V.
##
##CopyLeft  2009
##
##This program is free software: you can redistribute it and/or modify
##it under the terms of the GNU General Public License as published by
##the Free Software Foundation, either version 3 of the License, or
##(at your option) any later version.
##
##This program is distributed in the hope that it will be useful,
##but WITHOUT ANY WARRANTY; without even the implied warranty of
##MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##GNU General Public License for more details.
##
##You should have received a copy of the GNU General Public License
##along with this program.  If not, see <http://www.gnu.org/licenses/>.
################################################################################

try: 
    import serial 
    
except ImportError:

    print ("you must have python-serial installed")
    print ('if you are using Debian/Ubuntu type $sudo apt-get install python3-serial')
    

from pictype import pic_type
import time

def check_conection(PORT,BAUD):
        
    try:
        ser = serial.Serial(PORT,BAUD,timeout=0.1)
        ser.close()
        message = "\n\n Connected to " + PORT + " at " + str(BAUD)
        return True, message
        
    except:
        message = ("\n\n Could not connect to " + PORT + " at " + str(BAUD)+'\n ERROR!')
        return  False, message


def check_pic(PORT,BAUD,RESET_RTS):
       
    type=None
    max_flash=None
    family=None
    bsize=None

    ser = serial.Serial(PORT,BAUD,timeout=0.1)
    if RESET_RTS:
            ser.setRTS(1)
            time.sleep(.1)
            ser.setRTS(0)
            time.sleep(.1)

    #Ask PIC IDE
    ser.write(b'\xC1')
          
    #wait for PIC answer
    ret=ser.read(2)
    ret=ret.decode()

    #close serial port
    ser.close()

    #In case there was no answer from pic
    if len(ret)!=2:
        message='Not found, \n ERROR!'
        return type,max_flash,family,message, bsize
           
    #In case of pic not recognized
    if ret[1]!= "K":
        message="\n Error, PIC not recognized (protocol error)\n"
        return type,max_flash,family,message, bsize
        
    pt=ord(ret[0])
        
    type, max_flash, family, bsize=pic_type(pt)
    message = '\n Found:'+ type
    return type,max_flash,family,message, bsize
    
