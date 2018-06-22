#!/usr/bin/python

from gpiozero import OutputDevice
from gpiozero import Button
from gpiozero import LED
from rewake import TempSensor
from time import *
import time


'''
AC Modes:

Off = 0, On = 1, Auto = 2
Timer On, Timer Off (how will this overlap on/off functionality?)
'''
globals()['modes'] = {
    0: "Off",
    1: "Auto",
    2: "Always On"
}


# Functions
def ac_on():
    print "Turning AC On"
    # led.on()
    ac.on()


def ac_off():
    print "Turning AC Off"
    # led.off()
    ac.off()


def ac_auto():
    print("AC Auto Mode")
    # led.blink()


# def button_handler():
    # if I press the button, it should blink a certain number of times to let me know what the current mode is
    # led.blink()


def button_hold_handler():
    set_mode()


def set_mode():

    # Off to Auto
    if globals()['mode'] == 0:
        ac_on()
        globals()['mode'] = 1

    # Auto to On
    elif globals()['mode'] == 1:
        ac_auto()
        globals()['mode'] = 2

    # On to Off
    elif globals()['mode'] == 2:
        ac_off()
        globals()['mode'] = 0

    print "AC Mode: " + globals()['modes'][globals()['mode']]


# Setup Devices
ac = OutputDevice(18)
#led = LED(35)

# Set global to match current AC state
globals()['mode'] = ac.value


# Set temp ranges
t_hi = 69
t_lo = 68

# Set operating times
operation_times = [
    [
        '9:00'
    ]
]

# Read temp
ts = TempSensor()

# Setup button
button = Button(16)

# Button event handlers
# button.when_activated = button_handler
button.when_held = button_hold_handler


# Start program loop
while True:

    # AC should be Off
    if globals()['mode'] == 0:
        if ac.value:
            ac_off()
        continue

    # AC should be On
    elif globals()['mode'] == 1:
        if not ac.value:
            ac_on()

    # AC should be Auto, which reads current temp and adjusts accordingly
    elif globals()['mode'] == 2:
        temp = ts.fahrenheit()
        print strftime('%x %X') + " Temp: " + str(temp)
        time.sleep(10)

        # See if temp is BELOW desired LOW temp
        if temp < t_lo:
            if ac.value is True:
                ac_off()

        # See if temp is ABOVE desired HIGH temp
        if temp > t_hi:
            if ac.value is False:
                ac_on()
