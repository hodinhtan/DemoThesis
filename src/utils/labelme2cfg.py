import argparse
import paho.mqtt.client as mqtt
import os.path
import json
import time
import base64

from utils.constants import *

class Labelme2TB:
    def __init__(self):
        self.genData = {}

    def checkConfigFile(self, cfg_file):
        try:
            with open(cfg_file, 'rt') as f:
                data = json.load(f)
                if(data): 
                    return data
                else:
                    return 0
        except Exception as e:
             print('[ERROR] Invalid JSON file')
             print(e)

    def doiToaDo(self, points, h ,w):
        return [points[0][0]/w, points[0][1]/h]

    def getLabelList(self, label, data, name, h, w):
        l = []
        i = 1
        for item in data:
            if item['label'] == label:
                if i<10: ii = '0'+str(i)
                else: str(i)
                n = name + label + ii
                toado = doiToaDo(item['points'], h ,w)
                x = {"name": n, "label":n, "xPos": toado[0], "yPos": toado[1], "type": label}
                l.append(x)
                i +=1
        return l

    def setJsonData(self, key, data):
        self.genData[key] = data

    def run(self, original, name):
        try:
            data = checkConfigFile(args)
            if not data: raise Exception 
                
            genData = {}
            genData['Tang'] = self.name
            n = self.name
            s = data['shapes']
            h = data['imageHeight']
            w = data['imageWidth']

            lBaoChay = getLabelList("BaoChay", s, n, h, w) 
            lBaoKhoi = getLabelList("BaoKhoi", s, n, h, w) 
            lPhunNuoc = getLabelList("PhunNuoc", s, n, h, w) 
            genData['BaoChay'] = lBaoChay
            genData['BaoKhoi'] = lBaoKhoi
            genData['PhunNuoc'] = lPhunNuoc

            print(genData)
            #with open(output + "/" + name +"_config.json", 'w') as f:
            #   json.dump(genData, f, indent=2)

        except Exception as e:
            print (e)
