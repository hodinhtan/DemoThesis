import json
import base64

for i in range(5):
    TANG = "tang" + str(i+1)
    PRE = "data:image/png;base64,"
    data = {}
    with open(TANG + ".png", "rb") as f:
        idata = f.read()
        base64_data = PRE + base64.b64encode(idata).decode('utf-8')
        print(base64_data[0:20])

    with open("../map.json", "rb") as f:
        data = json.load(f)

    data['mapImageUrl'] = base64_data
    with open(TANG + "_map.json", "w") as f:
        json.dump(data,f,indent=2)

