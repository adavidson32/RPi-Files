#--------------------------OUTLET VARIABLES------------------------------

class variables:
    def __init__(self):
        self.Outlets = {'O1': {'pin': 19, 'type': 'none' , 'name': 'O1'         , 'state': 0, 't_change': 0},
                        'O2': {'pin': 5 , 'type': 'none' , 'name': 'O2'         , 'state': 0, 't_change': 0},
                        'O3': {'pin': 6 , 'type': 'light', 'name': 'desk light' , 'state': 0, 't_change': 0},
                        'O4': {'pin': 13, 'type': 'light', 'name': 'room lights', 'state': 0, 't_change': 0}}
        self.outlet_keys = [key for key in self.Outlets.keys()]
        self.outlet_pins = [self.Outlets[key]['pin'] for key in self.outlet_keys]
        #self.Outlets['O1']['pin'], self.Outlets['O2']['pin'], self.Outlets['O3']['pin'], self.Outlets['O4']['pin'])
        self.outlet_names = [self.Outlets[key]['name'] for key in self.outlet_keys]
        #(Outlets['O1']['name'], Outlets['O2']['name'], Outlets['O3']['name'], Outlets['O4']['name'])
        self.outlet_types = [self.Outlets[key]['type'] for key in self.outlet_keys]
        self.outlet_states = [self.Outlets[key]['state'] for key in self.outlet_keys]
        for i in range(len(self.outlet_keys)):
            print("key('{}'), name('{:>15}, type('{:>8}'), pin('{:>2}'), state('{}'))".format(self.outlet_keys[i], self.outlet_names[i], self.outlet_types[i], self.outlet_pins[i], self.outlet_states[i]))
        self.ADAFRUIT_IO = {'KEY'     : '11e4014862694ae6a474e89ece59c049',
                            'USERNAME': 'adavidson93'}
        self.SUB_FEEDS = {'ifttt'   : 'IFTTT'}
        self.PUB_FEEDS = {'temp'    : 'RoomTemp',
                          'pressure': 'AirPressure',
                          'light'   : 'AmbientLight',
                          'pir'     : 'Motion',
                          'altitude': 'Altitude'}
        self.sample_rate = 10.0 #How often to send temperature value
        self.room_temp = 10.0 #Initial value (could be anything....)
        self.last = 0



#------------------------------------------------------------------------
