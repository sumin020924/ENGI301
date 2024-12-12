# Eggcellent Timer

## Setting up the hardware
Wire all the hardware components before running the software.
Refer to the hackster.io link:
https://www.hackster.io/sumin020924/edes-301-eggcellent-timer-74d33b

## Setting up the software
Before running the timer, make sure that the device is connected to the Internet.
sudo dhclient usb1 --> enter password: temppwd --> ping google.com

Install all softwares on PocketBeagle before running drivers.

### System tools
sudo apt-get update --> 
sudo apt-get install build-essential python-dev python-setuptools python-smbus -y --> 
sudo apt-get install python-pip python3-pip -y --> 
sudo apt-get install zip -y 

### Adafruit libraries
sudo pip3 install --upgrade setuptools --> 
sudo pip3 install --upgrade Adafruit_BBIO --> 
sudo pip3 install adafruit-blinka

### Temperature sensor
Download the DTS file for the DS18B20 temperature sensor.
Run the code below to set up for the temperature sensor:
debian@beaglebone:/boot$ cat uEnv.txt --> debian@beaglebone:/var/lib/cloud9$ cd /sys/bus 
--> debian@beaglebone:/sys/bus$ ls --> debian@beaglebone:/sys/bus$ cd w1 --> debian@beaglebone:/sys/bus/w1$ ls --> debian@beaglebone:/sys/bus/w1$ cd devices -->
debian@beaglebone:/sys/bus/w1/devices$ ls --> debian@beaglebone:/sys/bus/w1/devices$ cd 28-20a9d4469694 --> debian@beaglebone:/sys/bus/w1/devices/28-20a9d4469694 ls -->
debian@beaglebone:/sys/bus/w1/devices/28-20a9d4469694$ ls --> debian@beaglebone:/sys/bus/w1/devices/28-20a9d4469694$ cat w1_slave

### Configure pins
Note that all pins for buttons, buzzer, SPI screen, and temperature sensor should be configured before running. Run 'configure_pins.sh' in the terminal. 
