import usbtmc

class Teaspoon():
    def __init__(self):
        self.spoon = usbtmc.Instrument(0x1313, 0x80f8)
    def ping(self,x, output = False):
        a = self.spoon.ask(x)
        if output:
            print(a)
        return a
    def test(self):
        self.ping("*IDN?")
    def getTemperature(self):
        t = []
        t.append(self.ping("SENS1:TEMP:DATA?"))
        t.append(self.ping("SENS3:TEMP:DATA?"))
        return t
    def getHumidity(self):
        return self.ping("SENS2:HUM:DATA?")

if __name__ == '__main__':
    print("Hello, it's me. ")
