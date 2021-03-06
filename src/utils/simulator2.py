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
        #print (self.json_data)
        self.payload = self.createDataTelemetry(self.json_data)
        self.TEMP_CHOICE = [0,5,10,20,21,22,23,23,24,24,24,25,27,26,28,30,40,50,60,80,100]

        with open('utils/group.json') as f:
            self.group = json.load(f)

    def tbInstantce(self, token):
        print("create tb instance")
        try:
            client = mqtt.Client(self.tb_name)
            client.username_pw_set(token)
            client.connect(THINGSBOARD_HOST, MQTT_PORT, 60)
            client.loop_start()
            return client
        except Exception as e:
            print('[ERROR] : {}' .format(e))

    def genDataCamera(self,idx):
        self.payload[idx] = "https://www.youtube.com/watch?v=qo65StoT9XQ&ab_channel=Th%C6%B0vi%E1%BB%87nT%E1%BA%A1QuangB%E1%BB%ADu-%C4%90HB%C3%A1chkhoaH%C3%A0N%E1%BB%99i"

    def genDataNhietDo(self, k, v):
        a = {}
        a['value'] = random.choice(self.TEMP_CHOICE)
        a['ts'] =  time.time()
        self.payload[k].append(a)
        if a['value'] < 25:
           #turn off dieuhoa, 
           adh = {}
           adh['value'] = "off"
           adh['ts'] =  time.time()
           #baochay normal
           abc = {}
           abc['value'] = "normal"
           abc['ts'] =  time.time()
            
        if a['value'] > 30 and a['value'] <= 40:
           #turn on dieuhoa, 
           adh = {}
           adh['value'] = "on"
           adh['ts'] =  time.time()
           #baochay normal
           abc = {}
           abc['value'] = "normal"
           abc['ts'] =  time.time()

        if a['value'] > 40 and a['value'] <= 60:
           #turn on dieuhoa, 
           adh = {}
           adh['value'] = "on"
           adh['ts'] =  time.time()
           #baochay normal
           abc = {}
           abc['value'] = "warning"
           abc['ts'] =  time.time()

        if a['value'] > 60:
           #turn on dieuhoa, 
           adh = {}
           adh['value'] = "on"
           adh['ts'] =  time.time()
           #baochay normal
           abc = {}
           abc['value'] = "critical"
           abc['ts'] =  time.time()

        return tangxNhietDoy
    
    def createDataTelemetry(self):
        for idx, v in self.group.items():
            if ('NhietDo' in idx):
                self.payload[idx] = []
                self.genDataNhietDo(idx, v)
            elif ('Camera' in idx):
                self.payload[idx] = []
                self.genDataCamera(idx)
                
        
    def parseFile(self, fd):
        print("parse file: ", fd)
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
        else:
            raise ValueError('Telemetry Send')

    def run(self, token):
        client = self.tbInstantce(token)
        try:
            while True:
                self.sendTelemetry(client, self.gw_telemetry, self.payload)
                time.sleep(INTERVAL_TIME)
                self.payload = self.createDataTelemetry(self.json_data)
                print(self.payload)
        except KeyboardInterrupt as e:
            print('[INFO] program exiting ...')
            client.loop_stop()
            client.disconnect()
