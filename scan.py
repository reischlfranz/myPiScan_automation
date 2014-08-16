#!/usr/bin/env python
import os
import sys

import os
import time
from datetime import datetime
from subprocess import call
from time import sleep

#import Raspberry Pi GPIO module
import RPi.GPIO as GPIO

# Set the mode of numbering the pins. 
GPIO.setmode(GPIO.BOARD)

# Disable Already In Use warnings
GPIO.setwarnings(False)

# GPIO pin 8 as input. 
GPIO.setup(8, GPIO.IN) 

# GPIO pin 10, 12 as output
GPIO.setup(10, GPIO.OUT) # Green
GPIO.setup(12, GPIO.OUT) # Yellow

# Set 10 to True (LED off)
GPIO.output(10,True)
GPIO.output(12,True)

# ######################
# ### Initialization ###
# ######################

# Initiating file and path parameters

# filepath only for testing purposes. Should be configured later on in settings file. 
str_filepath="/public/img/"

# filename prefix
str_prefix="scn_"

# filetype
str_filetype=".tiff"




def getfilename():
    
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
    # str_time=datetime.now().strftime("%H_%M")
    
    # DEBUG output: print date and time
    str_out="Todays date:: "+str_date+". Current time: "+str_time
    print(str_out)
    
    # contencate filename
    str_datetime_now=str_date+"_-_"+str_time
    str_filename=str_prefix+str_datetime_now+str_filetype
    
    # DEBUG output: print filename
    str_out="Filename: "+str_filename
    print(str_out)
    
    if not os.access(str_filepath+str_filename, os.F_OK):
        # DEBUG output: XXXXX
        str_out="File does not exist: "+str_filename
        print(str_out)
        
        # TESTING create an empty file there
        f_file=open(str_filepath+str_filename, mode='w')
        time.sleep(2)
        f_file.close()
        
    else:
        # DEBUG output: XXXXX
        str_out="File does already exist: "+str_filename
        print(str_out)
        i=0
        while i<=num_iter:
            str_filename=str_prefix+str_datetime_now+"_"+str(i)
            
            if not os.access(str_filename, os.F_OK):
                
                # DEBUG output: XXXXX
                str_out="File does not exist: "+str_filename
                print(str_out)
    
                print(str_filename)
                
                break;
            else:
                # DEBUG output: XXXXX
                str_out="File does already exist: "+str_filename
                print(str_out)
    
                i=i+1            
    
                continue
            #end if
            
        #end while
        
        if i>=num_iter:
            # Too much iterations, giving up
            print("Too many iterations, giving up")
            return -1
            
        #end if
           
    #end if
    
    
    return str_filename
#end function


def do_scan(quality=0):

    # Open Logfile, Write timestamp
    f_file=open("./img_log.txt", mode='a')
    f_file.write("Scan gestartet:"+datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"\n")
    
    # Setting LEDs
    GPIO.output(12, False) # Yellow LED on -> working
    GPIO.output(10, True) # Green LED off -> scanning in progress
    
    # Generate Filename
    fn=getfilename()
    
    print("Filename:"+fn)
    f_file.write("generated Filename:"+fn+"\n")

    if(quality==1):
        
        # Do a 300 DPI Color scan
        out=os.system("scanimage --format=tiff --mode=Color --resolution=300 -p -v > "+fn+str_filetype)
        
    elif(quality==0):
        
        # Do a 150 DPI Black&White scan 
        out=os.system("scanimage --format=tiff --mode=Gray --resolution=150 -p -v > "+fn+str_filetype)
    #end if

    # Allow deletion of TIFF Image for everyone
    # By default, all files created by this script will be owned by root!
    # Note: If you want to restrict access to certain users, be sure to use the right chown
    os.system("chmod 777 "+fn+str_filetype)

    out_str=str(out)
    print("\n\nScan: "+out_str)
    f_file.write("Return value scanimage: "+out_str+"\n")

    # Setting LEDs
    GPIO.output(10, False) # Green LED on -> scanning done

    # Insert TIFF Broken Check here!
    # ---
    tiff_file=open(fn+str_filetype,mode='rb')
    tiff_broken=tiffcheck(tiff_file, 1024)
    
    if tiff_broken==0:
        print("TIFF is OK, continue")
    else:
        print("TIFF is broken")
    # ---
    # TIFF Broken Check done

    print("\n")  
    print("Scan complete. Converting to jpg...")
    f_file.write("Scan complete. Converting to jpg... "+datetime.now().strftime("%H:%M:%S")+"\n")

    out=os.system("convert "+fn+str_filetype+" "+fn+"_"+out_str+".jpg")

    # Allow deletion of JPG Image for everyone
    # By default, all files created by this script will be owned by root!
    # Note: If you want to restrict access to certain users, be sure to use the right chown
    os.system("chmod 777 "+fn+"_"+out_str+".jpg")
    
    out_str=str(out)
    print("\nConv: "+out_str)
    
    print("Conversion complete. Deleting TIFF...")
    f_file.write("Conversion complete. Deleting/Archiving TIFF... "+datetime.now().strftime("%H:%M:%S")+"\n")
    
    # Comment out the next line if you want to keep the TIFF
    # os.system("rm -f "+fn+str_filetype)
    
    #DEBUG: Keep TIFF in archive
    if not os.access("./archive", os.F_OK):
        os.system("mkdir ./archive")
    os.system("mv "+fn+str_filetype+" ./archive")

    print("Done.")
    
    # I could copy files to network drive now...
    GPIO.output(12, True) #Yellow LED off -> complete

    print(" ")  
    print("Ready for new scan.")
#end function


def tiffcheck(f,size=1024):
    pos=f.seek(-size,os.SEEK_END)
    
    for i in range(size-2):
        ch=f.read(1)
        if ch=="":
            print("EOF found prior")
            return 1
        if not ch==chr(0xff):
            print("Abbruch, anderen char gefunden:Position "+str(i)+"_Gelesen:"+hex(ord(ch))+"_Position_"+str(f.tell()))
            return 0
        print("Position "+str(i)+"_Gelesen:"+hex(ord(ch))+"_Position_"+str(f.tell())) # DEBUG Info
        #f.seek(1,os.SEEK_CUR)
    
    return 1




print("Program start. System Info (Python version):")
print(sys.version)
print("------------")
print("Additional info:")
print(sys.version_info)
print("------------")
print(" ")  
print("Ready for new scan.")

os.chdir(str_filepath)

GPIO.output(10, False) #Green LED on -> System ready.

do_other_thing=0;
        
while 1:


    if GPIO.input(8):
        
        # If button is pressed longer than 2 seconds (20x 0.1 sec), do other thing
        for i in range(1, 20):

            sleep(0.1)
                        
            if not GPIO.input(8):
                do_other_thing=1;
                break;
            #end if
                        
        #end for
        
        if do_other_thing==1:
            
            print("Button pressed less than 2 seconds")
            
            # Quality = 0
            do_scan(0) 
            
        else:
            
            print("Button pressed 2 sec or longer")
            
            # Quality = 1
            do_scan(1)
            
        #end if
        do_other_thing=0;
        
        sleep(0.7)

#end while

