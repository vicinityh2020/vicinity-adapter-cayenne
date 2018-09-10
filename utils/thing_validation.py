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

import os
import json
import requests
import logging
import globals as globals
import requests
from flask import jsonify

# Validate that the objects stored are compliant with the TD data models
# The function will return the output of the validator service
# NOTE: To successfully run this test, the adapter must be running
class ThingDescriptionValidation():
  def __init__ (self):
    self._logger = logging.getLogger('VICINITY_LOG')  
    self._logger.info("Validator instanced")      

  
  # Depending on whether the validation flag is enabled or not, the method will return an object with the output of the remote operation
  # NOTE: If the flag is set to false, the output of the operation will be equivalent to a successful validation
  def validate(self, thing_description):
        
    if globals.config['thing_description_validation']:
      r = requests.post(globals.config['neighbourhood_manager_endpoint'] + '/api/repository/validate', \
       data=json.dumps(thing_description), \
       headers={"Content-Type": "application/json"})        
      res = json.loads(r.text)         
      
      if ((res['status'] == 'success') and (res['data']['message'] == 'Thing is valid')):      
        return {"success": True}
      else:
        return {
          "success": False, 
          "error": res['data']['errors']
        }
    else:
      return {"success": True}


    
      
      