from time import *
import time
import datetime
from devices import TempSensor
from devices import AirConditioner
from dynamodb.iot import Schedules
from gpiozero import BadPinFactory
from pprint import pprint
import logging
import sys

# Configure logging
logging.basicConfig(stream=sys.stderr, level=logging.INFO)

# Setup Devices
ac = AirConditioner(14)
ts = TempSensor()

# Initial configuration values
ac.mode = int(ac.value)
globals()['temp'] = 72


# TODO: pull schedule just for today
globals()['schedule'] = sorted(Schedules().get_by_attribute('group', 'ac'), key=lambda k: ['time'])


'''
NOTES / TODOs

so, aside from being able to control the modes via schedule, we should also
be able to set the temp using the schedule as well.  

also, the schedule table here is generic, however, the collection docs refer specifically to AC schedule, 
so I'll prob have to re-think this in time

need to think about invalidating loaded schedule 
'''


def set_temp(temp):
    print "Setting temp to: " + str(temp)
    globals()['temp'] = temp


def cycle_mode():

    # Off to Auto
    if ac.mode == 0:
        ac.set_mode(ac.AUTO)

    # Auto to On
    elif ac.mode == 1:
        ac.set_mode(ac.ON)

    # On to Off
    elif ac.mode == 2:
        ac.set_mode(ac.OFF)

    print "AC Mode: " + ac.mode


def determine_desired_settings():

    for event in globals()['schedule']:

        # Convert schedule time string to datetime
        schedule_time = datetime.datetime.strptime(event['time'], "%H:%M").time()
        d = datetime.datetime.combine(datetime.datetime.today(), schedule_time)

        # Set new values to current values, to be overwritten if necessary
        new_mode = ac.mode
        new_temp = globals()['temp']

        # Determine desired mode
        if d <= datetime.datetime.now():

            # Log info
            logging.debug("The following schedule was selected: ")
            logging.debug(event)

            # Use settings from schedule
            new_mode = event['mode']

            # See if temperature should be updated based on schedule
            if 'temp' in event and event['temp'] != new_temp:

                new_temp = event['temp']

            break

    return new_mode, new_temp


# Run program
while True:

    mode, temp = determine_desired_settings()

    print str(mode) + ' / ' + str(temp)

    if ac.mode != mode:
        print "Setting mode to: " + str(mode)
        ac.set_mode(mode)

    if globals()['temp'] != temp:
        print "Setting mode to: " + str(temp)
        set_temp(temp)

    #
    # AC should be Off
    #
    if ac.mode == 0:
        if ac.value:
            ac.on()

    # AC should be Auto, which reads current temp and adjusts accordingly
    elif ac.mode == 1:
        current_temp = ts.fahrenheit()
        print strftime('%x %X') + " Temp: " + str(current_temp)

        # See if temp is BELOW desired LOW temp
        if current_temp < globals()['temp']:
            if ac.value is True:
                ac.off()

        # See if temp is ABOVE desired HIGH temp
        if current_temp > globals()['temp']:
            if ac.value is False:
                ac.on()

    # AC should be On
    elif ac.mode == 2:
        if not ac.value:
            ac.on()

    time.sleep(10)
