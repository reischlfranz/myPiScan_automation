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

import ConfigParser

SETTINGS1_color="Gray"
SETTINGS1_resolution="150"
SETTINGS1_width="215.9mm"
SETTINGS1_height="297.18mm"

SETTINGS2_color="Color"
SETTINGS2_resolution="300"
SETTINGS2_width="215.9mm"
SETTINGS2_height="297.18mm"


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

# path to settings file
str_settingspath=os.getcwd()+"/"

# make settings file writeable
# should be disabled in production!
os.system("chmod 777 "+str_settingspath+"/settings.ini")

# filename prefix
str_prefix="_pic"

# filetype
str_filetype=".tiff"

def read_settings():
    print "Re-Reading settings file"
    Config = ConfigParser.ConfigParser()
    Config
    Config.read(str_settingspath+"/settings.ini")
    
    global SETTINGS1_color
    global SETTINGS1_resolution
    global SETTINGS1_width
    global SETTINGS1_height
    
    global SETTINGS2_color
    global SETTINGS2_resolution
    global SETTINGS2_width
    global SETTINGS2_height
    
    SETTINGS1_color=Config.get("Scan1", "color")
    SETTINGS1_resolution=Config.get("Scan1", "resolution")
    SETTINGS1_width=Config.get("Scan1", "width")
    SETTINGS1_height=Config.get("Scan1", "height")
    
    SETTINGS2_color=Config.get("Scan2", "color")
    SETTINGS2_resolution=Config.get("Scan2", "resolution")
    SETTINGS2_width=Config.get("Scan2", "width")
    SETTINGS2_height=Config.get("Scan2", "height")

    #DEBUG: Print all those on screen
    print "Finished reading settings file:"
    print "SETTINGS1_color:"+SETTINGS1_color
    print "SETTINGS1_resolution:"+SETTINGS1_resolution
    print "SETTINGS1_width:"+SETTINGS1_width
    print "SETTINGS1_height:"+SETTINGS1_height
    print " "
    print "SETTINGS2_color:"+SETTINGS2_color
    print "SETTINGS2_resolution:"+SETTINGS2_resolution
    print "SETTINGS2_width:"+SETTINGS2_width
    print "SETTINGS2_height:"+SETTINGS2_height
    

#end def

def getfilename():
	
	num_iter=15         # int: Number of iterations to try
	str_date=""         # String: current date as string 
	str_filename=""     # String: completed filename
	
	#Read the last filename from tempfile - files have format of '2015-07-15_pic05'
	lastfile=open('lastscan','r')
	lastfilename=lastfile.read()
	lastfile.close()
	
	# DEBUG output: print lastfilename
	str_out="lastfilename: "+lastfilename
	print(str_out)
	
	#filenumber defaults to 1, except if there are already files from the same date
	filenumber=1
	
	#Getting the date portion of lastfilename
	lastfiledate=lastfilename[:6]
	
	# get current date
	str_date=datetime.now().strftime("%Y-%m-%d")
	
	#If last file was today, increase number for next file. Otherwise, leave 1
	if lastfiledate==str_date:
		filenumber=lastfilename[14:2]+1
		
		# DEBUG output: print lastfilename[14:2]
		str_out="lastfilename[14:2]: "+lastfilename[14:2]
		print(str_out)
	#end if
	
	#Contecating filename
	str_filename=str_date+str_prefix+format(filenumber,'02d')
	
	# DEBUG output: print filename
	str_out="Filename: "+str_filename
	print(str_out)
	
	if not os.access(str_filepath+str_filename, os.F_OK):
		# DEBUG output: XXXXX
		str_out="File does not exist: "+str_filename
		print(str_out)
		
	else:
		# DEBUG output: XXXXX
		str_out="File does already exist: "+str_filename
		print(str_out)
		i=0
		while i<=num_iter:
			filenumber=filenumber+1
			str_filename=str_date+str_prefix+format(filenumber,'02d')
			
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
	
	# Write new filename into tempfile
	lastfile=open('lastscan','w')
	lastfilename=lastfile.write(str_filename)
	lastfile.close()
	
	return str_filename
