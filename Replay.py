# -*- coding: utf-8 -*-
import time
import json
import argparse 
from pythonosc import osc_message_builder
from pythonosc import osc_bundle_builder
from pythonosc import udp_client
 
class Replay():
    def __init__(self, fileName, delay, ip, port):
        self.delay = delay / 1000 if delay > 0 else 0
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
            time.sleep(self.delay)

parser = argparse.ArgumentParser(description='Replay a recording.')
parser.add_argument('file', type=str, help='The name of the file to replay')
parser.add_argument('--delay', type=int, help='milliseconds delay between lines', default=500)
args = parser.parse_args()
replay = Replay(args.file, args.delay, '127.0.0.1', 8833)
replay.pushToOsc()