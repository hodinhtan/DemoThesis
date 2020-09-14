import json
import base64
import argparse
import os

from utils.constants import *

MODE = ["folder", "file"]

def convert(inf, mode):
	if mode == MODE[0]:
		b64s = {}
		try:
			for file_name in os.listdir(inf):
				pre = "data:image/png;base64,"
				with open(inf + file_name , "rb") as f:
					idata = f.read()
					base64_data = pre + base64.b64encode(idata).decode('utf-8')
					b64s[file_name[:-4]] = base64_data

				with open(B64_PATH + file_name[:-4] + ".base64", "w") as f:
					json.dump(base64_data,f,indent=2)
			return b64s
		except  exception as err:
			print("convert error ", err)
	elif mode == MODE[1]:
		try:
			pre = "data:image/png;base64,"
			with open(inf + file_name , "rb") as f:
				idata = f.read()
				base64_data = pre + base64.b64encode(idata).decode('utf-8')

			with open(B64_PATH + file_name[:-4] + ".base64", "w") as f:
				json.dump(base64_data,f,indent=2)
			
			return base64_data
		except  exception as err:
			print("convert error ", err)
