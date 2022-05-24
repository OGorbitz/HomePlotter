import math

class SaeLength(object):
    def __init__(self, inches, feet=0):
        self.totalInches = inches + feet * 12

    def feet(self):
        return math.floor(self.totalInches / 12)

    def inches(self): 
        return math.floor(self.totalInches % 12)

    def sixteenths(self):
        return math.floor(self.totalInches % 1 * 16)

    def __str__(self):
        if self.totalInches <= 0:
            return "0"

        os = ""
        if self.feet() > 0:
            os += self.feet().__str__() + "'"
            if self.inches() > 0 or self.sixteenths() > 0:
                os += " "
        if self.inches() > 0:
            os += self.inches().__str__()
            if self.sixteenths() > 0: 
                os += "-"
        if self.sixteenths() > 0:
            n = self.sixteenths()
            d = 16
            while True:
                if n % 2 == 0:
                    n = int(n / 2)
                    d = int(d / 2)
                else:
                    break
            
            os += n.__str__() + "/" + d.__str__()
        if self.inches() > 0 or self.sixteenths() > 0:
            os += "\""
        return os




