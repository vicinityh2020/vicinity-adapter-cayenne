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
import time, datetime, pytz
from queue import Queue
import paho.mqtt.client as mqtt
import threading
import logging
import json

from thing_validation import ThingDescriptionValidation
import components_dictionary as component
import cayenne_parser
import globals as globals

class TtnClient (threading.Thread):
   
   def __init__(self):      
      
      self._logger = logging.getLogger('VICINITY_LOG')    
      self._cayenne =   cayenne_parser.CayenneParser()   
      self._validator = ThingDescriptionValidation()

      self._active_timer = {}      
      self._thread = threading.Thread(target=self.Start, name="Ttn_thread")
      self._ttn_topic = '+/devices/+/up'
      self._thread.daemon = True
      self._thread.start()    

   def Start(self):
      self._logger.info("TTN client thread instanced")        
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
         self._logger.info("Connected to MQTT Broker - " + os.environ.get('LORAWAN_MQTT_URL'))
      else:
         self._logger.error("Connection error to MQTT Broker - " + os.environ.get('LORAWAN_MQTT_URL'))

      # subscribe for all devices of user
      mqttc.subscribe(self._ttn_topic)    

   def on_message (self, mqttc,obj,msg):       
      raw = json.loads(msg.payload.decode())    
      if (raw != None):          
            self.ParsePayload (raw)

   def on_publish(self, mosq, obj, mid):      
      self._logger.info("mid: " + str(mid))          

   def on_subscribe(self, mosq, obj, mid, granted_qos):      
      self._logger.info("Subscribed to topic " + self._ttn_topic)          


   def on_unsubscribe(self, client, userdata, mid):      
      self._logger.info("UnSubscribed: " + str(client) + " " + str(granted_qos))                  

   def on_log(self, mqttc,obj,level,buf):
      self._logger.info("message:" + str(buf))          
      self._logger.info("userdata:" + str(obj))     

   def ParsePayload(self,payload):
      data = {
            "name": payload["dev_id"],
            "oid": payload["hardware_serial"],            
            "type": "core:Device",
            "properties": [],
            "actions": [],
            "events": [],
            # Internal array to handle the last observations coming from the sensors
            "values": []
      }    

      # Parse the payload field 
      properties = self._cayenne.decodeCayenneLpp(payload['payload_raw'], str(payload['metadata']['time']))           
      for i in properties:         
         if "type" in i:
            data["properties"].append(self.AddProperty(i, data["oid"]))  
            data["events"].append(self.AddEvent(i, data["oid"]))   
            data["values"].append(self.AddValue(i, payload['metadata']['time']))      

      self._logger.debug("Message received - " + data['oid'])   
      self._validator.validate(data)  
      globals.queue.put(data)

   def AddProperty(self, property, oid):
      return {
         "pid": property["id"],
         "monitors": property["type"],
         "read_link": {
            "href": "/device/" + oid + "/property/" + property["id"],
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
            self._mqttc.unsubscribe(self._ttn_topic)
         if (isinstance(self._active_timer, threading.Timer)):
            self._active_timer.cancel()
      except:         
         sys.exit("Error on closing TTN client")