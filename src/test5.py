from utils import simulator
from utils.constants import *
from threading import Thread

s5 = simulator.Simulator('tang5', "tang5_config.json")

t5 = Thread(target=s5.run, args=(TOKEN_TANG_5,))

t5.start()

t5.join()
