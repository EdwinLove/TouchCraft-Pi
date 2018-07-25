import serial
import serial.tools.list_ports as port_list
from Objects import Point

class InputFromSerial:
    def __init__(self):
        self.touchThreshold = 50

        ports = list(port_list.comports())
        for port_no, description, address in ports:
            if 'USB-SERIAL' in description:
                self.ser = serial.Serial(port_no, 230400)
        

    def getPoints():
        y = 0
        points = {}
        while y < 16:
            line = self.ser.readline().decode()
            print(line)
            for x, point in enumerate(line.split(',')):
                if (False == isinstance(point, str)):
                    continue
                clean = point.rstrip(';\r\n')
                if '' == clean or '.' == clean:
                    continue
                value = int(clean)
                if value > self.touchThreshold:
                    points[str(x) + ':' + str(y)] = Point(x, y, value)
            y+=1

        return points

    def getCoords(self):
        y = 0
        points = []
        while y < 16:
            line = self.ser.readline().decode()
            print(line)
            for x, point in enumerate(line.split(',')):
                if (False == isinstance(point, str)):
                    continue
                clean = point.rstrip(';\r\n')
                if ';' in clean:
                    clean = clean.split(';', 1)[0]
                if '.' in clean:
                    clean = clean.split('.', 1)[0]
                if '' == clean or '.' == clean:
                    continue
                value = int(clean)
                if value > 10:
                    points.append([x-8, y-8, value])
            y+=1
            
        return points

    def getCoords(self):
        y = 0
        points = []
        while True:
            line = self.ser.readline().decode().rstrip(';\r\n')
            if '.' == line:
                return points
            print(line)
            for x, point in enumerate(line.split(',')):
                if (False == isinstance(point, str)):
                    continue
                clean = point.rstrip(';\r\n')
                if ';' in clean:
                    clean = clean.split(';', 1)[0]
                if '.' in clean:
                    clean = clean.split('.', 1)[0]
                if '' == clean or '.' == clean:
                    continue
                value = int(clean)
                if value > 10:
                    points.append([x-8, y-8, value])
            y+=1
            
        return points


class SimulatedInput:
    def __init__(self):
        self.input = [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 4, 4, 4, 2, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 4, 4, 4, 2, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 4, 8, 4, 2, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 3, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 9, 9, 6, 4, 2],
                [0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 7, 8, 5, 8, 3, 0],
                [0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 7, 9, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]

        self.smallInput = [
            [0, 1, 0],
            [1, 1, 1],
            [0, 1, 0]
        ]

    def getPoints(self, useSmall=False):
        notNullPoints = {}
        for y, row in enumerate(self.input):
            for x, value in enumerate(row):
                if value > 0:
                    notNullPoints[str(x) + ':' + str(y)] = Point(x, y, value)
            
        return notNullPoints

    def getCoords(self):
        points = []
        for y, row in enumerate(self.input):
            for x, value in enumerate(row):
                if value > 0:
                    points.append([x, y, value])
            
        return points