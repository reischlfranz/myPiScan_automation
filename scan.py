#!/usr/bin/env python
import os
import sys

import os
import time
from datetime import datetime
from subprocess import call

def getfilename():
    # Initiating file and path parameters
    
    # filepath only for testing purposes. Should be configured later on in settings file. 
    str_filepath="/public/img/"
    
    # filename prefix
    str_prefix="scn_"
    
    # filetype
    str_filetype=".tiff"
    
    # done initiating file and path parameters
    
    
    num_iter=15         # int: Number of iterations to try
    str_date=""         # String: current date as string 
    str_time=""         # String: current time as string
    str_datetime_now="" # String: combined time and date to an unique string
    str_filename=""     # String: completed filename
    
    # get current date
    str_date=datetime.now().strftime("%Y-%m-%d")
    
    # get current time
    str_time=datetime.now().strftime("%H_%M_%S")
    # for testing purposes: strip the second of the filename and you have the chance to get a double filename
    #str_time=datetime.now().strftime("%H_%M")
    
    # DEBUG output: print date and time
    str_out="Heute ist: "+str_date+". Uhrzeit ist: "+str_time
    print(str_out)
    
    # contencate filename
    str_datetime_now=str_date+"_-_"+str_time
    str_filename=str_prefix+str_datetime_now+str_filetype
    
    # DEBUG output: print filename
    str_out="Filename: "+str_filename
    print(str_out)
    
    if not os.access(str_filepath+str_filename, os.F_OK):
        # DEBUG output: XXXXX
        str_out="Datei existiert noch nicht: "+str_filename
        print(str_out)
        
        # TESTING create an empty file there
        f_file=open(str_filepath+str_filename, mode='w')
        time.sleep(2)
        f_file.close()
        
    else:
        # DEBUG output: XXXXX
        str_out="Datei existiert bereits: "+str_filename
        print(str_out)
        i=0
        while i<=num_iter:
            str_filename=str_prefix+str_datetime_now+"_"+str(i)+str_filetype
            
            if not os.access(str_filepath+str_filename, os.F_OK):
                
                # DEBUG output: XXXXX
                str_out="Datei existiert noch nicht: "+str_filename
                print(str_out)
    
                print(str_filename)
                
                break;
            else:
                # DEBUG output: XXXXX
                str_out="Datei existiert noch nicht: "+str_filename
                print(str_out)
    
                i=i+1            
    
                continue
            #end if
            
        #end while
        
        if i==num_iter:
            # Too much iterations, giving up
            
            return -1
            
        #end if
           
    #end if
    
    
    return str_filepath+str_filename
#end function




print("program start")
print(sys.version)
print("------------")
print(sys.version_info)
print("------------")
print("------------")

while 1:
    e = ""
    print ('Push the button: [Enter] to scan / [Q] to quit');
    e = raw_input('now');
    if e=="":
        # No input, Scan
        # filename=execfile("filenaming.py")
        fn=getfilename()
        
        print("Dateiname:"+fn)
        
        os.system("scanimage --format=tiff --mode=Color --resolution=300 -p > "+fn)
     
    elif e.lower()=="q":
        # input q, quit
        break
    #end if
    
    

#end while

