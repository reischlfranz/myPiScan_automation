myPiScan_automation
Ing. Franz Reischl, 2013


Purpose of this project was to scan documents to the Raspberry Pi via the press of a physical button.
For this, a supported USB Scanner has to be connected and running using SANE.

Make sure you have the necessary packages installed:
* Python 2.7
* Sane
* imagemagick (for jpg conversion)
* Output folder /public/img (You can change this in the code)
* Button connected to Pin 8 of the Raspberry pi (see further down)
* LEDs connected to Pin 10 and 12 of the Raspberry pi (Optional, see further down)
* Internet connection 
	(Optional, but recommended for the Pi to set itself to the correct time, 
	since this script creates filenames based on the time and date.) 


Installation:
Copy this script to your Raspberry Pi and start with root privileges (necessary for GPIO handling):
	python ./scan.py
Optional: For this script to start automatically on Pi boot, add a line to your /etc/rc.local file:
	python /path/to/scan.py
 
Once started, when pressing the button, the script will create a filename based on current date and time 
and check if a file of this name already exists. (Since it takes more than a second for a scan to complete,
this should not really be an issue.) The script will scan a single page - 300 dpi, color - to a tiff file
with the created naming. After that, it converts the tiff to a jpg for size reasons and deletes/archives the 
tiff. Finally, a chmod 777 is applied to the file, to allow a user to delete it once he did what he scanned 
it for. This is necessary, because any file created by a script running as root will belong to the root user.   




GPIO-Ports used:
 8: Input, Tactile switch. Hooked to GND via a 10k resistor, pull up to 3.3V 
10: Output, Green LED
12: Output, Yellow LED (Did not have a red one)
LEDs are switched to GND, which means switching the port off turns the LED on.