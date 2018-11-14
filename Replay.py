# -*- coding: utf-8 -*-
import time
import json
import argparse 
from pythonosc import osc_message_builder
from pythonosc import osc_bundle_builder
from pythonosc import udp_client
 
class Replay():
    def __init__(self, fileName, ip, port):
        self.file = open(fileName)
        self.client = udp_client.SimpleUDPClient(ip, port)


    def pushToOsc(self):
        while True:
            line = self.file.readline()
            try:
                parsed_json = json.loads(line)
                self.client.send_message('/totalPressure', parsed_json['/totalPressure'])
                self.client.send_message('/cx', parsed_json['/cx'])
                self.client.send_message('/cy', parsed_json['/cy'])
                self.client.send_message('/maxpressure', parsed_json['/maxpressure'])
                self.client.send_message('/areas', parsed_json['/areas'])
                print({
                    "/totalPressure": parsed_json['/totalPressure'],
                    "/cx": parsed_json['/cx'],
                    "/cy": parsed_json['/cy'],
                    "/maxpressure":parsed_json['/maxpressure'],
                    "/areas": parsed_json['/areas'],
                })
            except json.decoder.JSONDecodeError:
                quit()
            time.sleep(0.5)

parser = argparse.ArgumentParser(description='Replay a recording.')
parser.add_argument('file', type=str, help='the name of the file to replayr')
args = parser.parse_args()
replay = Replay(args.file, '127.0.0.1', 8833)
replay.pushToOsc()