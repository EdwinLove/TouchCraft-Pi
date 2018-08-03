# -*- coding: utf-8 -*-
import pygame.mixer

from Objects import Cluster

class OutputMixSamples:
    def __init__(self, samples, dim):
        self.dim = dim

        self.channels = []
        self.loudestMultiplier = 3
        pygame.mixer.init()
        for index, sample in enumerate(samples):
            channel = pygame.mixer.find_channel()
            channel.set_volume(0)
            channel.play(pygame.mixer.Sound(sample), -1)
            self.channels.append(channel)
        
    def outputCluster(self, cluster):
        if False == isinstance(cluster, Cluster):
            self.setVolumes([0, 0, 0, 0])
            return

        output = cluster.output()
        self.setVolumes(self.calculateVolumes(
            output['x'],
            output['y']
        ))

    def calculateVolumes(self, x, y):
        xNeg = self.dim - x
        yNeg = self.dim - y
        maximum = (2 * self.dim**2)**(1/2)
        A = ( maximum - (x**2    + y**2   )**(1/2) ) / maximum
        B = ( maximum - (xNeg**2 + y**2   )**(1/2) ) / maximum
        C = ( maximum - (x**2    + yNeg**2)**(1/2) ) / maximum
        D = ( maximum - (xNeg**2 + yNeg**2)**(1/2) ) / maximum
        print(A)
        print(B)
        print(C)
        print(D)
        loudest = max(A, B, C, D)
        if A == loudest:
            A *= self.loudestMultiplier
        if B == loudest:
            B *= self.loudestMultiplier
        if C == loudest:
            C *= self.loudestMultiplier
        if D == loudest:
            D *= self.loudestMultiplier

        return [
            A / self.loudestMultiplier,
            B / self.loudestMultiplier,
            C / self.loudestMultiplier,
            D / self.loudestMultiplier
        ]
        
    def setVolumes(self, volumes):
#        print ('@@')
        print(volumes)
#        print ('@@')
        
        for index, channel in enumerate(self.channels):
            channel.set_volume(volumes[index])

# class OutputLedMatrix(SerialClass):
#     def __init__(self, dim):
#         self.dim = dim
#         self.ser = self.getSerial('USB-SERIAL', 230400)   

#     def outputCluster(self, cluster):
#         if False == isinstance(cluster, Cluster):
#             return

#         self.printToSerial(self.generateMatrix(cluster))

#     def printToSerial(self, matrix):
#         self.ser.write(matrix)
    
#     def generateMatrix(self, cluster):
#         matrix = []
#         while y < self.dim:
#             line = []
#             while x < self.dim:
#                 line.append(self.getValue(x, y, cluster))
#             matrix.append(line)

#         return matrix

#     def getValue(self, x, y, cluster):
#         output = cluster.output()
#         dist = ( (x - output['x'])**2 + (y - output['y'])**2 )**(1/2)
#         if dist > output['radius']:
#             return 0

#         maxMultiplier = output['radius'] + 1

#         return  output['maxValue'] * ( (maxMultiplier - dist) / maxMultiplier )


# MyOutput = OutputMixSamples([], 8)
# print(MyOutput.calculateVolumes(-8,-8))
# print(MyOutput.calculateVolumes(0, 0))
# print(MyOutput.calculateVolumes(-8,8))
# print(MyOutput.calculateVolumes(8,-8))
# print(MyOutput.calculateVolumes(8,8))