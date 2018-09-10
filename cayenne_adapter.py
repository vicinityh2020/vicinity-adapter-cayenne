#!/usr/bin/python3

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
import sys
sys.path.append('mqtt/')
sys.path.append('utils/')
sys.path.append('server/')

from os.path import join, dirname
from dotenv import load_dotenv

import json
import threading
import logging

from mqtt_client import MqttClient 
from flask_server import FlaskServer

LOGLEVEL = logging.DEBUG       # DEBUG, INFO, WARNING, ERROR, CRITICAL
BASE_URL = '/adapter'


def endProgram(status):   
   logging.debug("Program finished")
   sys.exit(status)

if __name__ == '__main__':
  try:       
    logging.basicConfig(
      filemode="a",
      format="%(asctime)s [%(levelname)s] [%(threadName)s] %(message)s",
      datefmt="%Y-%m-%d %H:%M:%S",
      level=LOGLEVEL
    )       

    # Check whether .env file exists (otherwise, we will assume that they will be already set)
    if (os.path.exists('.env')):
      logging.debug('.env file found - loading...')
      load_dotenv(join(dirname(__file__), '.env')) 

    if (os.environ.get('LORAWAN_APP_SERVER') ):               
      mqtt = MqttClient()    
      flask = FlaskServer()          
    else:
      logging.error('Needed environment variables not found - closing')  
    
  except KeyboardInterrupt:      
    try:
      logging.info("CTRL + C pressed")
      # flask.TearDown()
    except:
      logging.error("ERROR")

  endProgram(0)

  

