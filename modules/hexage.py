import time
import stat
import os
import datetime


def gethexage(filename):
    
    file_stats = os.stat(filename)
    
    hex_date = time.strftime("%Y-%m-%d",time.localtime(file_stats[stat.ST_MTIME]))
    hex_time = time.strftime("%H:%M:%S",time.localtime(file_stats[stat.ST_MTIME]))
    
    ymd_hex=hex_date.split('-')
    time_hex=hex_time.split(':')
    
    fecha_hex = datetime.datetime(int(ymd_hex[0]), int(ymd_hex[1]),int(ymd_hex[2]), int(time_hex[0]), int(time_hex[1]),int(time_hex[2]))
  
    datetime.timedelta
    old=str(datetime.datetime.today() - fecha_hex)
    
    newold=old.split(',')
       
    if len(newold)==1:
        hm=newold[0].split(':')
        if hm[0]!='0':
            age=hm[0]+' hrs'
            return age
        if hm[1]!='00':
            age=hm[1]
            return age+ ' min'
        
        else:
            age='0 min'
            return age
  
    if len(newold)==2:
        age=str(newold[0])
        return age
 
    