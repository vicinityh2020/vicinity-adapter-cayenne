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

import os, sys
import paho.mqtt.client as mqtt
import threading
import logging
import random
import pydash.strings
import json # Testing (to be removed in production)
import datetime # Testing

from thing_validation import ThingDescriptionValidation
import components_dictionary as component
import cayenne_parser
import globals as globals

class LoRaServerClient (threading.Thread):
   
   def __init__(self):      
      self._logger = logging.getLogger('VICINITY_LOG')       
      self._cayenne = cayenne_parser.CayenneParser()
      self._validator = ThingDescriptionValidation()
      
      self._active_timer = {}      
      self._thread = threading.Thread(target=self.Start, name='LoRaServer_thread')      
      # self._thread = threading.Thread(target=self.TestParser, name='LoRaServer_thread')
      self._loraserver_topic = 'application/+/node/+/rx'
      self._thread.daemon = True
      self._thread.start()       

   def TestParser(self):                  
      
      self._active_timer = threading.Timer(6, self.TestParser)                              
      self._active_timer.start()
      self._mqttc = mqtt.Client()  

      random_value = random.randint(0,3)

      raw = {
            'applicationID': '1',
            'applicationName': 'my-app',
            # 'deviceName': 'Seeduino' ,            
            # 'devEUI': '3339343771356214' ,         
            # 'deviceName': 'Seeduino_' + str(random_value),            
            'deviceName': '333934377135621' + str(random_value),          
            'devEUI': '333934377135621' + str(random_value),            
            'rxInfo': [
                  {
                        'mac': '0000000000010203',
                        'time': datetime.datetime.now().isoformat(),
                        'rssi': -49,
                        'loRaSNR': 10,
                        'name': '0000000000010203',
                        'latitude': 10,
                        'longitude': 20,
                        'altitude': -1
                  }
            ],
            'txInfo': {
                  'frequency': 868100000,
                  'dataRate': {
                        'modulation': 'LORA',
                        'bandwidth': 125,
                        'spreadFactor': 7
                  },
                  'adr': True,
                  'codeRate': '4/5'
            },
            'fCnt': 73,
            'fPort': 8,
            'data': 'AmcA7QNoTw=='
      }    
      self.ParsePayload (raw)     
        

   def Start(self):
      self._logger.info('LoRaServer client thread instanced')        
      self._mqttc = mqtt.Client()      
           
      # Assign event callbacks
      self._mqttc.on_connect = self.on_connect
      self._mqttc.on_message = self.on_message
      self._mqttc.on_subscribe = self.on_subscribe
      
      self._mqttc.username_pw_set(os.environ.get('LORAWAN_APPID'), os.environ.get('LORAWAN_PSW'))      

      self._mqttc.connect(os.environ.get('LORAWAN_MQTT_URL'), \
            int(1883 if not(os.environ.get('LORAWAN_MQTT_PORT')) else os.environ.get('LORAWAN_MQTT_PORT')), 60) 

      # and listen to server
      run = True
      while run:
         self._mqttc.loop()

   def on_connect (self, mqttc, mosq, obj, rc):            
      if rc == 0:
         self._logger.info('Connected to MQTT Broker - ' + os.environ.get('LORAWAN_MQTT_URL'))
      else:
         self._logger.error('Connection error to MQTT Broker - ' + os.environ.get('LORAWAN_MQTT_URL'))        
      
      # subscribe for all devices of user (tailor to every MQTT Broker)
      mqttc.subscribe(self._loraserver_topic)  

   def on_message (self, mqttc,obj,msg):            
      raw = json.loads(msg.payload.decode())    
      if (raw != None):                              
            self.ParsePayload (raw)            

   def on_publish(self, mosq, obj, mid):
      self._logger.debug('mid: ' + str(mid))      

   def on_subscribe(self, mosq, obj, mid, granted_qos):
      self._logger.debug('Subscribed: ' + str(mid) + ' ' + str(granted_qos))      

   def on_log(self, mqttc,obj,level,buf):
      self._logger.debugrint('message:' + str(buf))
      self._logger.debug('userdata:' + str(obj))   

   def ParsePayload(self,payload):
      data = {
            "name": "CAYENNE-" + payload["deviceName"],
            "oid": payload["devEUI"],            
            "type": "core:Device",
            "properties": [],
            "actions": [],
            "events": [],
            # Internal array to handle the last observations coming from the sensors
            "values": []
      }          

      # Parse the payload field (Cayenne parser)
      properties = self._cayenne.decodeCayenneLpp(payload['data'], str(payload['rxInfo'][0]['time']))  
         
      for i in properties:         
         if "type" in i:
            data["properties"].append(self.AddProperty(i, data["oid"]))                    
            data["events"].append(self.AddEvent(i, data["oid"]))   
            data["values"].append(self.AddValue(i, payload['rxInfo'][0]['time']))   

      # self._logger.debug("Message received - " + data['oid'])              

      # NOTE: If the validation is not carried out, the validator returns a "success" output
      validation = self._validator.validate(data)       
      if (validation['success']):                           
            globals.queue.put(data)
      else:
            self._logger.error("Thing Description did not pass the validation - list of errors: { " + \
                  pydash.strings.join(validation['error'], ',') + ' }' )            

   def AddProperty(self, property, oid):      
      return {
         "pid": property["id"],
         "monitors": property["type"],
         "read_link": {
            "href": "/objects/" + oid + "/properties/" + property["id"],
            "output": {
            "type": "object",
            "field": [{
               "name": "property",
               "schema": {
               "type": "string"
               }
            },
            {
               "name": "value",
               "schema": {
            #    "type": component.dictionary[property["id"]]["format"]
                  "type": "integer"
               }
            }]
         }
      },
   }     

   def AddEvent(self, property, oid):
      return {
         "eid": "get-" + property["id"],
         "monitors": property["type"],
         "output": {
            "type": "object",
            "field": [{
               "name": "observed-property",
               "schema": {
                  "type": "string"
               }
            },
            {
               "name": "value",
               "schema": {
                  # "type": component.dictionary[property["id"]]["format"]
                  "type": "integer"
               }
            }]
         },
      }   

   def AddValue(self, property, timestamp):      
      if property['format'] == 'float':
         value = float(property['value'])
      else:
         value = property['value']     
      
      return {
            "value": value,
            "timestamp": timestamp,
            "pid": property['id']
      }      

   def TearDown(self):               
      try: 
         if (self._mqttc):
            self._mqttc.unsubscribe(self._loraserver_topic)
         if (isinstance(self._active_timer, threading.Timer)):
            self._active_timer.cancel()
      except:         
         sys.exit('Error when closing TTN client')