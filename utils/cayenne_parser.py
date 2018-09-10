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

import struct
import logging
import json
import base64
import components_dictionary as component
import codecs

CAYENNELPP_MAX_CHANNEL = 99
CAYENNELPP_MIN_SIZE_BYTES = 3

LPP_DIGITAL_INPUT = 0
LPP_DIGITAL_OUTPUT = 1
LPP_ANALOG_INPUT = 2
LPP_ANALOG_OUTPUT = 3
LPP_LUMINOSITY = 101
LPP_PRESENCE = 102
LPP_TEMPERATURE = 103
LPP_RELATIVE_HUMIDITY = 104
LPP_ACCELEROMETER = 113
LPP_BAROMETRIC_PRESSURE = 115
LPP_GYROMETER = 134
LPP_GPS = 136

LPP_DIGITAL_INPUT_NAME = "DigitalIn"
LPP_DIGITAL_OUTPUT_NAME = "DigitalOut"
LPP_ANALOG_INPUT_NAME = "AnalogIn"
LPP_ANALOG_OUTPUT_NAME = "AnalogOut"
LPP_LUMINOSITY_NAME = "Illuminance"
LPP_PRESENCE_NAME = "Presence"
LPP_TEMPERATURE_NAME = "Temperature"
LPP_RELATIVE_HUMIDITY_NAME = "RelativeHumidity"
LPP_ACCELEROMETER_NAME = "Accelerometer"
LPP_BAROMETRIC_PRESSURE_NAME = "BarometricPressure"
LPP_GYROMETER_NAME = "Gyrometer"
LPP_GPS_NAME = "Gps"

LPP_DIGITAL_INPUT_SIZE = 1          # 1 byte
LPP_DIGITAL_OUTPUT_SIZE = 1         # 1 byte
LPP_ANALOG_INPUT_SIZE = 2           # 2 bytes, 0.01 signed
LPP_ANALOG_OUTPUT_SIZE = 2          # 2 bytes, 0.01 signed
LPP_LUMINOSITY_SIZE = 2             # 2 bytes, 1 lux unsigned
LPP_PRESENCE_SIZE = 1               # 1 byte, 1
LPP_TEMPERATURE_SIZE = 2            # 2 bytes, 0.1C signed
LPP_RELATIVE_HUMIDITY_SIZE = 1      # 1 byte, 0.5% unsigned
LPP_ACCELEROMETER_SIZE = 6          # 2 bytes per axis, 0.001G
LPP_BAROMETRIC_PRESSURE_SIZE = 2    # 2 bytes 0.1 hPa Unsigned
LPP_GYROMETER_SIZE = 6              # 2 bytes per axis, 0.01 degrees/s
LPP_GPS_SIZE = 9                    # 3 byte lon/lat 0.0001 degrees, 3 bytes alt 0.01 meter

