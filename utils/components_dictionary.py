#  Copyright (C) 2018 ATOS Spain
 
#  This file is part of VICINITY.
 
#  VICINITY is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
 
#  VICINITY is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
 
#  You should have received a copy of the GNU General Public License
#  along with VICINITY.  If not, see <http://www.gnu.org/licenses/>

dictionary = {
  'Temperature': {
    'unit': 'Degree celsius (C)',
    'format': 'float',
    'type': 'adapters:DeviceTemperature'
  },
  'RelativeHumidity': {
    'unit': '%',
    'format': 'float',
    'type': 'adapters:RelativeHumidity'
  },
  'BarometricPressure': {
    'unit': 'Pascals',
    'format': 'float',
    # 'type': 'BarometricPressureSensor'
  },
  'DigitalIn': {
    'unit': 'unitless',
    'format': 'float',
    # 'type': 'DigitalInSensor'
  },
  'DigitalOut': {
    'unit': 'unitless',
    'format': 'float',
    # 'type': 'DigitalOutSensor'
  },
  'AnalogIn': {
    'unit': 'unitless',
    'format': 'float',
    # 'type': 'AnalogInSensor'
  },
  'AnalogOut': {
    'unit': 'unitless',
    'format': 'float',
    # 'type': 'AnalogOutSensor'
  },
  'Illuminance':{
    'unit': 'Lux',
    'format': 'integer',
    'type': 'adapters:Luminance'
  },
  'Latitude': {
    'unit': 'Decimal Degrees',
    'format': 'float',
    'type': 'adapters:Location'
  },  
  'Longitude': {
    'unit': 'Decimal Degrees',
    'format': 'float',
    'type': 'adapters:Location'
  },
  'Altitude': {
    'unit': 'Meters',
    'format': 'float',
    'type': 'adapters:Location'
  },
  'SNR': {
    'unit': 'dB',
    'format': 'float',
    # 'type': 'SnrSensor'
  },
  'RSSI': {
    'unit': 'dBm',
    'format': 'float',
    # 'type': 'RssiSensot'
  },
  'Accelerometer': {
    'unit': 'G',
    'format': 'float',
    # 'type': 'Accelerometer'
  },
  'Gyrometer': {
    'unit': 'Degrees per second',
    'format': 'float',
    # 'type': 'Gyrometer'
  },
  'Presence': {
    'unit': 'boolean',
    'format': 'boolean',
    # 'type': 'PresenceSensor'
  }
}