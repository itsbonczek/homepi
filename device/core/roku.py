import requests
import time
import xml.etree.ElementTree as ET

import sys

from wakeonlan import send_magic_packet

class Key:
    HOME = 'Home'
    REV = 'Rev'
    FWD = 'Fwd'
    PLAY = 'Play'
    SELECT = 'Select'
    LEFT = 'Left'
    RIGHT = 'Right'
    DOWN = 'Down'
    UP = 'Up'
    BACK = 'Back'
    INSTANT_REPLAY = 'InstantReplay'
    INFO = 'Info'
    BACKSPACE = 'Backspace'
    SEARCH = 'Search'
    ENTER = 'Enter'
    POWER_OFF = 'PowerOff'
    POWER_ON = 'PowerOn'
    FIND_REMOTE = 'FindRemote'
        

class Roku:
    'Roku IP control'
    
    ROKU_PORT = 8060

    ip_address = None
    # app ids keyed by name
    apps_dict = {}
    device_info_dict = {}

    def __init__(self, ip_address):
        self.ip_address = ip_address
      
    # Initiatlization - loads apps and device info

    def initialize(self):
        self.load_apps()
        self.device_info_dict = self.get_device_info()

    # Apps    
    
    def load_apps(self):
        apps = self.get_apps()

        self.apps_dict = {}
        for app in apps:
            self.apps_dict[app[1]] = app[0]

    def get_apps(self):
        response = self.do_request('GET', '/query/apps')
        root = ET.fromstring(response)
        return map(lambda app_element: (app_element.attrib['id'], app_element.text), root)

    def navigate_to_app(self, app_name):
        if app_name in self.apps_dict:
            app_id = self.apps_dict[app_name]
            self.do_command('POST', self.get_launch_app_path(app_id), True)

    def get_launch_app_path(self, app_id):
        return '/launch/' + app_id

    
    # Key Press
    
    def do_keypress(self, key):
        self.do_command('POST', self.get_keypress_path(key))

    def get_keypress_path(self, key):
        return '/keypress/' + key

    # Device Info
    def get_device_info(self):
        response = self.do_command('GET', '/query/device-info')
        root = ET.fromstring(response)

        device_info_dict = {}
        for elem in root:
            device_info_dict[elem.tag] = elem.text

        return device_info_dict

    # WOL

    def get_mac_address(self):
        return self.device_info_dict['ethernet-mac']

    def wake(self):
        send_magic_packet(self.get_mac_address(), ip_address=self.ip_address)
   
    # Helpers

    def do_command(self, method, path, wake=False):
        if wake:
            self.wake()
            time.sleep(1)

        return self.do_request(method, path)

    def do_request(self, method, path):
        url = self.get_base_url() + path
        r = requests.request(method, url)
        return r.text.encode('utf-8')

    def get_base_url(self):
        return 'http://' + self.ip_address + ':' + str(self.ROKU_PORT)





