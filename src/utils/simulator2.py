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
        tangxNhietDoy = {}
        tangxNhietDoy['value'] = random.choice([10,20,21,22,23,23,24,24,24,25,27,26,28,30,40, 60])
        tangxNhietDoy['ts'] =  time.time()*100000
        if tangxNhietDoy['value'] > 30 and tangxNhietDoy['value'] > 40:
           pre = tangxNhietDoy[:4]
           num = tangxNhietDoy[-1]
           # bat dieu hoa 
           dh = pre +"DieuHoa"+num

        if tangxNhietDoy['value'] > 30 and tangxNhietDoy['value'] > 40:
            #bat dieu hoa
            #
        return tangxNhietDoy
    def genDataBaoChay(self):
        a = {}
        a['value'] = random.choice(["normal", "warning", "fire"])
        a['ts'] =  time.time()*100000
        return a
    def genDataBaoKhoi(self):
        a = {}
        a['value'] = random.choice(["normal", "warning", "smoke"])
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
