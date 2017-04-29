import logging
import Adafruit_GPIO.I2C as I2C

i2c = I2C()
# BMP280 default address.
BMP280_I2CADDR = 0x76
BMP280_CHIPID = 0xD0
# BMP280 Registers
BMP280_DIG_T1 = 0x88  # R   Unsigned Calibration data (16 bits)
BMP280_DIG_T2 = 0x8A  # R   Signed Calibration data (16 bits)
BMP280_DIG_T3 = 0x8C  # R   Signed Calibration data (16 bits)
BMP280_DIG_P1 = 0x8E  # R   Unsigned Calibration data (16 bits)
BMP280_DIG_P2 = 0x90  # R   Signed Calibration data (16 bits)
BMP280_DIG_P3 = 0x92  # R   Signed Calibration data (16 bits)
BMP280_DIG_P4 = 0x94  # R   Signed Calibration data (16 bits)
BMP280_DIG_P5 = 0x96  # R   Signed Calibration data (16 bits)
BMP280_DIG_P6 = 0x98  # R   Signed Calibration data (16 bits)
BMP280_DIG_P7 = 0x9A  # R   Signed Calibration data (16 bits)
BMP280_DIG_P8 = 0x9C  # R   Signed Calibration data (16 bits)
BMP280_DIG_P9 = 0x9E  # R   Signed Calibration data (16 bits)
BMP280_CONTROL = 0xF4
BMP280_RESET = 0xE0
BMP280_CONFIG = 0xF5
BMP280_PRESSUREDATA = 0xF7
BMP280_TEMPDATA = 0xFA

#----------------------------------------------------------------------
units_std = {'temp': 'f', 'pressure': 'atm', 'altitude': 'feet'}
units_met = {'temp': 'c', 'pressure': 'Pa', 'altitude': 'meters'}
# temp units = 'f' or 'c', pressure units = 'Pa' or 'atm', altitude units = 'meters' or 'feet'
dec_places_std = {'temp': 2, 'pressure': 3, 'altitude': 1}
dec_places_met = {'temp': 2, 'pressure': 1, 'altitude': 1}

# Usage:
#   from bmp280 import BMP280
#   bmp = BMP280(units, dec_places) <-- units and dec_places example shown above....
#   temp = bmp.

#----------------------------------------------------------------------

class BMP280(object):
    def __init__(self, address=BMP280_I2CADDR, i2c=None, **kwargs, units=units_std, dec_places=dec_places_std):
        self._logger = logging.getLogger('Adafruit_BMP.BMP280')
        self._device = i2c.get_i2c_device(address, **kwargs)
        chip_ip = self._device.readU8(BMP280_CHIPID)
        print("Chip ID = ", str(chip_id))
        #if chip_id != 0x58:
        #    raise Exception('Unsupported chip')
        # Load calibration values.
        self._load_calibration()
        self._device.write8(BMP280_CONTROL, 0x3F)
        self.units_temp = units['temp']
        self.units_pressure = units['pressure']
        self.units_altitude = units['altitude']
        self.dp_temp = dec_places['temp']
        self.dp_pressure = dec_places['pressure']
        self.dp_altitude = dec_places['altitude']

