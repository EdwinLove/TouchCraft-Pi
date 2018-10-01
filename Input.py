import serial
import serial.tools.list_ports as port_list
from Objects import Point
import sys

class AbstractInput():
    def __init__(self, dim):
        self.dim = dim
        self.touchThreshold = 10  # 10

    def getPoints(self): 
        points = {}
        for y, line in enumerate(self.getPointsSet()):
            for x, value in enumerate(line):
                if value > self.touchThreshold:
                    points[str(x) + ':' + str(y)] = Point(x, y, value)

        return points

    def getCoords(self):
        coords = []
        for y, line in enumerate(self.getPointsSet()):
            print(line) #CH
            for x, value in enumerate(line): #CH
                #if value > self.touchThreshold:
                coords.append([x, y, value])
        print("########") #CH
        return coords


class InputFromSerial(AbstractInput):
    def __init__(self, dim):
        AbstractInput.__init__(self, dim)
        self.ser = self.getSerial('USB-SERIAL', 230400)

    def getSerial(self, name, baudRate):
        ports = list(port_list.comports())
        for port_no, description, address in ports:
            print(port_no)
            print(description)
            print(address)

            if name in description:
                return serial.Serial(port_no, baudRate)

    def getPointsSet(self):
        lines = []
        while True:
            line = self.ser.readline() ###################################
            sys.stdout.flush()
#             print(list(line))
#             newLine = list(filter(lambda x: x < 100, list(line)))
#             print(newLine)
# #            print(b''.join(newLine))
#             #line = line.encode("windows-1252")
#             #line = line.encode('utf-8').strip()
#             print(line.decode('utf-8', 'ignore'))

            line = line.decode('utf-8', 'ignore').rstrip(';\r\n')
            # line = self.ser.readline().decode().rstrip(';\r\n')
            if '.' == line:
                if len(lines) == self.dim:
                    return lines
                lines = []
            else:
                thisLine = []
                for x, point in enumerate(line.split(',')):
                    try:
                        thisLine.append(self.cleanPoint(point))
                    except ValueError:
                        print('ooops')

                if len(thisLine) == self.dim:
                    lines.append(thisLine)

    def cleanPoint(self, point):
        if (False == isinstance(point, str)):
            return 0
        clean = point.rstrip(';\r\n')
        if ';' in clean:
            clean = clean.split(';', 1)[0]
        if '.' in clean:
            clean = clean.split('.', 1)[0]
        if '' == clean or '.' == clean:
            return 0
        
        return int(clean)

class SimulatedInput(AbstractInput):
    def getPointsSet(self):
        return [
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

class TestInput(AbstractInput):
    def __init__(self, dim):
        AbstractInput.__init__(self, dim)
        self.index = 0
        self.coords = [[0,0], [2,2], [14,2], [2, 14], [14, 14], [15,15]]

    def getPointsSet(self):
        y = 0
        matrix = []
        coord = self.coords[self.index]
        while y < self.dim:
            x = 0
            line = []
            while x < self.dim:
                if coord[0] == x and coord[1] == y:
                    line.append(50)
                elif abs(coord[0] - x) < 3 and abs(coord[1] - y) < 3:
                    line.append(25)
                else:
                    line.append(0)
                x += 1
            matrix.append(line)
            y += 1

        self.index += 1

        return matrix
