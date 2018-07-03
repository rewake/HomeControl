from time import *
import time
from datetime import datetime
from devices import TempSensor
from devices import AirConditioner
from dynamodb.iot import Schedules
import logging
import sys

# Configure logging
logging.basicConfig(stream=sys.stderr, level=logging.INFO)

# Setup devices
ac = AirConditioner(14)
ts = TempSensor()

# Default settings
default_mode = ac.OFF
default_temp = 72

# Polling interval in seconds
poll_interval = 10


'''
NOTES / TODOs

also, the schedule table here is generic, however, the collection docs refer specifically to AC schedule, 
so I'll prob have to re-think this in time

need to think about invalidating loaded schedule 
'''


def determine_desired_settings():

    # Get today's schedule from DB
    schedule = Schedules().today('ac')

    # Set new values to default values, to be overwritten by schedule
    new_mode = default_mode
    new_temp = default_temp

    # Loop scheduled events
    for event in schedule:

        # Convert schedule time string to datetime
        schedule_time = datetime.strptime(event['time'], "%H:%M").time()
        d = datetime.combine(datetime.today(), schedule_time)

        '''
        If event datetime is in the past, we'll consider the current event as active, and it will be selected for use.
        
        NOTE: this logic is dependant on the chronological order of events set in the schedule
        '''
        if d <= datetime.now():

            # Log info
            logging.debug("The following schedule was selected: ")
            logging.debug(event)

            # See if mode should be updated based on schedule
            if 'mode' in event and event['mode'] != ac.mode:

                # Set mode to event mode
                new_mode = event['mode']

            # See if temperature should be updated based on schedule
            if 'temp' in event and event['temp'] != new_temp:

                # Set temp to event temp
                new_temp = event['temp']

            # Break loop - no need to check other events in the schedule
            break

    # Return desired mode and temperature
    return new_mode, new_temp


# Run program
while True:

    # Get desired settings
    desired_mode, desired_temp = determine_desired_settings()

    logging.info(str(desired_mode) + ' / ' + str(desired_temp))

    # Set AC mode to desired mode
    if ac.mode != desired_mode:
        print "Setting mode to: " + str(desired_mode)
        ac.set_mode(desired_mode)

    # If AC mode is AUTO, we need to monitor the temperature and adjust the AC mode automatically
    if ac.mode == ac.AUTO:

        # Get current temp
        current_temp = ts.fahrenheit()
        print strftime('%x %X') + " Temp: " + str(current_temp)

        # See if temp is BELOW desired LOW temp
        if current_temp < desired_temp:

            # Check current AC mode
            if ac.mode is not ac.OFF:

                # Turn AC off
                ac.off()

        # See if temp is ABOVE desired HIGH temp
        if current_temp > desired_temp:

            # Check current AC mode
            if ac.mode is not ac.ON:

                # Turn AC on
                ac.on()

    # Wait before polling devices
    time.sleep(poll_interval)
