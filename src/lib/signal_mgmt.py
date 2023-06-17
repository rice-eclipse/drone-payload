import RPi.GPIO as GPIO
import dronekit
import config_vars


def init_vehicle() -> dronekit.Vehicle:
    '''
    Connects to the vehicle and returns the vehicle object
    Initializes Raspberry Pi pins that connect to the Pixhawk
    '''
    # sets up the pins connected to the switches
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(config_vars.INPUT_PIN1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(config_vars.INPUT_PIN2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # connects to the vehicle
    return dronekit.connect(config_vars.ADDRESS, wait_ready=True, baud=57600)


def switch_override(vehicle: dronekit.Vehicle) -> bool:
    '''
    Detects the input GPIO limit switch states, overrides ArduPigeon
    channels to begin drone flight if both switches are off (arms open)
    '''
    # sends the 1200Hz signal to channel 7 if either of the switches are on
    if (GPIO.input(config_vars.INPUT_PIN1) or GPIO.input(config_vars.INPUT_PIN2)):
        vehicle.channels.overrides = {'7': config_vars.SIGNAL_ON}
        print(f"Signal high (sending signal {config_vars.SIGNAL_ON} Hz)")
        return False  # Drone not unfolded

    # sends the 1700Hz signal to channel switches if both switches are off
    vehicle.channels.overrides = {'7': config_vars.SIGNAL_OFF}
    print(f"Signal low (sending signal {config_vars.SIGNAL_OFF} Hz)")
    return True  # Drone Unfolded
