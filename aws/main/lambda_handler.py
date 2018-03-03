# -*- coding: utf-8 -*-

# Copyright 2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Amazon Software License (the "License"). You may not use this file except in
# compliance with the License. A copy of the License is located at
#
#    http://aws.amazon.com/asl/
#
# or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, express or implied. See the License for the specific
# language governing permissions and limitations under the License.

"""Alexa Smart Home Lambda Function Sample Code.

This file demonstrates some key concepts when migrating an existing Smart Home skill Lambda to
v3, including recommendations on how to transfer endpoint/appliance objects, how v2 and vNext
handlers can be used together, and how to validate your v3 responses using the new Validation
Schema.

Note that this example does not deal with user authentication, only uses virtual devices, omits
a lot of implementation and error handling to keep the code simple and focused.
"""

import boto3
import json
import logging
import time
import uuid


# Setup logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(request, context):
    try:
        logger.info("Directive:")
        logger.info(json.dumps(request, indent=4, sort_keys=True))
        
        logger.info("Received v3 directive!")
        if request["directive"]["header"]["name"] == "Discover":
            response = handle_discovery_v3(request)
        else:
            response = handle_non_discovery_v3(request)

        logger.info("Response:")
        logger.info(json.dumps(response, indent=4, sort_keys=True))

        return response
    except ValueError as error:
        logger.error(error)
        raise

def get_utc_timestamp(seconds=None):
    return time.strftime("%Y-%m-%dT%H:%M:%S.00Z", time.gmtime(seconds))

def get_uuid():
    return str(uuid.uuid4())

def get_endpoints():
    return [
        {
            'endpointId': 'appliance-001',
            'friendlyName': 'TV',
            'description': 'Living Room TV',
            'manufacturerName': 'TCL',
            'displayCategories': ['TV'],
            'cookie': {},
            'capabilities': [
                {
                    'type': 'AlexaInterface',
                    'interface': 'Alexa.PowerController',
                    'version': "3"
                },
                {
                    'type': 'AlexaInterface',
                    'interface': 'Alexa.PlaybackController',
                    'version': "3",
                    "supportedOperations" : ["Play", "Pause", "Stop"]
                },
                {
                    'type': 'AlexaInterface',
                    'interface': 'Alexa.InputController',
                    'version': "3",
                }
            ]   
        },
        {
            'endpointId': 'watch-tv-scene',
            'friendlyName': 'Watch TV',
            'description': 'Turns on the Living Room TV',
            'manufacturerName': 'TCL',
            'displayCategories': ['SCENE_TRIGGER'],
            'cookie': {},
            'capabilities': [
                {
                    'type': 'AlexaInterface',
                    'interface': 'Alexa.SceneController',
                    'version': "3"
                },
            ]   
        }

    ]

def get_topic(topic_name):
    return '$aws/things/homepi/' + topic_name
  

# v3 handlers
def handle_discovery_v3(request):
  
    response = {
        "event": {
            "header": {
                "namespace": "Alexa.Discovery",
                "name": "Discover.Response",
                "payloadVersion": "3",
                "messageId": get_uuid()
            },
            "payload": {
                "endpoints": get_endpoints()
            }
        }
    }
    return response

def handle_non_discovery_v3(request):
    
    request_namespace = request["directive"]["header"]["namespace"]
    request_name = request["directive"]["header"]["name"]

    # for now, forward all requests to the pi
    iot_client = boto3.client('iot-data', region_name='us-east-1')
    iot_client.publish(topic ='sendcommand', qos=1, payload = json.dumps(request))
   
    if request_namespace == "Alexa.PowerController":
        return handle_power_request(request)
    elif request_namespace == "Alexa.PlaybackController":
        return handle_playback_request(request)
    elif request_namespace == "Alexa.InputController":
        return handle_input_request(request)
    elif request_namespace == "Alexa.SceneController":
        return handle_scene_request(request)
    elif request_namespace == "Alexa.Authorization":
        if request_name == "AcceptGrant":
            response = {
                "event": {
                    "header": {
                        "namespace": "Alexa.Authorization",
                        "name": "AcceptGrant.Response",
                        "payloadVersion": "3",
                        "messageId": "5f8a426e-01e4-4cc9-8b79-65f8bd0fd8a4"
                    },
                    "payload": {}
                }
            }
            return response

    # other handlers omitted in this example

def handle_power_request(request):

    request_name = request["directive"]["header"]["name"]
    
    if request_name == "TurnOn":
        value = "ON"
    else:
        value = "OFF"

    response = {
        "context": {
            "properties": [
                {
                    "namespace": "Alexa.PowerController",
                    "name": "powerState",
                    "value": value,
                    "timeOfSample": get_utc_timestamp(),
                    "uncertaintyInMilliseconds": 500
                }
            ]
        },
        "event": {
            "header": {
                "namespace": "Alexa",
                "name": "Response",
                "payloadVersion": "3",
                "messageId": get_uuid(),
                "correlationToken": request["directive"]["header"]["correlationToken"]
            },
            "endpoint": {
                "scope": {
                    "type": "BearerToken",
                    "token": "access-token-from-Amazon"
                },
                "endpointId": request["directive"]["endpoint"]["endpointId"]
            },
            "payload": {}
        }
    }
    
    return response

def handle_playback_request(request):
    response = {
        "context": {
            "properties": []
        },
        "event": {
            "header": {
                "namespace": "Alexa",
                "name": "Response",
                "payloadVersion": "3",
                "messageId": get_uuid(),
            },
            "endpoint": {
                "endpointId": request["directive"]["endpoint"]["endpointId"]
            },
            "payload": {}
        }
    }

    return response    

def handle_input_request(request):
    
    value = request["directive"]["payload"]["input"]

    response = {
        "context": {
            "properties": [
                {
                    "namespace": "Alexa.InputController",
                    "name": "input",
                    "value": value,
                    "timeOfSample": get_utc_timestamp(),
                    "uncertaintyInMilliseconds": 500
                }
            ]
        },
        "event": {
            "header": {
                "namespace": "Alexa",
                "name": "Response",
                "payloadVersion": "3",
                "messageId": get_uuid(),
            },
            "endpoint": {
                "endpointId": request["directive"]["endpoint"]["endpointId"]
            },
            "payload": {}
        }
    }

    return response

def handle_scene_request(request):
    
    response = {
        "context": {
        },
        "event": {
            "header": {
                "namespace": "Alexa.SceneController",
                "name": "ActivationStarted",
                "payloadVersion": "3",
                "messageId": get_uuid(),
                "correlationToken": request["directive"]["header"]["correlationToken"]
            },
            "endpoint": {
                "endpointId": request["directive"]["endpoint"]["endpointId"]
            },
            "payload": {
                "cause": {
                    "type": "VOICE_INTERACTION"
                },
                "timestamp": get_utc_timestamp()
            }
        }
    }

    return response  


def get_directive_version(request):
    try:
        return request["directive"]["header"]["payloadVersion"]
    except:
        try:
            return request["header"]["payloadVersion"]
        except:
            return "-1"

