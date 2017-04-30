#--------------------------single_relay.py------------------------------
#
# Use:
#    from single_relay.py import relay
#    device = relay(5)....
#    device.on()            -->  turns device ON
#    device.off()           -->  turns device off
#    device.flip()          -->  flips device state, returns new state
#    device.set(new_value)  -->  sets device to new_value
#    device.info('state')   -->  returns current state of device
#    device.info('type')    -->  returns type device assigned to that outlet
#    device.info()          -->  defaults to 'all' which returns all info
#
#-----------------------INITIALIZE+SETUP DS18B20-------------------------

import RPi-GPIO as io
from time import time as now

class relay:
    def __init__(self, pin, name='not assigned', func_type='none'):
        self.type = func_type
        self.name = name
        self.pin = pin
        io.setmode(io.BCM)
        io.setwarnings(False)
        io.setup(self.pin, io.OUT, initial=HIGH)
        self.state = 0
        self.t_change = now()

#-----------------------ON/OFF FUNCTIONS---------------------------------

    def on(self):
        self.state = 1
        self.t_change = now()
        io.output(self.pin, io.LOW)

    def off(self):
        self.state = 0
        self.t_change = now()
        io.output(self.pin, io.HIGH)

    def flip(self):
        if self.state:
            self.off()
        elif not(self.state):
            self.on()
        return self.state

    def set(self, set_value):
        if set_value:
            self.on()
        elif not(set_value):
            self.off()

    def close(self):
        io.cleanup()

#----------------------------DEVICE INFO---------------------------------

    def info(self, which='all'):
        if which == 'all':
            return {'type': self.type, 'state': self.state, 't_change': self.t_change, 'pin': self.pin}
        elif which == 'state':
            return self.state
        elif which == 'time':
            return self.t_change
        elif which == 'type':
            return self.type
        elif which == 'pin':
            return self.pin
        elif which == 'sec':
            return round(now()-self.t_change, 2)
        elif which == 'min':
            return round((self.info('sec')/60), 2)

#-----------------------------------------------------------------------
