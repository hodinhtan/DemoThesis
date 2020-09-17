#!/usr/bin/env python3
import argparse
import paho.mqtt.client as mqtt
import os.path
import json
import time
import base64
import imghdr
from utils import constants as C

class MQTT_CREATE():
    def __init__(self):
        self.gateway_topic = 'v1/devices/me/attributes'
        self.node_topic = 'v1/gateway/attributes'
        self.payload = {}
        self.gateway_payload = {}

    def on_connect(client, userdata, flags, rc):    
        if(rc == 0):
            print('[INFO] Connected succesfully ...[OK]')
            client.connected_flag = True
        else:
            print('[ERROR] Connection Failed')
            raise ValueError('Connection Problem')


    def on_disconnect(client, userdata, rc):
        console.log('Disconnection : {}' .format(rc))

    def connectThingsboard(self, THINGSBOARD_HOST, token):
        client = mqtt.Client()
        client.username_pw_set(token)
        client.on_connect = self.on_connect
        client.connected_flag = False
        client.connect(THINGSBOARD_HOST, C.MQTT_PORT, 60)
        client.loop_start()
        return client


    def checkConfigFile(self, f):
        try:
            with open(f, 'rt') as file:
                data = json.load(file)
                if(data): 
                    return data
                else:
                    return 0
        except Exception as e:
            print('[ERROR] Invalid JSON file')
            print(e)

    def configDataParser(self, config):
        print(config)
        self.payload = {}
        try:
            for BaoChay in config['BaoChay']:
                self.payload[BaoChay['name']] = {
                    'xPos' : BaoChay['xPos'],
                    'yPos' : BaoChay['xPos'],
                    'entityLabel' : BaoChay['label'],
                    'deviceType' : 'baochay'
                }
            for BaoKhoi in config['BaoKhoi']:
                self.payload[BaoKhoi['name']] = {
                    'xPos' : BaoKhoi['xPos'],
                    'yPos' : BaoKhoi['yPos'],
                    'entityLabel' : BaoKhoi['label'],
                    'deviceType' : 'baokhoi'
                }
            for PhunNuoc in config['PhunNuoc']:
                self.payload[PhunNuoc['name']] = {
                    'xPos' : PhunNuoc['xPos'],
                    'yPos' : PhunNuoc['yPos'],
                    'entityLabel' : PhunNuoc['label'],
                    'deviceType' : 'phunnuoc'
                }
            for Camera in config['Camera']:
                self.payload[Camera['name']] = {
                    'xPos' : Camera['xPos'],
                    'yPos' : Camera['yPos'],
                    'entityLabel' : Camera['label'],
                    'deviceType' : 'camera'
                }
            for DieuHoa in config['DieuHoa']:
                self.payload[DieuHoa['name']] = {
                    'xPos' : DieuHoa['xPos'],
                    'yPos' : DieuHoa['yPos'],
                    'entityLabel' : DieuHoa['label'],
                    'deviceType' : 'dieuhoa'
                }
            for NhietDo in config['NhietDo']:
                self.payload[NhietDo['name']] = {
                    'xPos' : NhietDo['xPos'],
                    'yPos' : NhietDo['yPos'],
                    'entityLabel' : NhietDo['label'],
                    'deviceType' : 'nhietdo'
                }
        except Exception as e:
            print('[ERROR] Parsing Error')
            print(e)
        self.gateway_payload['ToaNha'] = config['ToaNha']
        return self.payload, self.gateway_payload



    def sendPayload(self, client, topic, payload):
        try:
            ret, cnt = client.publish(topic, json.dumps(payload), 1)
            if(ret != 0):
                print('[ERROR] message cant be able to sent')
                print('[INFO] Resending ....')
                time.sleep(1)
                ret, cnt = sendPayload(client, self.gateway_topic, gateway_payload)
                if (ret != 0):
                    print('[ERROR] sending again failed')
                    return False
                else:
                    return True
            else:
                return True
        except Exception as e:
            print('[ERROR] sending message')
            print(e)

    def run(self, f="", host="localhost", token=""):
        print (f, host, token)
        ret = self.checkConfigFile(f)
        if(host):
            THINGSBOARD_HOST = host
        if(token):
            ACCESS_TOKEN = token
        if(ret):
            nodes_payload, gateway_payload = self.configDataParser(ret)
            client = self.connectThingsboard(THINGSBOARD_HOST, ACCESS_TOKEN)
            while not client.connected_flag:
                print('[INFO] Connecting ...')
                time.sleep(1)
            try:
                ret = self.sendPayload(client, gateway_topic, gateway_payload)
                if(ret):
                    print('[INFO] Message send ...[OK]', gateway_topic, json.dumps(gateway_payload))
                    ret = self.sendPayload(client, self.node_topic, nodes_payload)
                    if(ret):
                        print('[INFO] setup ...[OK]', self.node_topic, json.dumps(nodes_payload))
                print('[INFO] program exiting ...')
                client.loop_stop()
                client.disconnect()
            except KeyboardInterrupt:
                client.loop_stop()
                client.disconnect()

        else:
            print('[ERROR] Error Parsing JSON file')
