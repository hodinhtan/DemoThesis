"""
@filename : sensors simulator
@author : Tan	Ho
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
from constants import *

DEBUG_MODE = False
choice = {
    "baochay":    ["normal", "high temp", "fire"],
    "baokhoi": ["normal", "high temp", "smoke"],
    "phunnuoc": ["on", "off"]
}

THINGSBOARD_HOST = ''
MQTT_PORT = 1883
ACCESS_TOKEN = ''
Topic = 'v1/gateway/telemetry'
INTERVAL = 60
next_reading = time.time()
payload = {}


def simulateSlotValue():
	return random.choice(choice)


def populateValues():
	parking_lot = {}
	for x in range(simulate_slots):
		name = 'tang1BaoChay' + f'{x+1:02d}'
		parking_lot[name] = simulateSlotValue()
	return parking_lot 


def msgAssembler(obj):
	payload = {}
	for key, value in obj.items():
		payload[key] = []
		msg = {
			'ts' : 0,
			'values' : {}
		}
		msg['ts'] = round(time.time() * 1000)
		msg['values']['status'] = value
		payload[key].append(msg)
	return payload

def on_connect(client, userdata, flags, rc):    
    if(rc == 0):
    	print('[INFO] Connected succesfully')
    	client.connected_flag = True
    else:
    	print('[ERROR] Connection Failed')
    	raise ValueError('Connection Problem')

def on_disconnect(client, userdata, rc):
	print('[INFO] Disconnection : {}' .format(rc))


def connectThingsboard():
	try:
		client = mqtt.Client('Simulator')
		client.connected_flag = False
		client.on_connect = on_connect
		client.username_pw_set(ACCESS_TOKEN)
		client.connect(THINGSBOARD_HOST, MQTT_PORT, 60)
		client.loop_start()
		return client
	except Exception as e:
		print('[ERROR] : {}' .format(e))

	
def parseFile(fd):
	with open(fd, 'rt') as file:
		data = json.load(file)
		if(data): 
			return data
		else:
			return 0

def sendTelemetry(client, topic, payload):
	ret = client.publish(topic, json.dumps(payload), 1)
	if (ret[0] == 0):
		print('{} Telemetry sent ...[OK]' .format(datetime.now().strftime("%d/%m/%Y, %H:%M:%S")))
		time.sleep(0.5)
		if (DEBUG_MODE):
			print(payload)
	else:
		raise ValueError('Telemetry Send')

if __name__ == "__main__":
	client = connectThingsboard()
	if(args.file):
		ret = parseFile(args.file)
		ret = msgAssembler(ret)
	else:
		ret = populateValues()
		ret = msgAssembler(ret)
	while not client.connected_flag:
		print('[INFO] Connecting ...')
		time.sleep(1)
	try:
		while True:
			ret = populateValues()
			ret = msgAssembler(ret)
			sendTelemetry(client, Topic, ret)
			next_reading += INTERVAL
			sleep_time = next_reading - time.time()
			if sleep_time > 0:
				time.sleep(sleep_time) 
	except KeyboardInterrupt as e:
		print('[INFO] program exiting ...')
		client.loop_stop()
		client.disconnect()
