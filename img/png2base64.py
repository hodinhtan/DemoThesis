import json
import base64
for i in range(5):
    TANG = "tang" + str(i+1)
    PRE = "data:image/png;base64,"
    with open(TANG + ".png", "rb") as f:
        idata = f.read()
        base64_data = PRE + base64.b64encode(idata).decode('utf-8')
        print(base64_data[0:20])

    with open(TANG + ".base64", "w") as f:
        json.dump(base64_data,f,indent=2)

