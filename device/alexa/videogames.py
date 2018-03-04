from .base import AlexaPowerController, AlexaPlaybackController, AlexaInputController, AlexaSceneController

import time

import os
import sys
sys.path.append(os.path.abspath(__file__ + '/../../../../'))

from homepi.device.core.roku import Key

class VideoGamesSceneController(AlexaSceneController):

  roku_device = None

  PLAY_VIDEO_GAMES_SCENE_ID = 'play-video-games-scene'

  def __init__(self, roku_device):
    self.roku_device = roku_device

  def activateScene(self, endpoint_id):
    self.roku_device.wake()
    time.sleep(1)
    self.roku_device.do_keypress(Key.POWER_ON)
    time.sleep(1)
    self.roku_device.navigate_to_app('HDMI\xa02')

  def get_scene_ids(self):
    return [self.PLAY_VIDEO_GAMES_SCENE_ID]