class CayenneParser ():
   def __init__(self):  
      pass

   def decodeCayenneLpp(self, input, timestamp):
      
      output = []      
      decoded = base64.b64decode(input)              
      offset = 0            
      
      while (offset < len(decoded)):
         if (self.validateCayenneLppSize (input)):                        
            
            channel = struct.unpack_from("B", decoded, offset)[0]                        
            offset = offset + 1
            
            data_type = struct.unpack_from("B", decoded, offset)[0]            
            offset = offset + 1                        

            if (self.validateCayenneLppChannel(channel)):
               if (data_type == LPP_DIGITAL_INPUT):  
                  if (offset + LPP_DIGITAL_INPUT_SIZE <= len(decoded)):                     
                     output.append({
                        "format": component.dictionary[LPP_DIGITAL_INPUT_NAME]["format"],                        
                        "value": str(struct.unpack_from("B", decoded, offset)[0]),
                        "id": LPP_DIGITAL_INPUT_NAME ,
                        "unit": component.dictionary[LPP_DIGITAL_INPUT_NAME]["unit"],
                        # "type": component.dictionary[LPP_DIGITAL_INPUT_NAME]["type"]
                     })             
                     offset = offset + LPP_DIGITAL_INPUT_SIZE               
                  else:
                     raise ValueError("Invalid Cayenne message")
               elif (data_type == LPP_DIGITAL_OUTPUT):                   
                  if (offset + LPP_DIGITAL_OUTPUT_SIZE <= len(decoded)):                                       
                     output.append({
                        "format": component.dictionary[LPP_DIGITAL_OUTPUT_NAME]["format"],                        
                        "value": str(struct.unpack_from("B", decoded, offset)[0]),
                        "id": LPP_DIGITAL_OUTPUT_NAME ,
                        "unit": component.dictionary[LPP_DIGITAL_OUTPUT_NAME]["unit"],
                        # "type": component.dictionary[LPP_DIGITAL_OUTPUT_NAME]["type"]
                     })             
                     offset = offset + LPP_DIGITAL_OUTPUT_SIZE               
                  else:
                     raise ValueError("Invalid Cayenne message")       
               elif (data_type == LPP_ANALOG_INPUT):
                  if (offset + LPP_ANALOG_INPUT_SIZE <= len(decoded)):                     
                     output.append({
                        "format": component.dictionary[LPP_ANALOG_INPUT_NAME]["format"],                        
                        "value": str(struct.unpack_from(">h", decoded, offset)[0] / 100.0 ),
                        "id": LPP_ANALOG_INPUT_NAME ,
                        "unit": component.dictionary[LPP_ANALOG_INPUT_NAME]["unit"],
                        # "type": component.dictionary[LPP_ANALOG_INPUT_NAME]["type"]                        
                     })             
                     offset = offset + LPP_ANALOG_INPUT_SIZE               
                  else:
                     raise ValueError("Invalid Cayenne message")                                 
               elif (data_type == LPP_ANALOG_OUTPUT):       
                  if (offset + LPP_ANALOG_OUTPUT_SIZE <= len(decoded)):                     
                     output.append({
                        "format": component.dictionary[LPP_ANALOG_OUTPUT_NAME]["format"],                        
                        "value": str(struct.unpack_from(">h", decoded, offset)[0] / 100.0 ),
                        "id": LPP_ANALOG_OUTPUT_NAME ,
                        "unit": component.dictionary[LPP_ANALOG_OUTPUT_NAME]["unit"],
                        # "type": component.dictionary[LPP_ANALOG_OUTPUT_NAME]["type"]
                     })             
                     offset = offset + LPP_ANALOG_OUTPUT_SIZE
                  else:
                     raise ValueError("Invalid Cayenne message")          
               elif (data_type == LPP_LUMINOSITY):
                  if (offset + LPP_LUMINOSITY_SIZE <= len(decoded)):                     
                     output.append({
                        "format": component.dictionary[LPP_LUMINOSITY_NAME]["format"],                        
                        "value": str(struct.unpack_from(">h", decoded, offset)[0]),
                        "id": LPP_LUMINOSITY_NAME ,
                        "unit": component.dictionary[LPP_LUMINOSITY_NAME]["unit"],
                        "type": component.dictionary[LPP_LUMINOSITY_NAME]["type"]
                     })             
                     offset = offset + LPP_LUMINOSITY_SIZE
                  else:
                     raise ValueError("Invalid Cayenne message")   
               elif (data_type == LPP_PRESENCE):
                  if (offset + LPP_PRESENCE_SIZE <= len(decoded)):                     
                     output.append({
                        "format": component.dictionary[LPP_PRESENCE_NAME]["format"],                        
                        "value": str(struct.unpack_from("?", decoded, offset)[0]),
                        "id": LPP_PRESENCE_NAME ,
                        "unit": component.dictionary[LPP_PRESENCE_NAME]["unit"],
                        # "type": component.dictionary[LPP_PRESENCE_NAME]["type"]
                     })
                     offset = offset + LPP_PRESENCE_SIZE
                  else:
                     raise ValueError("Invalid Cayenne message")                  
               elif (data_type == LPP_TEMPERATURE):   
                  if (offset + LPP_TEMPERATURE_SIZE <= len(decoded)):                     
                     output.append({
                        "format": component.dictionary[LPP_TEMPERATURE_NAME]["format"],                        
                        "value": str(struct.unpack_from(">h", decoded, offset)[0] / 10.0 ),
                        "id": LPP_TEMPERATURE_NAME ,
                        "unit": component.dictionary[LPP_TEMPERATURE_NAME]["unit"],
                        "type": component.dictionary[LPP_TEMPERATURE_NAME]["type"]                        
                     })
                     offset = offset + LPP_TEMPERATURE_SIZE               
                  else:
                     raise ValueError("Invalid Cayenne message")                                       
               elif (data_type == LPP_RELATIVE_HUMIDITY):   
                  if (offset + LPP_RELATIVE_HUMIDITY_SIZE <= len(decoded)):                     
                     output.append({
                        "format": component.dictionary[LPP_RELATIVE_HUMIDITY_NAME]["format"],                        
                        "value": str(struct.unpack_from("B", decoded, offset)[0]  / 2.0),
                        "id": LPP_RELATIVE_HUMIDITY_NAME ,
                        "unit": component.dictionary[LPP_RELATIVE_HUMIDITY_NAME]["unit"],
                        "type": component.dictionary[LPP_RELATIVE_HUMIDITY_NAME]["type"]                        
                     })             
                     offset = offset + LPP_RELATIVE_HUMIDITY_SIZE        
                  else:
                     raise ValueError("Invalid Cayenne message")                  
               elif (data_type == LPP_ACCELEROMETER):
                  if (offset + LPP_GYROMETER_SIZE <= len(decoded)):                    
                     output.append({
                        "format": component.dictionary[LPP_ACCELEROMETER_NAME]["format"],                        
                        "value": str(struct.unpack_from(">h", decoded, offset)[0] / 1000.0),
                        "id": LPP_ACCELEROMETER_NAME + "X",
                        "unit": component.dictionary[LPP_ACCELEROMETER_NAME]["unit"],
                        # "type": component.dictionary[LPP_ACCELEROMETER_NAME]["type"]
                     })
                     output.append({
                        "format": component.dictionary[LPP_ACCELEROMETER_NAME]["format"],                        
                        "value": struct.unpack_from(">h", decoded, offset + 2)[0] / 1000.0,
                        "id": LPP_ACCELEROMETER_NAME + "Y",
                        "unit": component.dictionary[LPP_ACCELEROMETER_NAME]["unit"],
                        # "type": component.dictionary[LPP_ACCELEROMETER_NAME]["type"]
                     })
                     output.append({
                        "format": component.dictionary[LPP_ACCELEROMETER_NAME]["format"],                        
                        "value": struct.unpack_from(">h", decoded, offset + 4)[0] / 1000.0,
                        "id": LPP_ACCELEROMETER_NAME + "Z",
                        "unit": component.dictionary[LPP_ACCELEROMETER_NAME]["unit"],
                        # "type": component.dictionary[LPP_ACCELEROMETER_NAME]["type"]
                     })
                     offset += LPP_ACCELEROMETER_SIZE
                  else:
                     raise ValueError("Invalid Cayenne message")        
               elif (data_type == LPP_BAROMETRIC_PRESSURE):    
                  if (offset + LPP_BAROMETRIC_PRESSURE_SIZE <= len(decoded)):
                     output.append({
                        "format": component.dictionary[LPP_RELATIVE_HUMIDITY_NAME]["format"],                        
                        "value": str(struct.unpack_from(">h", decoded, offset)[0] / 10.0),
                        "id": LPP_BAROMETRIC_PRESSURE_NAME ,
                        "unit": component.dictionary[LPP_BAROMETRIC_PRESSURE_NAME]["unit"],
                        # "type": component.dictionary[LPP_BAROMETRIC_PRESSURE_NAME]["type"],
                     })                                   
                     offset = offset + LPP_BAROMETRIC_PRESSURE_SIZE               
                  else:
                     raise ValueError("Invalid Cayenne message")        
               elif (data_type == LPP_GYROMETER):                  
                  if (offset + LPP_GYROMETER_SIZE <= len(decoded)):
                     output.append({
                        "format": component.dictionary[LPP_GYROMETER_NAME]["format"],                        
                        "value": str(struct.unpack_from(">h", decoded, offset)[0] / 100.0),
                        "id": LPP_GYROMETER_NAME + "X",
                        "unit": component.dictionary[LPP_GYROMETER_NAME]["unit"],
                        # "type": component.dictionary[LPP_GYROMETER_NAME]["type"]
                     })
                     output.append({
                        "format": component.dictionary[LPP_GYROMETER_NAME]["format"],                        
                        "value": struct.unpack_from(">h", decoded, offset + 2)[0] / 100.0,
                        "id": LPP_GYROMETER_NAME + "Y",
                        "unit": component.dictionary[LPP_GYROMETER_NAME]["unit"],
                        # "type": component.dictionary[LPP_GYROMETER_NAME]["type"]                        
                     })
                     output.append({
                        "format": component.dictionary[LPP_GYROMETER_NAME]["format"],                        
                        "value": struct.unpack_from(">h", decoded, offset + 4)[0] / 100.0,
                        "id": LPP_GYROMETER_NAME +"Z",
                        "unit": component.dictionary[LPP_GYROMETER_NAME]["unit"],
                        # "type": component.dictionary[LPP_GYROMETER_NAME]["type"]
                     })
                     offset += LPP_GYROMETER_SIZE
                  else:
                     raise ValueError("Invalid Cayenne message")     
               elif (data_type == LPP_GPS):
                  if (offset + LPP_GPS_SIZE <= len(decoded)):                                   
                     output.append({
                        "format": component.dictionary["Latitude"]["format"],                        
                        "value": str(self.readInt24BR(decoded, offset) / 10000.0),
                        "id": "Latitude",
                        "unit": component.dictionary["Latitude"]["unit"],
                        "type": component.dictionary["Latitude"]["type"]
                     })
                     output.append({
                        "format": component.dictionary["Longitude"]["format"],                        
                        "value": str(self.readInt24BR(decoded, offset + 3) / 10000.0),
                        "id": "Longitude" ,
                        "unit": component.dictionary["Longitude"]["unit"],
                        "type": component.dictionary["Latitude"]["type"]
                     })
                     output.append({
                        "format": component.dictionary["Altitude"]["format"],                        
                        "value": str(self.readInt24BR(decoded, offset + 6) / 100.0),
                        "id": "Altitude",
                        "unit": component.dictionary["Altitude"]["unit"],
                        "type": component.dictionary["Latitude"]["type"]                        
                     })
                     offset += LPP_GPS_SIZE                                                             
                  else:
                     raise ValueError("Invalid Cayenne message")
               else: 
                  raise ValueError("Invalid Cayenne LPP data type (" + str(data_type) + ")")
            else:
               raise ValueError("Invalid Cayenne LPP channel (" + str(channel) + ")")
         else: 
            raise ValueError("Invalid Cayenne LPP payload (size)")
      
      return output

   def validateCayenneLppSize (self, buffer):      
      return True if (buffer and len(buffer) >= CAYENNELPP_MIN_SIZE_BYTES) else False

   def validateCayenneLppChannel (self, channel):           
      return True if channel < CAYENNELPP_MAX_CHANNEL else False

   def readInt24BR (self, buffer, offset):             
      out = bytes([struct.unpack_from("B", buffer, offset)[0],
      struct.unpack_from("B", buffer, offset + 1)[0],
      struct.unpack_from("B", buffer, offset + 2)[0]])
      out = int.from_bytes(out, byteorder="big", signed=True)            
      return out
