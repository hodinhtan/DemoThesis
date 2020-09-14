"""
@filename : sensors simulator
@author : TanHo
@date : 29 August 2020
@organization : hust.edu.vn
@version : v1.0
@description : Sensors simulation.
"""

import argparse
import paho.mqtt.client as mqtt
import json
import time
import random
from datetime import datetime
from utils.constants import *

class Simulator():
    def __init__(self, tb_name, json_file):
        self.gw_telemetry = 'v1/gateway/telemetry'
        self.tb_name = tb_name
        self.json_data = self.parseFile(json_file)
        self.payload = self.createData(self.json_data)

    def tbInstantce(self, token):
        try:
            client = mqtt.Client()
            client.connected_flag = False
            client.username_pw_set(token)
            client.connect(THINGSBOARD_HOST, MQTT_PORT, 60)
            client.loop_start()
            return client
        except Exception as e:
            print('[ERROR] : {}' .format(e))

        
    def createData(self, json_data):
        payload = {}
        for v in json_data.values():
            if v in DEVICES:
               x = json_data[v]
               for y in x:
                   payload[y['label']] = random.choice([ 10, 20, 24, 26, 28 ,30 ,40])
        return payload
        
    def parseFile(self, fd):
        with open(fd, 'rt') as file:
            data = json.load(file)
            if(data): 
                return data
            else:
                return 0

    def sendTelemetry(self, client, topic, payload):
        ret = client.publish(topic, json.dumps(payload), 1)
        if (ret[0] == 0):
            print('{} Telemetry sent ...[OK]' .format(datetime.now().strftime("%d/%m/%Y, %H:%M:%S")))
            time.sleep(0.5)
            if (DEBUG_MODE):
                print(payload)
        else:
            raise ValueError('Telemetry Send')

    def run(self, token):
        client = self.tbInstantce(token)
        print(self.payload)
        while not client.connected_flag:
            print('[INFO] Connecting ...')
            time.sleep(1)
        try:
            while True:
                self.sendTelemetry(self, client, self.gw_telemetry, self.payload)
                time.sleep(INTERVAL_TIME)
        except KeyboardInterrupt as e:
            print('[INFO] program exiting ...')
            client.loop_stop()
            client.disconnect()
