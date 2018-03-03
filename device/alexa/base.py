from abc import ABC, abstractmethod

class AlexaPowerController(ABC):
  @abstractmethod
  def turnOn(self):
    pass

  @abstractmethod
  def turnOff(self):
    pass


class AlexaPlaybackController(ABC):
  @abstractmethod
  def play(self):
    pass

  @abstractmethod
  def pause(self):
    pass

  @abstractmethod
  def stop(self):
    pass


class AlexaInputController(ABC):
  @abstractmethod
  def selectInput(self, input_name):
    pass


class AlexaSceneController(ABC):
  @abstractmethod
  def activateScene(self, endpoint_id):
    pass

  @abstractmethod
  def get_scene_ids(self):
    pass