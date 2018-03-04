import atexit
import json
import os
import time

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

import sys
import os
sys.path.append(os.path.abspath(__file__ + '/../../../'))

from homepi.device.alexa.handler import AlexaRequestHandler
from homepi.device.alexa.roku import AlexaRokuController
from homepi.device.alexa.videogames import VideoGamesSceneController
from homepi.device.core.roku import Roku

myMQTTClient = None
requestHandler = None

def dosend(client, userdata, message):
    global requestHandler
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")

    request = json.loads(message.payload)
    requestHandler.handle_request(request)

def configure():
    global requestHandler
    roku = Roku(os.environ['HOMEPI_ROKU_IP_ADDRESS'])
    roku.initialize()
    roku_controller = AlexaRokuController(roku)
    video_games_scene_controller = VideoGamesSceneController(roku)

    controllers = {
        'appliance-001' : roku_controller
    }

    scene_handlers = [roku_controller, video_games_scene_controller]

    for controller in scene_handlers:
        for scene_id in controller.get_scene_ids():
            controllers[scene_id] = controller

    requestHandler = AlexaRequestHandler(controllers)

def connect():
    global myMQTTClient
    myMQTTClient = AWSIoTMQTTClient('homepi')
    myMQTTClient.configureEndpoint(os.environ['HOMEPI_IOT_ENDPOINT'], 8883)
    myMQTTClient.configureCredentials(os.environ['HOMEPI_ROOT_CA_PATH'], os.environ['HOMEPI_PRIVATE_KEY_PATH'], os.environ['HOMEPI_CERT_PATH'])
    myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
    myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
    myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
    myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
    atexit.register(onexit)
    myMQTTClient.connect()
    myMQTTClient.subscribe("sendcommand", 1, dosend)
    time.sleep(2)

def wait():
    while True:
        time.sleep(1)

def testpublish():
    global myMQTTClient
    # Publish to the same topic in a loop forever
    loopCount = 0
    while True:
        message = {}
        message['endpoint'] = 'device-01'
        message['command'] = 'PowerOn'
        messageJson = json.dumps(message)
        myMQTTClient.publish("sendcommand", messageJson, 1)
        print('Published topic %s: %s\n' % ("sendcommand", messageJson))
        loopCount += 1
        time.sleep(5)


def onexit():
  global myMQTTClient
  myMQTTClient.unsubscribe("sendcommand")
  myMQTTClient.disconnect()

if __name__ == '__main__':
  configure()
  connect()
  wait()
