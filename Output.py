# -*- coding: utf-8 -*-
import pygame.mixer

from Objects import Cluster

class OutputMixSamples:
    def __init__(self, samples, dim):
        self.dim = dim

        self.channels = []
        pygame.mixer.init()
        for index, sample in enumerate(samples):
            channel = pygame.mixer.find_channel()
            channel.set_volume(0)
            channel.play(pygame.mixer.Sound(sample), -1)
            self.channels.append(channel)
        
    def playSoundForCluster(self, cluster):
        if False == isinstance(cluster, Cluster):
            return

        output = cluster.output()
        self.setVolumes(self.calculateVolumes(
            output['x'],
            output['y']
        ))

    def calculateVolumes(self, x, y):
        xNeg = self.dim + x
        yNeg = self.dim + y
        xPos = self.dim - x
        yPos = self.dim - y
        max = (8 * self.dim**2)**(1/2)
        return [
            (xPos**2 + yPos**2)**(1/2) / max,
            (xNeg**2 + yPos**2)**(1/2) / max,
            (xPos**2 + yNeg**2)**(1/2) / max,
            (xNeg**2 + yNeg**2)**(1/2) / max
        ]
        
    def setVolumes(self, volumes):
        print(volumes)

        for index, channel in enumerate(self.channels):
            channel.set_volume(volumes[index])

MyOutput = OutputMixSamples([], 8)
print(MyOutput.calculateVolumes(-8,-8))
print(MyOutput.calculateVolumes(0, 0))
print(MyOutput.calculateVolumes(-8,8))
print(MyOutput.calculateVolumes(8,-8))
print(MyOutput.calculateVolumes(8,8))