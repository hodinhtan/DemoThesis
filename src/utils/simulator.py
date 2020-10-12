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

    def genDataNhietDo(self):
        a = {}
        normal = [] 
        for t in range(21,30,1):
          for i in range(100):
            normal.append(t)
        rare = [0,5,10,40,45,50]
        choices = normal + rare
        print ("------------------------------------- temp choices")
        print (choices)
        a['value'] = random.choice(choices)
        a['ts'] =  time.time()*100000
        return a
    def genDataDieuHoa(self):
        a = {}
        a['value'] = random.choice(["on", "off"])
        a['ts'] =  time.time()*100000
        return a
    def genDataBaoChay(self):
        a = {}
        normal = ["normal"] * 1000
        warning = ["warning"] * 5
        fire = ["fire"]
        choices = normal + warning + fire
        print ("------------------------------------- fire choices")
        print (choices)
        a['value'] = random.choice(choices)
        a['ts'] =  time.time()*100000
        return a
    def genDataBaoKhoi(self):
        a = {}
        normal = ["normal"] * 1000
        warning = ["warning"] * 5
        fire = ["smoke"]
        choices = normal + warning + fire
        print ("------------------------------------- smoke choices")
        print (choices)
        a['value'] = random.choice(choices)
        a['ts'] =  time.time()*100000
        return a
    
    def createDataTelemetry(self, json_data):
        print("create data")
        payload = {}
        #print (json_data)
        for idx, v in json_data.items():
            #print(idx, v)
            if idx in DEVICES:
                for y in v:
                    payload[y['label']] = []
                    a = {}
                    if idx == "BaoChay":
                        a = self.genDataBaoChay()
                    elif idx == "BaoKhoi":
                        a = self.genDataBaoKhoi()
                    elif idx == "NhietDo":    
                        a = self.genDataNhietDo()
                    elif idx == "DieuHoa":
                        a = self.genDataDieuHoa()
                    else: continue
                    payload[y['label']].append(a)
        return payload
        
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
