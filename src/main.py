import os
from utils import png2base64 as p2b64
from utils import png2config as p2cfg
from utils import labelme2cfg as l2c
from utils import constants as C
import mqtt

# danh sach cac widgets/cac tang
#widgets = []
#for filename in os.listdir(C.IMAGE_PATH):
#    widgets.append(filename[:-4])
#print (widgets)
#
## convert anh cac tang sang base64
#print("Running convert image to base64")
#res1 = p2b64.convert(C.IMAGE_PATH, "folder")
#print ("result: ", res1)
#
## thay doi anh trong file config_map, import truc tiep vao thingsboard
#print("Running add base64 image data to config map")
#for name, data in res1.items():
#    res2 = p2cfg.convert(data, C.WIDGET_PATH + name + "_map.json")
#print ("result: ", res2)
#
# chuyen labelme json thanh file config attribute cho thingsboard
if 0:
    print("Running labelme to config file")
    nl = l2c.Labelme2TB()
    nl.run(C.IMAGE_PATH + "tang2.json", "tang2")
    nl.run(C.IMAGE_PATH + "tang3.json", "tang3")
    nl.run(C.IMAGE_PATH + "tang4.json", "tang4")
    nl.run(C.IMAGE_PATH + "tang5.json", "tang5")



if 1:
    m1 = mqtt.MQTT_CREATE()
    m1.run(f="tang2_config.json",token=C.TOKEN_TANG_2)
