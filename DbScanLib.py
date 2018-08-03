# -*- coding: utf-8 -*-
import Input
import Output
from dbscan.dbscan import MyDBSCAN
import time
import pygame.mixer

from Objects import Point
from Objects import Cluster

class DbScanLib:

    def __init__(self, input, outputs = []):
        self.Input  = input
        self.outputs  = outputs

    def convertToClusters(self, points):
        clusters = {}
        for index, clusterNum in enumerate(MyDBSCAN(points, 1.5, 3)):
            if clusterNum == -1:
                continue

            if False == clusters.get(clusterNum, False):
            # print ('Create cluster '+ str(clusterNum))
                clusters[clusterNum] = Cluster()
                    
            point = points[index]
            #print ('Add '+ str(point[0]) + ', ' + str(point[1]) + ', ' + str(point[2]) + ' to ' + str(clusterNum) )
            clusters.get(clusterNum).addPoint(Point(point[0], point[1], point[2]))

        return clusters

    def filterClusters(self, clusters, maxClusters = 0):
        if 0 == maxClusters:
            return clusters

        if 1 < maxClusters:
            #TODO - Fix
            sortedList = clusters # sorted(clusters.items(), key=lambda cluster: cluster[1].maxValue())
            return sortedList[:maxClusters]

        highestValueCluster = False
        highestValueClusterIndex = False
        for index, cluster in clusters.items():
            # print(index)
            # print(cluster)
            if False == highestValueCluster or highestValueCluster.maxValue() < cluster.maxValue():
                highestValueCluster = cluster
                highestValueClusterIndex = index
                # print('Yup')        

        if highestValueCluster:
            return [highestValueCluster]

        return []

    def output(self, cluster):
        for output in self.outputs:
            output.outputCluster(cluster)
            
        if (cluster):
            return cluster.toString()
            
        return 'null'

    def scan(self):
        while(True):
            clusters = self.filterClusters(self.convertToClusters(self.Input.getCoords()), 1)
            outputString = ''
            if 0 == len(clusters):
                outputString = self.output(False)
            else:
                for cluster in clusters:
                    outputString += self.output(cluster) +'; '

            if '' != outputString:
                print(outputString)

#            time.sleep(0.2)
    
Input = Input.InputFromSerial(16)
#Input = Input.TestInput(16)
#Input = Input.SimulatedInput()
Output = Output.OutputMixSamples([
    'sounds/birdsong.wav',
    'sounds/bowls.wav',
    'sounds/harp.wav',
    'sounds/soul-clap.wav.wav'
], 16)

MyDbScanLib = DbScanLib(Input, [Output])
MyDbScanLib.scan()
