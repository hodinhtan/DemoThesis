from utils import simulator
from utils.constants import *

s = simulator.Simulator('tang1', DEVICE_PATH + "tang1_config.json")

s.run(TOKEN_TANG_1)
