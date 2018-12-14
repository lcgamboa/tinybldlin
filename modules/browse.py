import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk

def browse_hexfile(gui,filepath):
    
        file_open = gtk.FileChooserDialog(  title="Select HexFile",
                                            action=gtk.FileChooserAction.OPEN, 
                                            buttons=(   gtk.STOCK_CANCEL,
                                                        gtk.ResponseType.CANCEL,
                                                        gtk.STOCK_OPEN,
                                                        gtk.ResponseType.OK))
                                                        
        result = ""
        path=filepath.split('/')
        l=len(path)
        
        if l>=2:
            path_hex='/'
            for disp in range(1,l-1):
                path_hex=path_hex+path[disp]+'/'
                
        try:
            file_open.set_current_folder(path_hex)
            
        except:
            print ('choose a valid hex file')

        """Create and add the Images filter"""		
        filter = gtk.FileFilter()
        filter.set_name("Hex File")
        filter.add_pattern("*.HEX")
        filter.add_pattern("*.hex")
        file_open.add_filter(filter)
        
        """Create and add the 'all files' filter"""
        filter = gtk.FileFilter()
        filter.set_name("All files")
        filter.add_pattern("*")
        file_open.add_filter(filter)

        """Init the return value"""
        
        if file_open.run() == gtk.ResponseType.OK:
            result = file_open.get_filename()
            
        file_open.destroy()
        return result
