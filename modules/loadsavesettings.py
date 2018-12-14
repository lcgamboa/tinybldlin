from six.moves import configparser as ConfigParser
import os

def save_settigs(SECTION,NAME,VALUE):
    
    cfg = ConfigParser.ConfigParser()  
    configfile = os.path.join(os.environ.get("HOME", "."), ".tinybldlin")
    sections=["FILES","PIC","WINDOW","OPTIONS","TERMINAL"]

    if not cfg.read(configfile):
        print ("No existe el archivo intentando crear uno nuevo")
        for disp in sections:
            try:
                cfg.add_section(disp) 
                f = open(configfile, "w")  
                cfg.write(f)
                f.close()

            except:
                pass

    try:
        cfg.set(SECTION, NAME, VALUE)
        f = open(configfile, "w")
        cfg.write(f)
        f.close()
    except:
        cfg.add_section(SECTION)
        cfg.set(SECTION, NAME, VALUE)
        f = open(configfile, "w")
        cfg.write(f)
        f.close()
    return

def get_restore_settings(SECTION,NAME):
    cfg = ConfigParser.ConfigParser()  
    configfile = os.path.join(os.environ.get("HOME", "."), ".tinybldlin")
    cfg.read(configfile)  
    VALUE= cfg.get(SECTION, NAME)  
    return VALUE

#def OnInit(gui):
#
#    cfg = ConfigParser.ConfigParser()
#    configfile = os.path.join(os.environ.get("HOME", "."), ".tinybldlin")
#
#    if not cfg.read(configfile):
#        print "No config file"
#        return
#
#    #Getting Saved and restoring Values
#    if cfg.has_option("WINDOW", "top") and cfg.has_option("WINDOW", "left"):
#        Top=int(get_restore_settings('WINDOW','top'))
#        Left=int(get_restore_settings('WINDOW','left'))
#        WxTbl.SetPosition((Top,Left))
#
#    if cfg.has_option("WINDOW", "height") and cfg.has_option("WINDOW", "width"):
#        Height=int(get_restore_settings('WINDOW','height'))
#        Width=int(get_restore_settings('WINDOW','width'))
#        WxTbl.SetSize((Width,Height))
#
#    if cfg.has_option("FILES", "hexfile"):
#        HexFile=get_restore_settings('FILES','hexfile')
#        WxTbl.combo_box_hex.SetValue(HexFile)
#
#    if cfg.has_option("PIC", "comspeed"):
#        COMspeed=get_restore_settings('PIC','comspeed')
#        WxTbl.combo_box_speed.SetValue(COMspeed)
#
#    if cfg.has_option("TERMINAL", "termspeed"):
#        TERMspeed=get_restore_settings('TERMINAL','termspeed')
#        WxTbl.combo_box_speed_terminal.SetValue(TERMspeed)
#
#    if cfg.has_option("PIC", "comport"):
#        COMport=get_restore_settings('PIC','comport')
#        WxTbl.port.SetValue(COMport)

   

#def OnClose(WxTbl):
#
#
#    #seving Settings
#    try:
#        save_settigs('FILES','HexFile',WxTbl.combo_box_hex.GetValue())
#        save_settigs('PIC','COMport',WxTbl.port.GetValue())
#        save_settigs('PIC',"COMspeed",WxTbl.combo_box_speed.GetValue())
#        save_settigs('TERMINAL',"TERMspeed",WxTbl.combo_box_speed_terminal.GetValue())
#        Width,Height=WxTbl.GetSize()
#        save_settigs('WINDOW',"Width",Width)
#        save_settigs('WINDOW',"Height",Height)
#        Top,Left=WxTbl.GetPosition()
#        save_settigs('WINDOW',"Top",Top)
#        save_settigs('WINDOW',"Left",Left)
#
#    except:
#        print 'there was an error savig settings'
#    WxTbl.Destroy()
