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
        p = points
 #       xmin = min(p[0][0],p[1][0],p[2][0],p[3][0])
 #       ymin = min(p[0][1],p[1][1],p[2][1],p[3][1])
 #       xmin = min(p[0][0],p[1][0],p[2][0],p[3][0])
 #       xmin = min(p[0][0],p[1][0],p[2][0],p[3][0])
 #       xmin = min(p[0][0],p[1][0],p[2][0],p[3][0])
        return [p[0][0]/w, p[0][1]/h]

    def getLabelList(self, label, data, name, h, w):
        print(label, data, name, h,w)
        l = []
        i = 1
        for item in data:
            if item['label'] == label:
                n = name + label + str(i)
                toado = self.doiToaDo(item['points'], h ,w)
                x = {"name": n, "label":n, "xPos": toado[0], "yPos": toado[1], "type": label}
                l.append(x)
                i +=1
        return l

    def run(self, cfg_file, name):
        try:
            data = self.checkConfigFile(cfg_file)
          #  print(data)
            if not data: raise Exception 
                
            genData = {}
            genData['Tang'] = name
            genData['ToaNha'] = "TVTQB"
            n = name
            s = data['shapes']
            h = data['imageHeight']
            w = data['imageWidth']

            lBaoChay = self.getLabelList("BaoChay", s, n, h, w) 
            lBaoKhoi = self.getLabelList("BaoKhoi", s, n, h, w) 
            lPhunNuoc = self.getLabelList("PhunNuoc", s, n, h, w) 
            lNhietDo = self.getLabelList("NhietDo", s, n, h, w) 
            lCamera = self.getLabelList("Camera", s, n, h, w) 
            lDieuHoa = self.getLabelList("DieuHoa", s, n, h, w) 
            genData['BaoChay'] = lBaoChay
            genData['BaoKhoi'] = lBaoKhoi
            genData['PhunNuoc'] = lPhunNuoc
            genData['NhietDo'] = lNhietDo
            genData['Camera'] = lCamera
            genData['DieuHoa'] = lDieuHoa

            print(genData)
            with open(name +"_config.json", 'w') as f:
               json.dump(genData, f, indent=2)
            return genData
        except Exception as e:
            print (e)
