#--------------------------four_relays.py-------------------------------

# To use four_relays.py:
#     from four_relays import four_relays
#     outlet_pins = [4, 5, 6, 9]
#     outlet_names = ('bed light', 'futon light', 'desk light', 'iPhone charger')
#     ex. relays = four_relays(outlet_pins, outlet_names)
#     relays.on('all'), relays.on(1), relays.on([2,3,4]), relays.on('outlets-134'), relays.on(('bed light', 'futon light'))

#-----------------------INITIALIZE+SETUP DS18B20-------------------------

from single_relay import relay
from type_test import type_test, is_int, is_str, is_strint

class four_relays:
    def __init__(self, pins, names, types):
        self.Outlet1 = relay(pins[0], names[0], types[0])
        self.Outlet2 = relay(pins[1], names[1], types[1])
        self.Outlet3 = relay(pins[2], names[2], types[2])
        self.Outlet4 = relay(pins[3], names[3], types[3])
        self.Out = (self.Outlet1, self.Outlet2, self.Outlet3, self.Outlet4)
        self.names = names
        self.states = [0, 0, 0, 0]
        self.times = [0, 0, 0, 0]
        self.types = (self.Out[0].info('type'), self.Out[1].info('type'), self.Out[2].info('type'), self.Out[3].info('type'))
        self.pins = (self.Out[0].info('pins'), self.Out[1].info('pins'), self.Out[2].info('pins'), self.Out[3].info('pins'))

    #---------------------INFO REQUESTING-----------------------------------
    # Call update_state_time() to retrieve state/t_change from single_relay.py and
    # save to self.info state info....
    # Call current_info or current_types to return all info or

    def retrieve_info_states(self):
        return [self.Out[0].info('state'), self.Out[1].info('state'), self.Out[2].info('state'), self.Out[3].info('state')]

    def retrieve_info_times(self):
        return (self.Out[0].info('time'), self.Out[1].info('time'), self.Out[2].info('time'), self.Out[3].info('time'))

    def retrieve_info_types(self):
        return (self.Out[0].info('type'), self.Out[1].info('type'), self.Out[2].info('type'), self.Out[3].info('type'))

    def retrieve_info_pins(self):
        return (self.Out[0].info('pin'), self.Out[1].info('pin'), self.Out[2].info('pin'), self.Out[3].info('pin'))

    def retrieve_info_all(self):
        return {'O1': self.Out[0].info('all'), 'O2': self.Out[1].info('all'), 'O3': self.Out[2].info('all'), 'O4': self.Out[3].info('all')}

    #--------------------------Parsing Functions-----------------------------

    def calc(self, which, values=-1):
        print('starting calc with which=({}), values=({})'.format(which, values))
        which_outlets = [0, 0, 0, 0]
        value_assignments = self.retrieve_info_states()

        type_values, len_values = type_test(values, options='len')
        if type_values in ('int', 'str-int', 'str'):
            len_values = 1
            v = self.v_parse(values)
            print('v = ', v)
            value_assignments = (v, v, v, v)
        elif type_values in ('tuple', 'list'):
            if len_values not in (1, 2, 3, 4):
                print('too many values entered (enter 4 or less via list/tuple)')
            elif len_values == 1:
                v = self.v_parse(values)
                value_assignments = (v, v, v, v)
            else:
                for i in range(len_values):
                    value_assignments[i] = self.v_parse(values[i])
        print('Value  -->>  |type: {}| && |len: {}| && |value_assignements: {}|'.format(type_values, len_values, value_assignments))

        type_which, len_which = type_test(which, options='len')
        if (len_values != len_which) and (len_values != 1):
            print('Issue likely detected: (len_values != 1) and (len_values != len_which)')
        if type_which in ('tuple', 'list'):
            if len_which not in (1, 2, 3, 4):
                print('too many outlet addresses entered (enter 4 or less via list/tuple)')
            elif len_which == 1:
                w = self.w_parse(which)
                if w == -1:                     # (w == -1) if (which_outlets == 'all')
                    which_outlets = (1, 1, 1, 1)
                else:
                    which_outlets[w-1] = 1      # (w != -1) if (which_outlets in [1, 2, 3, 4])
            else:
                for i in range(len_which):
                    which_outlets[self.w_parse(which[i])-1] = 1
        elif type_which in ('str-int', 'int', 'str'):
            len_which = 1
            w = self.w_parse(which)
            print('w = ', w)
            if w == -1:                     # (w == -1) if (which_outlets == 'all')
                which_outlets = (1, 1, 1, 1)
            else:
                which_outlets[w-1] = 1      # (w != -1) if (which_outlets in [1, 2, 3, 4])
        print('Which  -->>  |type: {}| && |len: {}| && |which_outlets: {}|'.format(type_which, len_which, which_outlets))
        return which_outlets, value_assignments

    def v_parse(self, value):
        print('starting v_parse')
        if value in ('flip', 'opposite', -1, [-1], '-1', (-1,)):
            return -1
        elif value in ('on', 'ON', 'On', 1, '1', [1], (1,)):
            return 1
        elif value in ('off', 'OFF', 'Off', 0, [0], (0,), '0'):
            return 0
        else:
            print("Assigned Value ({}) is not in ('ON', 'OFF', 'flip', 1, 0, -1, etc.)".format(value))
            return 'error'

    def w_parse(self, which):
        print('starting w_parse')
        if which in ('all', '1234', 'ALL', 'All', 1234, '*', 'a'):
            return -1
        elif which in ('1', 1, 0b1000):
            return 1
        elif which in ('2', 2, 0b0100):
            return 2
        elif which in ('3', 3, 0b0010):
            return 3
        elif which in ('4', 4, 0b0001):
            return 4
        elif which in self.names:
            return (self.names.index(which) + 1)
        else:
            print("Assigned address ({}) is not in ('Outlet1', 'Outlet2', 'all', 'O1', 0b1011, etc.)".format(which))
            return 'error'

    #------------------------------------------------------------------------

    def update_states(self, outlets, values):
        print('starting update_states')
        #TD: After testing, remove or comment out all print statements
        #^^^ Maybe just leave 1x statement with new states....
        print('Using Outlets: {}'.format(outlets))
        print('Using Values: {}'.format(values))
        for i in range(4):
            if outlets[i] == 1:
                if values[i] == -1:
                    self.states[i] = self.Out[i].flip()
                elif values[i] in [0, 1]:
                    self.Out[i].set(values[i])
                    self.states[i] = self.Out[i].info('state')
                print('Outlet #{} changed to ({})'.format((i+1), self.states[i]))
                self.times[i] = self.Out[i].info('time')

    def set(self, outlets, values):
        print('starting set')
        outlets_org, values_org = self.calc(outlets, values)
        print('outlets_org: {}'.format(outlets_org))
        print('values_org: {}'.format(values_org))
        self.update_states(outlets_org, values_org)
        #(PPPP) print("self.Out[i].info('states') : {}, {}, {}, {}".format(self.retrieve_info_states()))
        #^^^^ Above function (set) is called for every on/off/flip so good place to put print statements...

    def on(self, outlets):
        print('starting on with outlets = ({})'.format(outlets))
        self.set(outlets, 'on')

    def off(self, outlets):
        self.set(outlets, 'off')

    def flip(self, outlets):
        self.set(outlets, 'flip')

    def close(self):
        self.Out[0].close()
        self.Out[0].close()
        self.Out[0].close()
        self.Out[0].close()

    #-------------------------------------------------------------------------
