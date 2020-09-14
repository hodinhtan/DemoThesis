import json
import base64

def convert(b64_img, map_cfg_file):
	with open(map_cfg_file, "rb") as f:
		data = json.load(f)

	data['mapImageUrl'] = b64_img

	with open(map_cfg_file, "w") as f:
		json.dump(data, f, indent=2)
