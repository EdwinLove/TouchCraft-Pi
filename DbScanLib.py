# -*- coding: utf-8 -*-
import Input
# import Output
from dbscan.dbscan import MyDBSCAN
import time
# import pygame.mixer

from pythonosc import osc_message_builder
from pythonosc import osc_bundle_builder
from pythonosc import udp_client

from Objects import Point
from Objects import Cluster

from math import sqrt

from statistics import median

ip = '127.0.0.1'
port = 8833

client = udp_client.SimpleUDPClient(ip, port)


class DbScanLib:

    pressures_prev = []
    deltas = []
    deltasY = []
    deltasX = []
    init = False

    def __init__(self, input, outputs = []):
        self.Input  = input
        self.outputs  = outputs

    def convertToClusters(self, points):
        clusters = {}
        count = 0
        for index, clusterNum in enumerate(MyDBSCAN(points, 1.5, 3)): # 1.5,3
            if clusterNum == -1:
                continue
            if False == clusters.get(clusterNum, False):
                # print ('Create cluster '+ str(clusterNum))
                clusters[clusterNum] = Cluster()
            point = points[index]
            #print ('Add '+ str(point[0]) + ', ' + str(point[1]) + ', ' + str(point[2]) + ' to ' + str(clusterNum) )
            clusters.get(clusterNum).addPoint(Point(point[0], point[1], point[2]))
            count+=1
            
        #print("num points: " + str(len(points)))
        #print("num clusters: " + str(len(clusters)))


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
            clusters = self.filterClusters(self.convertToClusters(self.Input.getCoords()), 0)
            outputString = ''
            if 0 == len(clusters):
                outputString = self.output(False)
            else:
                for cluster in clusters:
                    outputString += self.output(cluster) +'; '

            if '' != outputString:
                print(outputString)
    
    def sendList(list):
        bundle = osc_bundle_builder.OscBundleBuilder(osc_bundle_builder.IMMEDIATELY)
        msg = osc_message_builder.OscMessageBuilder(address="/cluster")
        for value in list:
            msg.add_arg(value)
            bundle.add_content(msg.build())
        client.send(bundle)

    def cluster(self): #CH
        points = self.Input.getCoords()
        totalPressure = 0
        
        p1 = []
        p2 = []
        pressures = []
        
        count = 0

        for p in points:
            totalPressure = totalPressure + p[2]
            if(count<=127):
                p1.append(p[2])
            else:
                p2.append(p[2])
            if(count%16 == 0):
                pressures.append([])
            pressures[-1].append(p[2])
            count += 1

        if(not self.init):
            self.pressures_prev = pressures[:]
            self.deltas = pressures[:]
            self.deltasX = pressures[:]
            self.deltasY = pressures[:]
            self.init = True

        totalX = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        totalY = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        maxvalX = 0.00001 # avoid div by zero
        maxvalY = 0.00001
        for x,line in enumerate(pressures):
            for y,v in enumerate(line):
                totalX[x] = totalX[x] + v
                if(v>maxvalX):
                    maxvalX = v
        
        pressure_areas = [0,0,0,0,0]
        i=0
        for x,line in enumerate(pressures):
            for y,v in enumerate(line):
                if(x<8):
                    if(y<8): # top left
                        i = 0
                    else : # bottom left
                        i = 3
                else:
                    if(y<8): # top right
                        i = 1
                    else : # bottom right
                        i = 2
                if(sqrt((x-8)**2 + (y-8)**2)<4): # centre circle (rad 4)
                    i = 4
                pressure_areas[i] = pressure_areas[i] + v

        for y,line in enumerate(pressures):
            for v in line:
                totalY[y] = totalX[y] + v
                if(v>maxvalY):
                    maxvalY = v

        centreX = 0
        centreY = 0
        for i,v in enumerate(totalX):
            centreX = centreX + i*(v/maxvalX)
        for i,v in enumerate(totalY):
            centreY = centreY + i*(v/maxvalY)
        centreX /= 16
        centreY /= 16

        # client.send_message("/raw1", p1)
        # client.send_message("/raw2", p2)
        client.send_message("/totalPressure", totalPressure)
        client.send_message("/cx", centreX)
        client.send_message("/cy", centreY)
        client.send_message("/maxpressure", max(maxvalX,maxvalY))
        client.send_message("/areas", pressure_areas)

        #clusters = self.convertToClusters(points)
        #clusters = self.filterClusters(self.convertToClusters(points), 0) # number of clusters
        # if len(clusters) > 0:
        #     for i,c in enumerate(clusters):
        #         clusterData = clusters.get(c).outputList()
        #         # # sendList(clusterData)
        #         # bundle = osc_bundle_builder.OscBundleBuilder(osc_bundle_builder.IMMEDIATELY)
        #         # msg = osc_message_builder.OscMessageBuilder(address="/cluster")
        #         # for value in clusterData:
        #         #     msg.add_arg(value)
        #         # bundle.add_content(msg.build())
        #         # bundle = bundle.build()
        #         # client.send(bundle)
        #         clusterData = [c] + clusterData
        #         client.send_message("/all", clusterData)

        #         # client.send_message("/x",clusterData[0])
        #         # client.send_message("/y",clusterData[1])
        #         # client.send_message("/radius",clusterData[2])
        #         # client.send_message("/max",clusterData[3])

        #         # print(cluster.outputList())

    def clusterFake(self, inputArray):
        self.Input.setInput(inputArray)
        clusters = self.filterClusters(self.convertToClusters(self.Input.getCoords()))
        if len(clusters) > 0:
            for cluster in clusters:
                print(cluster.output())

#            time.sleep(0.2)
    
Input = Input.InputFromSerial(16)
#Input = Input.TestInput(16)
#Input = Input.SimulatedInput()
# Input = Input.PassedInput()
# Output = Output.OutputMixSamples([
#     'sounds/birdsong.wav',
#     'sounds/bowls.wav',
#     'sounds/harp.wav',
#     'sounds/soul-clap.wav.wav'
# ], 16)

MyDbScanLib = DbScanLib(Input, [])
while True:
    MyDbScanLib.cluster()
