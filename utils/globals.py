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

from queue import LifoQueue

# Configuration parameters
config = {

  ## Endpoints
  #
  "gateway_api_endpoint": "http://localhost:8181",

  #
  "agent_endpoint": "http://localhost:9997",

  #
  # "neighbourhood_manager_endpoint": 'https://vicinity.bavenir.eu:3000'     # Production
  "neighbourhood_manager_endpoint": 'https://development.bavenir.eu:3000',    # Dev

  # 
  "vicinity_adapter_port": 9995,

  #
  "adapter_id": "adapter-cayenne",

  #
  "active_discovery": False,

  # Thing description validation flag: determines whether the validation process will be carried out or not
  "thing_description_validation": False,
}

### Global variables
# Queue that will be used as the communication channel between the MQTT client and the VICINITY adapter
queue = LifoQueue()
