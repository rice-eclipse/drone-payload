import RPi.GPIO as GPIO
from dronekit import connect

#Vehicle's address
ADDRESS = '/dev/ttyS0'

#On and off signal frequencies
SIGNAL_ON = 1200
SIGNAL_OFF = 1700

#Pins connected to switches
#TODO
INPUT_PIN1 = 26
INPUT_PIN2 = 16

#sets up the pins connected to the switches
GPIO.setmode(GPIO.BCM)
GPIO.setup(INPUT_PIN1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(INPUT_PIN2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#connects to the vehicle
vehicle = connect(ADDRESS, wait_ready=True, baud=57600)
def signal_detection():
    
    # loops continuously
    while(True):

        #sends the 1200Hz signal to channel 7 if either of the switches are on
        if (GPIO.input(INPUT_PIN1) or GPIO.input(INPUT_PIN2)):
            vehicle.channels.overrides = {'7', SIGNAL_ON}
            print("Signal high")

        # sends the 1700Hz signal to channel switches if both switches are off
        else:
            vehicle.channels.overrides = {'7', SIGNAL_OFF}
            print("Signal low")
    
    return

if __name__ == "main":
    signal_detection()
    