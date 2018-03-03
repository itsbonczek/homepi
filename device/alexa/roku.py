from .base import AlexaPowerController, AlexaPlaybackController, AlexaInputController, AlexaSceneController

import time

import os
import sys
sys.path.append(os.path.abspath(__file__ + '/../../../../'))

from homepi.device.core.roku import Key

class AlexaRokuController(AlexaPowerController, AlexaPlaybackController, AlexaInputController, AlexaSceneController):

  roku_device = None
  WATCH_TV_SCENE_ID = 'watch-tv-scene'

  def __init__(self, roku_device):
    self.roku_device = roku_device
  
  def turnOn(self):
    self.roku_device.wake()
    time.sleep(1)
    self.roku_device.do_keypress(Key.POWER_ON)

  def turnOff(self):
    self.roku_device.do_keypress(Key.POWER_OFF)

  def play(self):
    self.roku_device.do_keypress(Key.PLAY)

  def pause(self):
    self.roku_device.do_keypress(Key.PLAY)

  def stop(self):
    self.pause()

  def selectInput(self, input_name):
    for k, v in self.roku_device.apps_dict.items():
      if self.sanitizeInput(k) == self.sanitizeInput(input_name):
        self.roku_device.navigate_to_app(k)

  def sanitizeInput(self, input_name):
    return input_name.strip().lower()

  def get_scene_ids(self):
    return [self.WATCH_TV_SCENE_ID]

  def activateScene(self, endpoint_id):
    if endpoint_id == self.WATCH_TV_SCENE_ID:
      self.turnOn()



