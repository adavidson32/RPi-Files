#--------------------------four_relays.py-------------------------------
#
# To use four_relays.py:
#     from four_relays import four_relays
#     outlet_pins = [4, 5, 6, 9]
#     outlet_names = ('bed light', 'futon light', 'desk light', 'iPhone charger')
#     ex. relays = four_relays(outlet_pins, outlet_names)
#     relays.on('all'), relays.on(1), relays.on([2,3,4]), relays.on('outlets-134'), relays.on(('bed light', 'futon light'))
#
#-----------------------INITIALIZE+SETUP DS18B20-------------------------

from single_relay import relay

class four_relays:
    def __init__(self, pins, names, types):
        Out = ('', '', '', '')
        self.Out[0] = relay(pins[0], names[0], types[0])
        self.Out[1] = relay(pins[1], names[1], types[1])
        self.Out[2] = relay(pins[2], names[2], types[2])
        self.Out[3] = relay(pins[3], names[3], types[3])
        self.states = [0, 0, 0, 0]
        self.times = [0, 0, 0, 0]
        self.types = (self.Out[0].info('type'), self.Out[1].info('type'), self.Out[2].info('type'), self.Out[3].info('type'))
        self.pins = (self.Out[0].info('pins'), self.Out[1].info('pins'), self.Out[2].info('pins'), self.Out[3].info('pins'))

#---------------------INFO REQUESTING-----------------------------------
# Call update_state_time() to retrieve state/t_change from single_relay.py and
# save to self.info state info....
# Call current_info or current_types to return all info or

    def retrieve_info_states(self):
        return (self.Out[0].info('state'), self.Out[1].info('state'), self.Out[2].info('state'), self.Out[3].info('state'))

    def retrieve_info_times(self):
        return (self.Out[0].info('time'), self.Out[1].info('time'), self.Out[2].info('time'), self.Out[3].info('time'))

    def retrieve_info_types(self):
        return (self.Out[0].info('type'), self.Out[1].info('type'), self.Out[2].info('type'), self.Out[3].info('type'))

    def retrieve_info_pins(self):
        return (self.Out[0].info('pin'), self.Out[1].info('pin'), self.Out[2].info('pin'), self.Out[3].info('pin'))

    def retrieve_info_all(self):
        return {'O1': self.Out[0].info('all'), 'O2': self.Out[1].info('all'), 'O3': self.Out[2].info('all'), 'O4': self.Out[3].info('all'))

#--------------------------Parsing Functions-----------------------------

    def calc(self, which, values=-1):
        type_which, len_which = type(which), len(which)
        type_values, len_values = type(values), len(values)
        which_outlets = [0, 0, 0, 0]
        value_assignments = []
        if (len_which > 4 or len_values > 4):
            return 'error: which or values is too large (>4)'
        if len_values == 1:
            v = self.v_parse(values)
            value_assignements = [v, v, v, v]
        elif len_values in [2, 3, 4]:
            for i in range(len_values):
                value_assignments[i] = self.v_parse(values[i])
        if len_which == 1:
            w = self.w_parse(which)
            which_outlets[w-1] = 1
        elif len_which in [2, 3, 4]:
            for i in range(len_which):
                which_outlets[self.w_parse(which[i])-1] = 1
        if (len_values != len_which) and (len_values != 1):
            print('issue likely detected due to length of value/which inputs')
        return which_outlets, value_assignments

    def v_parse(self, value):
        if values in ('flip', 'opposite', -1, [-1], '-1', (-1,)):
            return = -1
        elif values in ('on', 'ON', 'On', 1, '1', [1], (1,)):
            return = 1
        elif values in ('off', 'OFF', 'Off', 0, [0], (0,), '0'):
            return = 0

    def w_parse(self, which):
        if which in ('all', '1234', 'O1234', 'ALL', 'All', [1,1,1,1], 'Outlet1234'):
            return -1
        if which in ('Outlet1', 'O1', 'o1', 1, 0b1000):
            return 1
        if which in ('Outlet2', 'O2', 'o2', 2, 0b0100):
            return 2
        if which in ('Outlet3', 'O3', 'o3', 3, 0b0010):
            return 3
        if which in ('Outlet4', 'O4', 'o4', 4, 0b0001):
            return 4

#------------------------------------------------------------------------

    def update_states(self, outlets, values):
        #TD: After testing, remove or comment out all print statements
        #^^^ Maybe just leave 1x statement with new states....
        print('Using Outlets: {}'.format(outlets))
        print('Using Values: {}'.format(values))
        for i in range(4):
            if outlets[i]:
                if values[i] == -1:
                    self.states[i] = self.Out[i].flip()
                elif values[i] in [0, 1]:
                    self.Out[i].set(values[i])
                    self.states[i] = self.Out[i].info('state')
                self.t_change[i] = self.Out[i].info('time')

    def set(self, outlets, values):
        outlets_org, values_org = self.calc(outlets, values)
        self.update_states(outlets_org, values_org)
        #(PPPP) print("self.Out[i].info('states') : {}, {}, {}, {}".format(self.retrieve_info_states()))
        #^^^^ Above function (set) is called for every on/off/flip so good place to put print statements...
    def on(self, outlets):
        self.set(outlets, 'on')

    def off(self, outlets):
        self.set(outlets, 'off')

    def flip(self, outlets):
        self.set(outlets, 'flip')

#-------------------------------------------------------------------------
