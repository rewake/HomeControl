import time
import datetime
from dynamodb.iot import Schedules

globals()['mode'] = 0
globals()['temp'] = 72

globals()['modes'] = {
    0: "Off",
    1: "Auto",
    2: "Always On"
}

globals()['schedule'] = Schedules().get('ac')

dbg = True;

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

# TODO : initial AC state

    if globals()['mode'] != mode:
        print "Setting mode to: " + str(mode)
        set_mode(mode)

    if globals()['temp'] != temp:
        print "Setting mode to: " + str(temp)
        set_temp(temp)

    # set_mode()
    time.sleep(20)
