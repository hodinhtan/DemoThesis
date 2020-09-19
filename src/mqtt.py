import argparse
import paho.mqtt.client as mqtt
import os.path
import json
import time
import base64
import imghdr



THINGSBOARD_HOST = ''
MQTT_PORT = 1883
ACCESS_TOKEN = ''

gateway_topic = 'v1/devices/me/attributes'
node_topic = 'v1/gateway/attributes'
payload = {}
gateway_payload = {}


def on_connect(client, userdata, flags, rc):    
    if(rc == 0):
    	print('[INFO] Connected succesfully ...[OK]')
    	client.connected_flag = True
    else:
    	print('[ERROR] Connection Failed')
    	raise ValueError('Connection Problem')


def on_disconnect(client, userdata, rc):
	console.log('Disconnection : {}' .format(rc))

def connectThingsboard():
	client = mqtt.Client()
	client.username_pw_set(ACCESS_TOKEN)
	client.on_connect = on_connect
	client.connected_flag = False
	client.connect(THINGSBOARD_HOST, MQTT_PORT, 60)
	client.loop_start()
	return client


def checkConfigFile(args):
	try:
		with open(args.file, 'rt') as file:
			data = json.load(file)
			if(data): 
				return data
			else:
				return 0
	except Exception as e:
		print('[ERROR] Invalid JSON file')
		print(e)

def configDataParser(config):
	print("GOC", config)
	payload = {}
	try:
		for BaoChay in config['BaoChay']:
			payload[BaoChay['name']] = {
				'xPos' : BaoChay['xPos'],
				'yPos' : BaoChay['yPos'],
				'entityLabel' : BaoChay['label'],
				'deviceType' : 'baochay'
			}
		for BaoKhoi in config['BaoKhoi']:
			payload[BaoKhoi['name']] = {
				'xPos' : BaoKhoi['xPos'],
				'yPos' : BaoKhoi['yPos'],
				'entityLabel' : BaoKhoi['label'],
				'deviceType' : 'baokhoi'
			}
		for PhunNuoc in config['PhunNuoc']:
			payload[PhunNuoc['name']] = {
				'xPos' : PhunNuoc['xPos'],
				'yPos' : PhunNuoc['yPos'],
				'entityLabel' : PhunNuoc['label'],
				'deviceType' : 'phunnuoc'
			}
		for DieuHoa in config['DieuHoa']:
			payload[DieuHoa['name']] = {
				'xPos' : DieuHoa['xPos'],
				'yPos' : DieuHoa['yPos'],
				'entityLabel' : DieuHoa['label'],
				'deviceType' : 'dieuhoa'
			}
		for NhietDo in config['NhietDo']:
			payload[NhietDo['name']] = {
				'xPos' : NhietDo['xPos'],
				'yPos' : NhietDo['yPos'],
				'entityLabel' : NhietDo['label'],
				'deviceType' : 'nhietdo'
			}
		for Camera in config['Camera']:
			payload[Camera['name']] = {
				'xPos' : Camera['xPos'],
				'yPos' : Camera['yPos'],
				'entityLabel' : Camera['label'],
				'deviceType' : 'camera'
			}
	except Exception as e:
		print('[ERROR] Parsing Error')
		print(e)
	gateway_payload['ToaNha'] = config['ToaNha']
	print(payload)
	return payload, gateway_payload



def sendPayload(client, topic, payload):
	try:
		ret, cnt = client.publish(topic, json.dumps(payload), 1)
		if(ret != 0):
			print('[ERROR] message cant be able to sent')
			print('[INFO] Resending ....')
			time.sleep(1)
			ret, cnt = sendPayload(client, gateway_topic, gateway_payload)
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

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Demo IoT Thu vien")
	parser.add_argument("--file", required=True, help="Cai dat du lieu theo JSON format")
	parser.add_argument("--host", required=True, help="Thingsboard Server IP")
	parser.add_argument("--token", required=True, help="Thingsboard Access Token")
	args = parser.parse_args()
	print("====================================================\n")
	print("\tTao cac device thong qua gateway")
	print("\n====================================================")
	ret = checkConfigFile(args)
	if(args.host):
		THINGSBOARD_HOST = args.host
	if(args.token):
		ACCESS_TOKEN = args.token
	if(ret):
		nodes_payload, gateway_payload = configDataParser(ret)
		client = connectThingsboard()
		while not client.connected_flag:
			print('[INFO] Connecting ...')
			time.sleep(1)
		try:
			ret = sendPayload(client, gateway_topic, gateway_payload)
			if(ret):
				print('[INFO] Message send ...[OK]', gateway_topic, json.dumps(gateway_payload))
				ret = sendPayload(client, node_topic, nodes_payload)
				if(ret):
					print('[INFO] setup ...[OK]', node_topic, json.dumps(nodes_payload))
			print('[INFO] program exiting ...')
			client.loop_stop()
			client.disconnect()
		except KeyboardInterrupt:
			client.loop_stop()
			client.disconnect()

	else:
		print('[ERROR] Error Parsing JSON file')
