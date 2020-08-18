import argparse
import paho.mqtt.client as mqtt
import os.path
import json
import time
import base64
import imghdr

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

def doiToaDo(points, h ,w):
    return [points[0][0]/h, points[2][1]/w]

def getLabelList(label, data,name, h, w):
    l = []
    i = 1
    for item in data:
        if item['label'] == label:
            n = name+label+str(i)
            toado = doiToaDo(item['points'], h ,w)
            x = {"name": n, "label":n, "xPos": toado[0], "yPos": toado[1]}
            l.append(x)
            i +=1
    print(l)
    return l

if __name__ == "__main__":  
    parser = argparse.ArgumentParser(description="Demo IoT Thu vien")
    parser.add_argument("--file", required=True, help="Cai dat du lieu theo JSON format")
    parser.add_argument("--name", required=True, help="Thingsboard Server IP")
    parser.add_argument("--output", required=True, help="output")
    args = parser.parse_args()
    print("====================================================\n")
    print("\tConvert du lieu tu labelme sang su dung config thingsboard")
    print("\n====================================================")
    data = checkConfigFile(args)
    name = args.name
    output = args.output
        
    genData = {}
    if(data):
        genData['Tang'] = name
        genData['ToaNha'] = "ThuVienTaQuangBuu"
        lBaoChay = getLabelList("BaoChay", data['shapes'], name, data['imageHeight'], data['imageWidth']) 
        lBaoKhoi = getLabelList("BaoKhoi", data['shapes'], name, data['imageHeight'], data['imageWidth']) 
        lPhunNuoc = getLabelList("PhunNuoc", data['shapes'], name, data['imageHeight'], data['imageWidth']) 
        genData['BaoChay'] = lBaoChay
        genData['BaoKhoi'] = lBaoKhoi
        genData['PhunNuoc'] = lPhunNuoc

    print(genData)
    with open(output + "/" + name +"_config.json", 'w') as f:
       json.dump(genData, f, indent=2) 
