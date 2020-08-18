import json
import base64
import argparse


def convert(inpp):
    try:
        for  idx, file_name in enumerate(inpp):
            PRE = "data:image/png;base64,"
            with open(file_name , "rb") as f:
                idata = f.read()
                base64_data = PRE + base64.b64encode(idata).decode('utf-8')
    #            print(base64_data[0:20])

            with open(file_name[:-4] + ".base64", "w") as f:
                json.dump(base64_data,f,indent=2)
    except  Exception as err:
        print("something not right: ", err)
    finally :
        print("done!")

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description="Chuyen png sang base64 string")
    parser.add_argument("--input", required=True, help="input vao", nargs='+')
    args = parser.parse_args()

    if (args.input):
        IN = args.input
    convert(IN)
