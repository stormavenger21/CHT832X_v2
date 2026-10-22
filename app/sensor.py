"""
October 16, 2026
This code is for the CHT832X temperature and humidity sensor from DF Robot, ppart number SEN0546

=====Instructions=====
connect the CHT832X directly to the pi header:
| Pi Pins  |  CHT832x |
| ---      |  ---     |
| 3        | yellow   |
| 4        | red      |
| 5        | green    |
| 6        | black    |

"""

import time

from smbus2 import SMBus, i2c_msg

class CHT832x:
    ADDRESS = 0x44
    MEASURE_COMMAND = [0x24, 0x00]

    def __init__(self, bus_number=1):
        self.bus_number = bus_number

    @staticmethod
    def _crc8(data):
        """Calculate the sensor's CRC-8 checksum."""
        crc = 0xFF

        for byte in data:
            crc ^= byte

            for _ in range(8):
                if crc & 0x80:
                    crc = ((crc << 1) ^ 0x31) & 0xFF
                else:
                    crc = (crc << 1) & 0xFF

        return crc

    def read(self):
        """Read temperature in Celsius and relative humidity."""
        with SMBus(self.bus_number) as bus:
            bus.write_i2c_block_data(
                self.ADDRESS,
                self.MEASURE_COMMAND[0],
                [self.MEASURE_COMMAND[1]],
            )
            time.sleep(0.060)
            try:
               data=i2c_msg.read(self.ADDRESS,6)
               bus.i2c_rdwr(data)
               data=list(data)
            except Exception as e:
               print(f"Error: {e}")

        if len(data) != 6:
            raise IOError("Incomplete CHT832x measurement")

        # Validate the temperature and humidity checksums.
        if self._crc8(data[0:2]) != data[2]:
            raise IOError("Temperature CRC mismatch")

        if self._crc8(data[3:5]) != data[5]:
            raise IOError("Humidity CRC mismatch")

        raw_temperature = (data[0] << 8) | data[1]
        raw_humidity = (data[3] << 8) | data[4]

        temperature = (
            -45.0 + 175.0 * raw_temperature / 65535.0
        )

        humidity = 100.0 * raw_humidity / 65535.0

        return {
            "temperature_c": round(temperature, 2),
            "humidity_rh": round(humidity, 2),
        }
