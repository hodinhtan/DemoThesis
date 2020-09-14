import os
from utils import png2base64 as p2b64
from utils import png2config as p2cfg
from utils import labelme2tb as l2tb
from utils import constants as C

# danh sach cac widgets/cac tang
widgets = []
for filename in os.listdir(C.IMAGE_PATH):
    widgets.append(filename[:-4])
print (widgets)

# convert anh cac tang sang base64
print("Running convert image to base64")
res1 = p2b64.convert(C.IMAGE_PATH, "folder")

# thay doi anh trong file config_map, import truc tiep vao thingsboard
print("Running add base64 image data to config map")
for name, data in res1.items():
    res2 = p2cfg.convert(data, C.WIDGET_PATH + name + "_map.json")

# chuyen labelme json thanh file config attribute cho thingsboard
print("Running labelme to config file")
l2tb
