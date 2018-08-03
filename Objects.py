class Point:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value

    def equals(self, point):
        return self.x == point.x and self.y == point.y

    def distanceFrom(self, point):
        if point.equals(self): 
            return 10000 # High so that it is not considered near, should avoid some duplicates

        return max(abs(self.x - point.x), abs(self.y - point.y))

class Cluster:
    def __init__(self):
        self.points = []

    def addPoint(self, point):
        self.points.append(point)

    def maxValue(self):
        return max(map(lambda point: point.value, self.points))

    def output(self):
        if 0 == len(self.points):
            
            return ''
    
        xPoints = list(map(lambda point: point.x, self.points))
        yPoints = list(map(lambda point: point.y, self.points))

        xAverage = int(sum(xPoints) / len(xPoints))
        yAverage = int(sum(yPoints) / len(yPoints))

        return {
            'x': xAverage,
            'y': yAverage,
            'radius': max(
                max(map(lambda x: abs(xAverage - x), xPoints)),
                max(map(lambda y: abs(yAverage - y), yPoints))
            ) + 1,
            'maxValue': self.maxValue()
        }

    def toString(self):
        dictionary = self.output()
        return '[x:' + str(dictionary['x']) + ',y:' + str(dictionary['y']) + ',radius:' + str(dictionary['radius']) + ',maxValue:' + str(dictionary['maxValue']) + ']'


class SerialClass:
    def getSerial(self, name, baudRate):
        ports = list(port_list.comports())
        for port_no, description, address in ports:
            print(port_no)
            print(description)
            print(address)

            if name in description:
                serial.Serial(port_no, baudRate)