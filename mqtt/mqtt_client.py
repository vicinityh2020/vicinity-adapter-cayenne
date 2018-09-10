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
import logging
import ttn_client
import loraserver_client


class MqttClient():
    def __init__(self):                        
        self._logger = logging.getLogger('VICINITY_LOG')    
        self._listener = None

        if os.environ.get('LORAWAN_APP_SERVER'):
            try:
                if (os.environ.get('LORAWAN_APP_SERVER') == "TTN"):                    
                    self._listener = ttn_client.TtnClient()                            
                elif (os.environ.get('LORAWAN_APP_SERVER') == "LoRaServer"):                      
                    self._listener = loraserver_client.LoRaServerClient()               
                else: 
                    self._listener = None                    
                    logging.error("Application server not found")                                                       
            except:                
                print("Unexpected error:", sys.exc_info()[0])                                
                sys.exit("Error on application server")
        else:
            logging.error("Application server not found - Please configure .env file")

    def TearDown(self):      
        # Tear down MQTT instances        
        if (self._listener):
            self._listener.TearDown()    
        
        
        