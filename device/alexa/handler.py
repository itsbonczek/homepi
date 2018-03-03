
from .base import AlexaPowerController, AlexaPlaybackController, AlexaInputController, AlexaSceneController

class AlexaRequestHandler():

  controllers = {}

  def __init__(self, controllers):
    self.controllers = controllers

  # handles an alexa smart home request
  # example: https://developer.amazon.com/docs/device-apis/alexa-powercontroller.html
  def handle_request(self, request):
    endpoint_id = self.get_endpoint_id(request)

    if endpoint_id not in self.controllers:
      return 
    
    controller = self.controllers[endpoint_id]
    namespace = self.get_namespace(request)
    request_name = self.get_request_name(request)

    if namespace == 'Alexa.PowerController':
      self.handle_power_controller_request(controller, request_name)
    elif namespace == 'Alexa.PlaybackController':
      self.handle_playback_controller_request(controller, request_name)
    elif namespace == 'Alexa.InputController':
      self.handle_input_request(controller, request_name, self.get_payload(request))
    elif namespace == 'Alexa.SceneController':
      self.handle_scene_request(controller, request_name, endpoint_id)


  def handle_power_controller_request(self, controller, request_name):
    if isinstance(controller, AlexaPowerController):
      if request_name == 'TurnOn':
        controller.turnOn()
      elif request_name == 'TurnOff':
        controller.turnOff()

  def handle_playback_controller_request(self, controller, request_name):
    if isinstance(controller, AlexaPlaybackController):
      if request_name == 'Play':
        controller.play()
      elif request_name == 'Pause':
        controller.pause()
      elif request_name == 'Stop':
        controller.stop()

  def handle_input_request(self, controller, request_name, payload):
    if isinstance(controller, AlexaInputController):
      if request_name == 'SelectInput':
        input_name = payload['input']
        controller.selectInput(input_name)

  def handle_scene_request(self, controller, request_name, endpoint_id):
    if isinstance(controller, AlexaSceneController):
      if request_name == 'Activate':
        controller.activateScene(endpoint_id)
      
  def get_endpoint_id(self, request):
    return request['directive']['endpoint']['endpointId']

  def get_namespace(self, request):
    return request['directive']['header']['namespace']    

  def get_request_name(self, request):
    return request['directive']['header']['name'] 

  def get_payload(self, request):
    return request['directive']['payload']   


