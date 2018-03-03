import sys
import os
sys.path.append(os.path.abspath(__file__ + '/../../../../'))

from homepi.device.core.roku import Roku
from homepi.device.core.roku import Key

import unittest
from unittest.mock import patch

class RokuMocks:
  def get_apps(self):
    return [('1', 'A')]

  def get_device_info(self):
    return {}

class TestRokuDevice(unittest.TestCase):

  def get_roku(self):
    r = Roku('192.168.1.1')
    r.initialize()
    return r

  @patch('homepi.device.core.roku.Roku.get_apps', new=RokuMocks.get_apps)
  @patch('homepi.device.core.roku.Roku.get_device_info', new=RokuMocks.get_device_info)
  def test_base_url(self):
    r = self.get_roku()
    self.assertEqual(r.get_base_url(), 'http://192.168.1.1:8060')

  @patch('homepi.device.core.roku.Roku.get_apps', new=RokuMocks.get_apps)
  @patch('homepi.device.core.roku.Roku.get_device_info', new=RokuMocks.get_device_info)
  def test_keypress_path(self):
    r = self.get_roku()
    self.assertEqual(r.get_keypress_path(Key.HOME), '/keypress/Home')

  @patch('homepi.device.core.roku.Roku.get_apps', new=RokuMocks.get_apps)
  @patch('homepi.device.core.roku.Roku.get_device_info', new=RokuMocks.get_device_info)
  def test_apps(self):
    r = self.get_roku()
    self.assertTrue('A' in r.apps_dict)




if __name__ == '__main__':
    unittest.main()