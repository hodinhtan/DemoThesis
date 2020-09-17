from utils import simulator
from utils.constants import *
from threading import Thread

s1 = simulator.Simulator('tang1', "tang1_config.json")
s2 = simulator.Simulator('tang2', "tang2_config.json")
s3 = simulator.Simulator('tang3', "tang3_config.json")
s4 = simulator.Simulator('tang4', "tang4_config.json")
s5 = simulator.Simulator('tang5', "tang5_config.json")

t1 = Thread(target=s1.run, args=(TOKEN_TANG_1,))
t2 = Thread(target=s2.run, args=(TOKEN_TANG_2,))
t3 = Thread(target=s3.run, args=(TOKEN_TANG_3,))
t4 = Thread(target=s4.run, args=(TOKEN_TANG_4,))
t5 = Thread(target=s5.run, args=(TOKEN_TANG_5,))

t1.start()
t2.start()
t3.start()
t4.start()
t5.start()

t1.join()
t2.join()
t3.join()
t4.join()
t5.join()
