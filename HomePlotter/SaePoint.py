from SaeLength import SaeLength
import math

# Specifies a point containing values x,y representing inches
class SaePoint(object):
    x = 0;
    y = 0;
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # Return X component as an SaeLength object
    def lx(self) -> SaeLength:
        return SaeLength(self.x)

    # Return Y Component as an SaeLength object
    def ly(self) -> SaeLength:
        return SaeLength(self.y)    

    # Return the distance to another specified point, in inches
    def distance(self, point):
        return SaeLength(math.sqrt((self.x - point.x) ** 2 + (self.y - point.y) ** 2))

    # Returns instance as json for serialization
    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    # Necessary for serialization to work
    def encode(self):
        return self.__dict__