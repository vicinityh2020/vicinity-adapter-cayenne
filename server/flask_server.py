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
from flask import Flask, jsonify
import requests
# from functools import partial, update_wrapper
import threading
import json
import globals as globals
import pydash as py_
import logging

from thing_validation import ThingDescriptionValidation


objects =  {
  "adapter-id": globals.config['adapter_id'],
  "thing-descriptions": [],
  # "values": []  # Here we will keep the last observations gathered by each device, including value and timestamp
}

app = Flask(__name__)
import views

class FlaskServer():
  def __init__(self):     
    self._logger = logging.getLogger('VICINITY_LOG')   
    self._logger.info("Flask server instance") 
    self._validator = ThingDescriptionValidation()    

    self._queue_check = threading.Timer(1.0, self.ParseQueue)
    self._queue_check.start() 
    self._objects = []          
    
    app.run(host='0.0.0.0', port=int(globals.config['vicinity_adapter_port']))   
  
  def GetObjects(self):
    return self._objects 

  def ParseQueue(self):    
    if (not globals.queue.empty()):          
      while (not globals.queue.empty()):  
        item = globals.queue.get(block=False)                 
        # values_array = py_.pick(item, 'values')       

        hit = py_.find(objects["thing-descriptions"], {"oid": item["oid"]})        
        if (not hit):               
          self._logger.info("New item - " + item["oid"])                             
          objects["thing-descriptions"].append(item)  

          if globals.config['active_discovery']:
            self.ActiveDiscovery()
        else: # Update last measurements          
          # print(json.dumps(item, indent=2))
          hit['values'] = item['values']
          pass               

    # Restart timer
    self._queue_check = threading.Timer(1.0, self.ParseQueue)
    self._queue_check.start()      
  
  def ActiveDiscovery(self):
    self._logger.info("Active discovery - (" + str(len(objects['thing-descriptions'])) + ' nodes)')
         
    #Send request to agent     
    r = requests.post(globals.config['agent_endpoint'] + '/agent/objects', \
      data=json.dumps(py_.omit(objects, 'values')), \
      headers={"Content-Type": "application/json"})     

    # ToDo - Handle response (for potential errors)
    pass

  def TearDown(self):      
    if (isinstance(self._queue_check, threading.Timer)):
      self._queue_check.cancel()
