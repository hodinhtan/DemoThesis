import json
import base64

with open("tang1.json", "r") as f:
    data = json.load(f)

TANG = "tang5"
print (data.keys())
print (data['imagePath'])
print(data['imageData'][:3])
data['imagePath'] = TANG + ".png"

with open(TANG + ".png", "rb") as f:
    idata = f.read()
    base64_data = base64.b64encode(idata).decode('utf-8') 
    print(base64_data[0:10])
data['imageData'] = ""
data['imageData'] = str(base64_data)

import cv2
img = cv2.imread(TANG+ ".png")
print(img.shape)
data['imageHeight'] = img.shape[0]
data['imageWidth'] = img.shape[1]
a_file = open(TANG+ ".json", "w")
json.dump(data, a_file, indent=2)
a_file.close()
