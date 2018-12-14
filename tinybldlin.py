#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

###############################################################################
##tinybldlin.py Writed by Fernando Juarez V.
##              modified by Luis Claudio Gamboa Lopes
##CopyLeft  2016
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
###############################################################################

import os
import sys
from gi.repository import GObject as gobject
sys.path.append("modules")
import searchserial
import detectpic
import loadsavesettings
import chunkhexfile
import transferhex
import time
import browse
import terminal


try:
    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk as gtk
except:
    print( 'You need python-gtk2 please install it...\
            \n If you are running ubuntu open a terminal and type:\
            \n sudo apt-get install python-gtk2  ')
            


path_images='modules/images/'
blue=path_images+'blue.ico'
red=path_images+'red.ico'
green=path_images+'green.ico'
yellow=path_images+'yellow.ico'


class Tinybldlin():
    
    global options
    global GUI
    options = sys.argv
    if len(options)<2:
        GUI=True
        
    else:
        GUI=False
        
    def __init__(self):
        
        if GUI==True:
    
            #Getting Tinybldlin from glade file
            builder = gtk.Builder()
            builder.add_from_file("glade/Tinybldlin.glade")

            #Automagicaly connecting signals
            builder.connect_signals(self)

            #getting widgets from Tinybldlin
            self.window1            = builder.get_object("window1")
            self.speed_combo        = builder.get_object('speed_combo')
            self.hexfile_combo      = builder.get_object('hexfile_combo')
            self.port_list          = builder.get_object('port_list')
            self.port_entry         = builder.get_object('port_entry')
            self.checkpic_button    = builder.get_object('checkpic_button')
            self.abort_button       = builder.get_object('abort_button')
            self.messages           = builder.get_object('messages')
            self.progress_bar       = builder.get_object('progressbar')
            self.chunk_hexfile      = builder.get_object('chunk_hexfile')
            self.rts_checkbutton    = builder.get_object('rts_checkbutton')
            
            self.open_terminal      = builder.get_object('open_terminal_button')
            self.close_terminal     = builder.get_object('close_terminal_button')
            self.clear_terminal     = builder.get_object('clear_terminal_button')
            self.send_data          = builder.get_object('send_terminal_button')
            self.terminal           = builder.get_object('terminal')
            
            self.tx_type_combo      = builder.get_object('tx_type_combo')
            self.rx_type_combo      = builder.get_object('rx_type_combo')
            self.tx_data_combo      = builder.get_object('tx_data_combo')
            
            self.terminal_window    = builder.get_object('scrolled_terminal_window')
            self.speed_terminal_combo     =builder.get_object('speed_terminal_combo')
            
            self.terminal_data_entry= self.tx_data_combo.get_child()
            
            self.terminal_data_entry.connect("activate", self.on_terminal_data_entry, self.terminal_data_entry)
            
            self.window1.show()

            #setting model to hexfile comboboxentry
            model = gtk.ListStore(str)
            self.hexfile_combo.set_model(model)
            #FIXME self.hexfile_combo.set_text_column(0)
            self.hex_file_entry=self.hexfile_combo.get_child()

            #Populating baud rates combo
            speeds = ('115200','57600','38400','19200','9600')
            self.set_model_from_list(self.speed_combo,speeds)
            self.set_model_from_list(self.speed_terminal_combo,speeds)
            self.speed_combo.set_active(0)
            self.speed_terminal_combo.set_active(0)
            speed_entry= self.speed_combo.get_child()
            speed_terminal_entry= self.speed_terminal_combo.get_child()
            
            #Populating Rx Tx data types
            tx_data_types = ('char','char\\','Type','TypEcho')
            rx_data_types = ('char','Hex')
            self.set_model_from_list(self.tx_type_combo,tx_data_types)
            self.set_model_from_list(self.rx_type_combo,rx_data_types)
            self.tx_type_combo.set_active(0)
            self.rx_type_combo.set_active(0)
            #making status icon
            self.status_icon = gtk.StatusIcon()
            self.status_icon.set_from_file(blue)

            #trying to restore settigs
            try:
                hex_file_path=loadsavesettings.get_restore_settings("FILES", "hexfile")
                self.hex_file_entry.set_text(hex_file_path)

                baud_rate=loadsavesettings.get_restore_settings("PIC", "comspeed")
                speed_entry.set_text(baud_rate)

                last_port=loadsavesettings.get_restore_settings("PIC", "comport")
                self.port_entry.set_text(last_port)
                
                chf_state=loadsavesettings.get_restore_settings("OPTIONS", "chf")
                self.chunk_hexfile.set_active(int(chf_state))
                
                rts_state=loadsavesettings.get_restore_settings("OPTIONS", "rts")
                self.rts_checkbutton.set_active(int(rts_state))
                
                speed_terminal=loadsavesettings.get_restore_settings("TERMINAL", "speed")
                speed_terminal_entry.set_text(speed_terminal)
                
            except:
                print ('probably theres no .tinybld')

            #defining some inter variables
            self.want_to_abort=False
            self.close=0
            self.go=1
            self.text_back=''
            
            
        else:
            file,port,baud,rts,check= self.treat_args(options)
            print (file,port,baud,rts,check)
            if file==None:
                sys.exit()
            if check==1:
                self.check_pic_terminal(port,baud,rts)
                
            else:
                self.tranfer_file(file,port,baud,rts)
            sys.exit()
            
    def on_browse_button_clicked(self,widget):

        hex_path=browse.browse_hexfile(Tinybldlin,self.hexfile_combo.get_active_text())
        if hex_path != '': 
            self.hexfile_combo.insert_text(0,hex_path)
            self.hexfile_combo.set_active(0)
            
    def on_write_button_clicked(self, widget):
        begin=time.strftime("%H:%M", time.localtime())
        PORT=self.port_entry.get_text()
        BAUD=self.speed_combo.get_active_text()
        hex_file_path=self.hex_file_entry.get_text()
        
        #checking if there's port availeble
        c,message=detectpic.check_conection(PORT, BAUD)

        #If tinybld cant connect to selected port return error message
        if c==False:
            print (message)
            self.write_message(message)
            while gtk.events_pending():
                gtk.main_iteration()
            self.abort_button.hide()
            self.status_icon.set_from_file(red)
            gobject.timeout_add(2000, self.on_timeout)
            return 

        else:
            self.status_icon.set_from_file(yellow)
            self.write_message(message)
            while gtk.events_pending():
                gtk.main_iteration()
        
        if self.chunk_hexfile.get_active():
            
            message = chunkhexfile.chunk_hexfile(hex_file_path)
            if message==None:
                self.write_message('\nChoose a valid hexfile')
                while gtk.events_pending():
                    gtk.main_iteration()
                
            else:
                self.write_message(message)
                while gtk.events_pending():
                    gtk.main_iteration()
                
        self.write_message('\n Searching for PIC ...')
                
        #Reset PIC by software
        RESET_RTS=self.rts_checkbutton.get_active()
        for i in range(0,15):

            progress = (i+1)/15.0

            while gtk.events_pending():
                gtk.main_iteration()
                self.progress_bar.set_fraction(progress)

            print ('Not found press PIC reset...')
            
            type,max_flash,family,message,bsize=detectpic.check_pic(PORT,BAUD,RESET_RTS)

            if max_flash!=None:
                break

            if self.want_to_abort:
                self.want_to_abort=False
                break

        #if after ask several times PIC ide tinybld dont have a vali max_flask
        #return an error message
        if max_flash==None:
            self.write_message(message)
            self.abort_button.hide()
            self.status_icon.set_from_file(red)
            self.progress_bar.set_fraction(0)
            gobject.timeout_add(2000, self.on_timeout)
            return
        
        else:
            self.write_message(message)
            while gtk.events_pending():
                gtk.main_iteration()
                
        #Reset PIC by software
        rts=self.rts_checkbutton.get_active()
        
        start = time.time()
        #Transfering file
        write_status=transferhex.transfer_hex(Tinybldlin,hex_file_path,PORT,BAUD,type,max_flash,family,rts,bsize)
        end = time.time()
        
        if write_status=='OK':
            self.write_message('\n Write OK at ' +str(begin)+' time: '+str(end-start)[0:5]+' sec')
                  
        self.progress_bar.set_fraction(0)
        self.abort_button.hide()
        self.status_icon.set_from_file(green)
        gobject.timeout_add(2000, self.on_timeout)
 
    def on_checkpic_button_clicked(self, widget):
       
        print 
        #Showing abort button
        self.abort_button.show()

        #Getting serial port and boud rate values
        PORT=self.port_entry.get_text()
        BAUD=self.speed_combo.get_active_text()

        #Asigning some variables
        type,max_flash,family=None,None,None

        #checking if there's port availeble
        c,message=detectpic.check_conection(PORT, BAUD)

        #If tinybld cant connect to selected port return error message
        if c==False:
            print (message)
            self.write_message(message)
            self.abort_button.hide()
            self.status_icon.set_from_file(red)
            gobject.timeout_add(2000, self.on_timeout)
            return type,max_flash,family

        else:
            self.status_icon.set_from_file(yellow)
            self.write_message(message)
        
        self.write_message('\n Searching for PIC ...')
        
        #Reset PIC by software
        RESET_RTS=self.rts_checkbutton.get_active()
   
        for i in range(0,15):

            progress = (i+1)/15.0
            while gtk.events_pending():
                gtk.main_iteration()
                self.progress_bar.set_fraction(progress)

            type,max_flash,family,message,bsize=detectpic.check_pic(PORT,BAUD,RESET_RTS)

            if max_flash!=None:
                break

            if self.want_to_abort:
                self.want_to_abort=False
                break
            
            print ('Not found press PIC reset...')

        #if after ask several times PIC ide tinybld dont have a vali max_flask
        #return an error message
        if max_flash==None:
            print (message)
            self.write_message(message)
            self.abort_button.hide()
            self.status_icon.set_from_file(red)
            self.progress_bar.set_fraction(0)
            gobject.timeout_add(2000, self.on_timeout)
            return type,max_flash,family

        print (message)
        
        self.write_message(message)
        self.progress_bar.set_fraction(0)
        self.abort_button.hide()
        self.status_icon.set_from_file(green)
        gobject.timeout_add(2000, self.on_timeout)
        return type,max_flash,family

        
    def on_abort_button_clicked(self, widget):
        print ('aborted')
        self.want_to_abort=True
        
    def on_search_button_clicked(self, widget):
           
        ports = searchserial.detect()
        if ports==[]:
            self.write_message('\n No serial ports detected')
            self.port_entry.set_text('')
            return
        store= gtk.ListStore(str)
        
        for disp in ports:
            store.append([disp])
            
        self.port_list.set_model(store)
        rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn('Ports', rendererText, text=0)
        self.port_list.append_column(column)
        self.port_entry.set_text(ports[0])
                
    def on_textview1_key_press_event(self, widget, key):
        
        print ('on_textview1_key_press_event')
        
    def on_rts_checkbutton_toggled(self, widget):
        return
        
    def set_model_from_list (self, cb, items):
        """Setup a ComboBox or ComboBoxEntry based on a list of strings."""           
        model = gtk.ListStore(str)
        for i in items:
            model.append([i])
        cb.set_model(model)
        #if type(cb) == gtk.ComboBoxText:
            #FIXME cb.set_text_column(0)
        #el
        if type(cb) == gtk.ComboBox:
            cell = gtk.CellRendererText()
            cb.pack_start(cell, True)
            cb.add_attribute(cell, 'text', 0)
            
    def on_port_list_row_activated(self, widget, row ,col):
        model = widget.get_model()
        text = model[row][0]
        self.port_entry.set_text(text)
        
    def write_message(self,message):
        #get message buffer
        buffer=self.messages.get_buffer()
        #get end iter
        end=buffer.get_end_iter()
        #insert message to buffer
        buffer.insert(end,message)
        #scroll down message tab
        self.messages.scroll_mark_onscreen(buffer.get_insert())
  
    def on_timeout(self):
        self.status_icon.set_from_file(blue)
        self.want_to_abort=False
        return False
    
    def treat_args(self,options):
        file,port,baud,rts,check= None, '/dev/ttyUSB0', 115200,0,None
         
        try:             
            for i in range(1,len(options)):
                
                if options[i].startswith('-'):
                    
                    opt=options[i][1:]                    
                    if opt=='version' or opt=='-version':
                        print ('Version 0.7')
                        
                    elif opt=='help' or opt=='-help':
                        print   ('--version : Prints the version number\
                                \n--help    : Display this help\
                                \n--file yourhexfile.hex or -file yourhexfile.hex : Intel Hex formated file to be bootloaded\
                                \n--port PORT or -port PORT : Set your serial port; default: /dev/ttyUSB0\
                                \n--baud BAUD or -baud BAUD : Baud rate to be used during communication; default: 115200 \
                                \n--rts 1,0 or -rts 1,0 : Set RTS on/off ') 
                        return file,port,baud,rts,check
                                
                    elif opt=='file' or opt=='-file' or opt=='f' or opt=='-f':
                        file=options[i+1]
                                          
                    elif opt=='baud' or opt=='-baud' or opt=='b' or opt=='-b':
                        baud=options[i+1]
                        
                    elif opt=='port' or opt=='-port' or opt=='p' or opt=='-p':
                        port=options[i+1]
                        
                    elif opt=='rts' or opt=='-rts' or opt=='r' or opt=='-r':
                        rts=options[i+1]
                        
                    elif opt=='checkpic' or opt=='-checkpic' or opt=='c' or opt=='-c':
                        check=1
                        return file,port,baud,rts,check
        except:
            print ('check options')
            
        return file,port,baud,rts,check
    
    def tranfer_file(self,file,port,baud,rts):
        begin=time.strftime("%H:%M", time.localtime())
        
        c,message=detectpic.check_conection(port, baud)

        #If tinybld cant connect to selected port return error message
        if c==False:
            print (message),
            return
        else:
            print (message),
        
        #chunkhexfile.chunk_hexfile(file) 
        print ('\n Searching for PIC ...')
        
        for i in range(0,20):
            
            while gtk.events_pending():
                gtk.main_iteration()

            type,max_flash,family,message,bsize=detectpic.check_pic(port,baud,rts)

            if max_flash!=None:
                break

            print (' press RESET')

        if max_flash==None:
            print (' pic not found')
            return
        else:
            print (message)
            
         
        start = time.time()
        write_status=transferhex.transfer_hex(None,file,port,baud,type,max_flash,family,rts,bsize)
        end = time.time()
        
        
        if write_status=='OK':
            print ('Write OK at ' +str(begin)+' time: '+str(end-start)[0:5]+' sec')
        else:
            print ('\n Error writing')
            return
   
    def check_pic_terminal(self,port,baud,rts):
        
        print ('checking pic')
        c,message=detectpic.check_conection(port, baud)

        #If tinybld cant connect to selected port return error message
        if c==False:
            print (message),
            return

        else:
            print (message),
        
        #chunkhexfile.chunk_hexfile(file)
        
        print ('\n Searching for PIC ...')
        
        for i in range(0,20):
            
            while gtk.events_pending():
                gtk.main_iteration()

            type,max_flash,family,message,bsize=detectpic.check_pic(port,baud,rts)

            if max_flash!=None:
                break

            print (' press RESET')
   
        if max_flash==None:
            print (' pic not found')
            return
        else:
            print (message)
            
    def on_open_terminal_button_released(self, widget):
        port=self.port_entry.get_text()
        speed=int(self.speed_terminal_combo.get_active_text())
        self.close_terminal.set_sensitive(1)
        self.send_data.set_sensitive(1)
        self.terminal_window.set_sensitive(1)
        self.open_terminal.set_sensitive(0)
        
        t=terminal.Terminal()
        t.open(Tinybldlin,port, speed)
        
    def on_close_terminal_button_clicked(self, widget):
        
        t=terminal.Terminal()
        t.close(Tinybldlin)
        
        self.close_terminal.set_sensitive(0)
        self.send_data.set_sensitive(0)
        self.terminal_window.set_sensitive(0)
        self.open_terminal.set_sensitive(1)
        
    def on_clear_terminal_button_clicked(self, widget):
        buffer=self.terminal.get_buffer()
        buffer.set_text("")
        
    def on_tx_type_combo_changed(self, widget):
        print ('')
        
    def on_send_terminal_button_clicked(self, widget):
        tx_type=self.tx_type_combo.get_active_text()
        data=self.tx_data_combo.get_active_text()
        t=terminal.Terminal()
        if tx_type=='char':
            t.send_data(data)
            
        if tx_type=='char\\':
            t.send_data(data)
            t.send_data('\r')
        
    def on_one_button_clicked(self, widget):
        print ('on_one_button_clicked')
        
    def on_two_button_clicked(self, widget):
        print ('on_two_button_clicked')
     
    def on_three_button_clicked(self, widget):
        print ('on_three_button_clicked')   
        
    def on_rx_type_combo_changed(self, widget):
        try:
            
            buffer=self.terminal.get_buffer()
            start, end = buffer.get_bounds()
            t=terminal.Terminal()
            rx_type=self.rx_type_combo.get_active_text()
            text = buffer.get_text(start, end, include_hidden_chars=True)
            text_hex=''
            text_char=''
            
            if rx_type=='Hex':
                
                for i in range(0,len(text)):
                    hexa=str(hex(ord(text[i])))[2:4]
                    if len(hexa)<2:
                        hexa='0'+hexa
                    text_hex=text_hex+hexa+ ' '
                    
                buffer.set_text('')
                t.write_message(Tinybldlin,text_hex)
            
            if rx_type=='char':
                buffer_hex=text.split(' ')
                for i in range(0,len(buffer_hex)):
                    try:
                        c=chr(eval('0x'+buffer_hex[i]))
                    except:
                        c=' '
                    text_char=text_char+c
                buffer.set_text('')
                t.write_message(Tinybldlin,text_char)


            while gtk.events_pending():
                    gtk.main_iteration()
   
        except:
            return
        
    def on_b_button_clicked(self, widget):
        print ('on_b_button_clicked')  
        
    def on_h_button_clicked(self, widget):
        print ('on_h_button_clicked')  
        
    def on_r_button_clicked(self, widget):
        print ('on_r_button_clicked')  
        
    def on_terminal_key_press_event(self, widget, event):
        
        type=self.tx_type_combo.child.get_text()
        data=event.keyval
        if event.keyval==gtk.keysyms.Return:
            data=0x0D
        elif event.keyval==gtk.keysyms.BackSpace:
            data=0x7f     

        try:
            if type=='Type':
                t=terminal.Terminal()
                t.terminal_type(data)
                
            if type=='TypEcho':
                t=terminal.Terminal()
                t.write_message(Tinybldlin,chr(data))
                t.terminal_type(data)
                
        except ValueError:
            print (data)
                
    def on_terminal_data_entry(self,widget,event):
        data=self.terminal_data_entry.get_text()
        t=terminal.Terminal()
        t.send_data(data)   
        
    def on_window1_destroy(self, widget):
        self.close=0
        file_path = self.hexfile_combo
        baud_rate = self.speed_combo
        speed_terminal=self.speed_terminal_combo

        Width,Height= self.window1.get_size()
       
        try:
            loadsavesettings.save_settigs('FILES','HexFile',file_path.get_text())
            loadsavesettings.save_settigs('PIC','COMport',self.port_entry.get_text())
            loadsavesettings.save_settigs('PIC',"COMspeed",baud_rate.get_text())
            
            loadsavesettings.save_settigs('WINDOW',"Width",Width)
            loadsavesettings.save_settigs('WINDOW',"Height",Height)
            
            loadsavesettings.save_settigs('OPTIONS',"RTS",int(self.rts_checkbutton.get_active()))
            loadsavesettings.save_settigs('OPTIONS',"CHF",int(self.chunk_hexfile.get_active()))
           
            loadsavesettings.save_settigs('TERMINAL',"speed",int(speed_terminal.get_text()))


        except:
            print ('there was an error saving settings')
            gtk.main_quit()
        print ('good bye')
        gtk.main_quit()
            
if __name__ == "__main__":
    try:
        Tinybldlin = Tinybldlin()
        gtk.main()
    except KeyboardInterrupt:
        print ('\nkilled by user')
