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

from flask_server import app, objects
from flask import jsonify, abort, request
import datetime
import pydash as py_
import json


BASE_URL = '/adapter'
ADAPTER_ID = 'adapter-cayenne'

# Server routing
@app.route(BASE_URL + '/objects', methods=['GET'])
def get_objects():       
  temp = py_.map_(objects['thing-descriptions'], lambda x: py_.omit(x, 'values'))
  return jsonify({
    'adapter-id': objects['adapter-id'],
    'thing-descriptions': temp
  })      

@app.route(BASE_URL + '/objects/<string:oid>/properties/<string:pid>', methods=['GET'])
def get_object_from_id(oid, pid):      
  hit_oid = py_.find(objects['thing-descriptions'], {'oid': oid})
  if hit_oid:
    hit_values = py_.find(hit_oid['values'], {'pid': pid})
    return jsonify(py_.omit(hit_values,'pid'))
  else:
    content = {'please move along': 'nothing to see here'}
    abort(404)

@app.route(BASE_URL + '/device/<string:oid>/property/<string:pid>', methods=['GET'])
def get_device_from_id(oid, pid):      
  hit_oid = py_.find(objects['thing-descriptions'], {'oid': oid})
  if hit_oid:
    hit_values = py_.find(hit_oid['values'], {'pid': pid})
    return jsonify(py_.omit(hit_values,'pid'))
  else:
    content = {'please move along': 'nothing to see here'}
    abort(404)
    
# NOTE: To make this work, the HTTP header must contain the "Content-Type" field set to "application/json"
@app.route(BASE_URL + '/objects/<string:oid>/properties/<string:pid>', methods=['PUT'])
def update_object_property(oid, pid):        

  body = request.json
  hit_oid = py_.find(objects['thing-descriptions'], {'oid': oid})
  if hit_oid:
    hit_values = py_.find(hit_oid['values'], {'pid': pid})
    hit_values['value'] = body['value']
    hit_values['timestamp'] = datetime.datetime.now().isoformat()     
    return jsonify(py_.omit(hit_values,'pid'))
  else:
    content = {'please move along': 'nothing to see here'}
    abort(404)
  