#----------------------------------------------------------------------

    def _load_calibration(self):
        self.cal_t1 = int(self._device.readU16(BMP280_DIG_T1))  # UINT16
        self.cal_t2 = int(self._device.readS16(BMP280_DIG_T2))  # INT16
        self.cal_t3 = int(self._device.readS16(BMP280_DIG_T3))  # INT16
        self.cal_p1 = int(self._device.readU16(BMP280_DIG_P1))  # UINT16
        self.cal_p2 = int(self._device.readS16(BMP280_DIG_P2))  # INT16
        self.cal_p3 = int(self._device.readS16(BMP280_DIG_P3))  # INT16
        self.cal_p4 = int(self._device.readS16(BMP280_DIG_P4))  # INT16
        self.cal_p5 = int(self._device.readS16(BMP280_DIG_P5))  # INT16
        self.cal_p6 = int(self._device.readS16(BMP280_DIG_P6))  # INT16
        self.cal_p7 = int(self._device.readS16(BMP280_DIG_P7))  # INT16
        self.cal_p8 = int(self._device.readS16(BMP280_DIG_P8))  # INT16
        self.cal_p9 = int(self._device.readS16(BMP280_DIG_P9))  # INT16
        self._logger.debug('T1 = {0:6d}'.format(self.cal_t1))
        self._logger.debug('T2 = {0:6d}'.format(self.cal_t2))
        self._logger.debug('T3 = {0:6d}'.format(self.cal_t3))
        self._logger.debug('P1 = {0:6d}'.format(self.cal_p1))
        self._logger.debug('P2 = {0:6d}'.format(self.cal_p2))
        self._logger.debug('P3 = {0:6d}'.format(self.cal_p3))
        self._logger.debug('P4 = {0:6d}'.format(self.cal_p4))
        self._logger.debug('P5 = {0:6d}'.format(self.cal_p5))
        self._logger.debug('P6 = {0:6d}'.format(self.cal_p6))
        self._logger.debug('P7 = {0:6d}'.format(self.cal_p7))
        self._logger.debug('P8 = {0:6d}'.format(self.cal_p8))
        self._logger.debug('P9 = {0:6d}'.format(self.cal_p9))

    def _load_datasheet_calibration(self):
        # Set calibration from values in the datasheet example.  Useful for debugging the
        # temp and pressure calculation accuracy.
        self.cal_t1 = 27504
        self.cal_t2 = 26435
        self.cal_t3 = -1000
        self.cal_p1 = 36477
        self.cal_p2 = -10685
        self.cal_p3 = 3024
        self.cal_p4 = 2855
        self.cal_p5 = 140
        self.cal_p6 = -7
        self.cal_p7 = 15500
        self.cal_p8 = -14500
        self.cal_p9 = 6000

    def read_raw(self, register):
        """Reads the raw (uncompensated) temperature or pressure from the sensor."""
        raw = self._device.readU16BE(register)
        raw <<= 8
        raw = raw | self._device.readU8(register + 2)
        raw >>= 4
        self._logger.debug('Raw value 0x{0:X} ({1})'.format(raw & 0xFFFF, raw))
        return raw

    def _compensate_temp(self, raw_temp):
        """ Compensate temperature """
        t1 = (((raw_temp >> 3) - (self.cal_t1 << 1)) *
              (self.cal_t2)) >> 11
        t2 = (((((raw_temp >> 4) - (self.cal_t1)) *
                ((raw_temp >> 4) - (self.cal_t1))) >> 12) *
              (self.cal_t3)) >> 14
        return t1 + t2

#----------------------------------------------------------------------

    def temp(self, units=self.units_temp, dp=self.dp_temp):
        """Gets the compensated temperature in degrees celsius."""
        raw_temp = self.read_raw(BMP280_TEMPDATA)
        compensated_temp = self._compensate_temp(raw_temp)
        temp = float(((compensated_temp * 5 + 128) >> 8)) / 100
        self._logger.debug('Calibrated temperature {0}'.format(temp))
        if units = 'f':
            temp = ((temp * 1.8) + 32.0)
        return round(temp, dp)

#----------------------------------------------------------------------

    def pressure(self, units=self.units_pressure, dp=self.dp_pressure):
        """Gets the compensated pressure in Pascals."""
        raw_temp = self.read_raw(BMP280_PRESSUREDATA)
        compensated_temp = self._compensate_temp(raw_temp)
        p1 = compensated_temp - 128000
        p2 = p1 * p1 * self.cal_p6
        p2 += (p1 * self.cal_p6) << 17
        p2 += self.cal_p4 << 35
        p1 = ((p1 * p1 * self.cal_p3) >> 8) + ((p1 * self.cal_p2) << 12)
        p1 = ((1 << 47) + p1) * (self.cal_p1) >> 33
        if 0 == p1:
            return 0
        p = 1048576 - raw_temp
        p = (((p << 31) - p2) * 3125) / p1
        p1 = (self.cal_p9 * (p >> 13) * (p >> 13)) >> 25
        p2 = (self.cal_p8 * p) >> 19
        p = ((p + p1 + p2) >> 8) + ((self.cal_p7) << 4)
        p_ret = float(p / 256)
        if units = 'atm':
            p_ret = p_ret * 0.00000986923169
        return round(p_ret, dp)

#----------------------------------------------------------------------

    def altitude(self, sealevel_pa=101325.0):
        """Calculates the altitude in meters."""
        # Calculation taken straight from section 3.6 of the datasheet.
        pressure = float(self.pressure())
        altitude = 44330.0 * (1.0 - pow(pressure / sealevel_pa, (1.0 / 5.255)))
        self._logger.debug('Altitude {0} m'.format(altitude))
        return altitude

#----------------------------------------------------------------------

    def read_sealevel_pressure(self, altitude_m=0.0):
        """Calculates the pressure at sealevel when given a known altitude in
        meters. Returns a value in Pascals."""
        pressure = float(self.pressure())
        p0 = pressure / pow(1.0 - altitude_m / 44330.0, 5.255)
        self._logger.debug('Sealevel pressure {0} Pa'.format(p0))
        return p0

#----------------------------------------------------------------------
