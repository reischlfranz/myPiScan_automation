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
            str_filename=str_prefix+str_datetime_now+"_"+str(i)+str_filetype
            
            if not os.access(str_filepath+str_filename, os.F_OK):
                
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
    
    
    return str_filepath+str_filename
#end function




print("Program start. System Info (Python version):")
print(sys.version)
print("------------")
print("Additional info:")
print(sys.version_info)
print("------------")
print(" ")  
print("Ready for new scan.")

GPIO.output(10, False) #Green LED on -> System ready.

while 1:


    if GPIO.input(8):
        # No input, Scan
        
        
        GPIO.output(12, False) # Yellow LED on -> working
        GPIO.output(10, True) # Green LED off -> scanning in progress
        
        # filename=execfile("filenaming.py")
        fn=getfilename()
        
        print("Filename:"+fn)
        
        os.system("scanimage --format=tiff --mode=Color --resolution=300 -p > "+fn)
 

        GPIO.output(10, False) # Green LED on -> scanning done

        print("\n")  
        print("Scan complete. Converting to jpg...")

        os.system("convert "+fn+" "+fn+".jpg")
        
        print("Conversion complete. Deleting TIFF...")
        
        # Comment out the next line if you want to keep the TIFF
        os.system("rm -f "+fn)

        # Setting ownership of file to samba user
        # This might be purly subjective...
#        os.system("chown nobody:nogroup "+fn)

        os.system("chmod 777 "+fn)

        print("Done.")
        
        # I could copy files to network drive now...
        GPIO.output(12, True) #Yellow LED off -> complete

        print(" ")  
        print("Ready for new scan.")


    #sleep(0.5)

#end while

