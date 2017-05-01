#-------------------------------ds18b20.py------------------------------

# Use:
#   ds = DS18B20('f', 3)  -->  use fahrenheit with 3 decimal places
#   ds = DS18B20()        -->  use default values (units='c', decimal_places=2)
#   ds.temp(0)            -->  return temp value for sensor #0 (float)
#   ds.temps()            -->  return all temp values on 1-wire bus (tuple of floats)
#   ds.device_count()     -->  returns number of ds18b20 sensors detected (int)

#-----------------------INITIALIZE+SETUP DS18B20-------------------------

import os, glob, time

class DS18B20:
    def __init__(self, units='c', decimal_places=2):
        self.units = 1 if (units == 'f') else 0
        # load required kernel modules
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')
        # Find file names for the sensor(s)
        base_dir = '/sys/bus/w1/devices/'
        device_folder = glob.glob(base_dir + '28*')
        self._num_devices = len(device_folder)
        self._device_file = list()
        self.dec_places = decimal_places
        i = 0
        while i < self._num_devices:
            self._device_file.append(device_folder[i] + '/w1_slave')
            i += 1

    #-----------------------DEVICE COUNT------------------------------------

    def num_ds(self):
        # call this to see how many sensors have been detected
        return self._num_devices

    #------------------INTERNAL TEMP CALC - DONT USE------------------------

    def _read_temp(self,index):
        # Issue one read to one sensor
        # you should not call this directly
        f = open(self._device_file[index],'r')
        lines = f.readlines()
        f.close()
        return lines

    #------------------------SINGLE TEMP CALC-------------------------------

    def temp(self, index=0, units=0):
        if units == 0:
            units = self.units
        # call this to get the temperature in degrees C
        # detected by a sensor
        lines = self._read_temp(index)
        retries = 5
        while (lines[0].strip()[-3:] != 'YES') and (retries > 0):
            # read failed so try again
            time.sleep(0.1)
            #print('Read Failed', retries)
            lines = self._read_temp(index)
            retries -= 1
        if retries == 0:
            return 998
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp = lines[1][equals_pos + 2:]
            temp = float(temp)/1000
            if units:
                temp = ((temp * 1.8) + 32.0)
            return round(temp, self.dec_places)
        else:
            # error
            return 999

    #------------------------ALL TEMP CALC-----------------------------------

    def temps(self):
        temps = ('',)
        for i in range(device_count):
            temps += (round(temp(i), self.dec_places),)
        return temps[1:]

    #-----------------------------------------------------------------------
