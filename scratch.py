from time import *
import time
import datetime
from gpiozero import OutputDevice
from devices import TempSensor
from dynamodb.iot import Schedules
from pprint import pprint
import logging
import sys

# Configure logging
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

# Setup Devices
ac = OutputDevice(14)
ts = TempSensor()

# Initial configuration values
globals()['mode'] = int(ac.value)
globals()['temp'] = 72

globals()['modes'] = {
    0: "Off",
    1: "Auto",
    2: "Always On"
}

globals()['schedule'] = Schedules().get_by_attribute('group', 'ac')


'''
NOTES / TODOs

so, aside from being able to control the modes via schedule, we should also
be able to set the temp using the schedule as well.  

also, the schedule table here is generic, however, the collection docs refer specifically to AC schedule, 
so I'll prob have to re-think this in time

need to think about invalidating loaded schedule 
'''


def set_mode(mode):
    globals()['mode'] = mode


def set_temp(temp):
    print "Setting temp to: " + str(temp)
    globals()['temp'] = temp


def cycle_mode():

    # Off to Auto
    if globals()['mode'] == 0:
        set_mode(1)

    # Auto to On
    elif globals()['mode'] == 1:
        set_mode(2)

    # On to Off
    elif globals()['mode'] == 2:
        set_mode(0)

    print "AC Mode: " + globals()['modes'][globals()['mode']]


# TODO: these probably belong in AC class, after all
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


def determine_desired_settings():

    for event in globals()['schedule']:

        schedule_time = datetime.datetime.strptime(event['time'], "%H:%M").time()
        d = datetime.datetime.combine(datetime.datetime.today(), schedule_time)

        # print d.strftime('%m/%d/%Y %H:%M') + ' / ' + datetime.datetime.now().strftime('%m/%d/%Y %H:%M') + ' / ' + str(d > datetime.datetime.now())

        # Set new values to current values, to be overwritten if necessary
        new_mode = globals()['mode']
        new_temp = globals()['temp']

        # Determine desired mode
        if d <= datetime.datetime.now():

            # print "The following schedule was selected: "
            # pprint(event)

            # Use settings from schedule
            new_mode = event['mode']

            if 'temp' in event and event['temp'] != new_temp:
                new_temp = event['temp']

            break

    return new_mode, new_temp


# Run program
while True:

    mode, temp = determine_desired_settings()

    print str(mode) + ' / ' + str(temp)

    if globals()['mode'] != mode:
        print "Setting mode to: " + str(mode)
        set_mode(mode)

    if globals()['temp'] != temp:
        print "Setting mode to: " + str(temp)
        set_temp(temp)

    #
    # AC should be Off
    #
    if globals()['mode'] == 0:
        if ac.value:
            ac_off()

    # AC should be Auto, which reads current temp and adjusts accordingly
    elif globals()['mode'] == 1:
        current_temp = ts.fahrenheit()
        print strftime('%x %X') + " Temp: " + str(current_temp)

        # See if temp is BELOW desired LOW temp
        if current_temp < globals()['temp']:
            if ac.value is True:
                ac_off()

        # See if temp is ABOVE desired HIGH temp
        if current_temp > globals()['temp']:
            if ac.value is False:
                ac_on()

    # AC should be On
    elif globals()['mode'] == 2:
        if not ac.value:
            ac_on()

    time.sleep(10)
