import sys
import os
import time
sys.path.append(os.path.abspath(__file__ + '/../../../../'))

from homepi.device.core.roku import Roku
from homepi.device.core.roku import Key


r = Roku('192.168.1.4')
r.initialize()
print(r.get_apps())
r.load_apps()
print(r.apps_dict)
print(r.get_device_info())

r.wake()
r.do_keypress(Key.POWER_ON)