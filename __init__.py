# -*- coding: utf-8 -*-
import os
from subprocess import Popen, PIPE, call

from modules import cbpi, socketio
from modules.core.hardware import SensorActive
import json
from flask import Blueprint, render_template, jsonify, request
from modules.core.props import Property

blueprint = Blueprint('brewbubbles', __name__)
cache = {}


def log(s):
    s = "cbpi_brewbubbles: " + s
    cbpi.app.logger.info(s)


@cbpi.sensor
class brewBubbles(SensorActive):
    log("cbpi_brewbubbles Start Instancing")
    key = Property.Text(label="BrewBubbles Name", configurable=True,
                        description="Enter the name of your BrewBubbles")
    sensorType = Property.Select("Data Type", options=["BPM", "Room Temp.",
                                 "Vessel Temp."], description="Select which type of data to register for this sensor")

    log("cbpi_brewbubbles continue Instancing")
    def get_unit(self):
        if self.sensorType == "Temperature":
            if self.get_config_parameter("unit", "C") == "C":
                return "°C"
            else:
                return "°F"
        else:
            return " "

    def stop(self):
        pass

    def execute(self):
        global cache
        while self.is_running():
            try:
                if cache[self.key] is not None:
                    reading = cache[self.key][self.sensorType]
                    self.data_received(reading)
            except:
                pass
            self.api.socketio.sleep(1)


@blueprint.route('/api/brewbubbles/v1/data', methods=['POST'])
def set_temp():
    global cache
    '''{
        "api_key":"Brew Bubbles",
        "device_source":"Brew Bubbles",
        "name":"Fermenter 1",
        "bpm":3.2,
        "ambient":65.3,
        "temp":65.525,
        "temp_unit":"F",
        "datetime":"2019-12-15T21:48:07Z"
    }
    '''
    log("cbpi_brewbubbles Start Parsing")
    data = request.get_json()
    log(str(data))
    id = data["name"]
    bpm = data["bpm"]
    room_temp = data["ambient"]
    vessel_temp = data["temp"]
    log("BrewBubbles %s BPM %s Room T %s Vessel T %s" % (
                                            id, bpm, room_temp, vessel_temp))
    cache[id] = {'BPM': bpm, 'Room T': room_temp, 'Vessel T': vessel_temp}

    return ('', 204)


@cbpi.initalizer()
def init(cbpi):
    print "INITIALIZE BrewBubbles MODULE"
    cbpi.app.register_blueprint(blueprint)