#end function


def do_scan(quality=0):

    global SETTINGS1_color
    global SETTINGS1_resolution
    global SETTINGS1_width
    global SETTINGS1_height
    
    global SETTINGS2_color
    global SETTINGS2_resolution
    global SETTINGS2_width
    global SETTINGS2_height

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

    sys_call=""
    
    print "TEST: SETTINGS1_height:"+SETTINGS1_height
    
    if(quality==0):
        # Do a scan with settings 1 (Standard is a full size A4 150 DPI Black&White scan) 
        sys_call=("scanimage " 
        "--format=tiff " 
        "--mode="+SETTINGS1_color +" "
        "--resolution "+SETTINGS1_resolution+" "
        "-l 0mm " # starting position top left, X coordinate
        "-t 0mm " # starting position top left, Y coordinate
        "-x "+ SETTINGS1_width  + " " # Width
        "-y "+ SETTINGS1_height + " " # Height
        "-p -v "
        "> "+fn+str_filetype)    
        
    elif(quality==1):
        # Do a scan with settings 2 (Standard is a full size A4 300 DPI Color scan)
        sys_call=("scanimage " 
        "--format=tiff " 
        "--mode="+SETTINGS2_color +" "
        "--resolution "+SETTINGS2_resolution+" "
        "-l 0mm " # starting position top left, X coordinate
        "-t 0mm " # starting position top left, Y coordinate
        "-x "+ SETTINGS2_width  + " " # Width
        "-y "+ SETTINGS2_height + " " # Height
        "-p -v "
        "> "+fn+str_filetype)
    else:
        return -1

    #end if
    print "++"
    print "++ will now use the following command: ++"
    print "++ " + sys_call + " ++"
    print "++"
    out=os.system(sys_call)
	
	
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
    tiff_file.close()
    
    if tiff_broken==0:
        print("TIFF is OK, continue")
    else:
        print("TIFF is broken")
    # ---
    # TIFF Broken Check done

    print("\n")  
    print("Scan complete. Converting to jpg...")
    f_file.write("Scan complete. Converting to jpg... "+datetime.now().strftime("%H:%M:%S")+"\n")

    out=os.system("convert "+fn+str_filetype+" "+fn+".jpg")

    # Allow deletion of JPG Image for everyone
    # By default, all files created by this script will be owned by root!
    # Note: If you want to restrict access to certain users, be sure to use the right chown
    os.system("chmod 777 "+fn+".jpg")
    
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
    
    defects_in_a_row=0
    
    for i in range(size-2):
        ch=f.read(1)
        if ch=="":
            print("EOF found, should not have come to this. I'm confused...")
            return 0
        if ch==chr(0xff):
            #print("FF gefunden:Position "+str(i)+"_Gelesen:"+hex(ord(ch))+"_Position_"+str(f.tell()))
            defects_in_a_row+=1
            
            if(defects_in_a_row>=64):
                # 8 defect bytes in a row detected, assuming TIFF is broken
                print("8 defect bytes in a row detected, assuming TIFF is broken, quitting...")
                return 1
        
            continue
        #end if
        
        defects_in_a_row=0
        # print("Position "+str(i)+"_Gelesen:"+hex(ord(ch))+"_Position_"+str(f.tell())) # DEBUG Info
        #f.seek(1,os.SEEK_CUR)
    
    return 0




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

#first time reading settings file
read_settings()


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
        read_settings()
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
        
#        #re-read settings when "deleteme" file is gone 
#        if not os.path.exists(str_settingspath+"/deleteme"):
#            read_settings()
#            delfile=open(str_settingspath+"/deleteme",mode='w')
#            delfile.close()
#            os.system("chmod 777 "+str_settingspath+"/deleteme")
#        #end if
        
        sleep(0.7)

#end while

