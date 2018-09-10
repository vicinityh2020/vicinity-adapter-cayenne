#! /usr/bin/python3

#################################################################
#   Copyright (C) 2018  
#   This program and the accompanying materials are made
#   available under the terms of the Eclipse Public License 2.0
#   which is available at https://www.eclipse.org/legal/epl-2.0/ 
#   SPDX-License-Identifier: EPL-2.0
#   Contributors: ATOS SPAIN S.A.
################################################################# 

import sys
sys.path.append("../utils/")
sys.path.append("../server/")
import unittest
import base64
import pydash as py_
import json
import requests
import globals as globals

import thing_validation
from flask_server import objects

class TestThingDescription(unittest.TestCase):
  def test_Objects (self):    
    #Get all objects from adapter
    r = requests.get('http://localhost:' + str(globals.config['vicinity_adapter_port']) + '/adapter/objects', \
     headers={"Content-Type": "application/json"})        
    objects = json.loads(r.text)    

    #Validate TDs
    r = requests.post(globals.config['neighbourhood_manager_endpoint'] + '/api/repository/validate', \
      data=json.dumps(objects), \
      headers={"Content-Type": "application/json"})        
    output = json.loads(r.text)    
    print(json.dumps(output, indent=2))            
    map = py_.map_(output['data'], lambda x: py_.has(x, 'errors'))
    self.assertTrue(False in map, 'Some error(s) have been triggered during the validation process')

    

if __name__ == '__main__':
    unittest.main()