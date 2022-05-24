from SaeLength import SaeLength
import math


class SaePoint(object):
    x = 0;
    y = 0;
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def lx(self) -> SaeLength:
        return SaeLength(self.x)

    def ly(self) -> SaeLength:
        return SaeLength(self.y)    

    def distance(self, point):
        return SaeLength(math.sqrt((self.x - point.x) ** 2 + (self.y - point.y) ** 2))

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def encode(self):
        return self.__dict__