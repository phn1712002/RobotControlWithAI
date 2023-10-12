# Interfaces
class ElectronicComponents:
    def __init__(self, 
                 name=None,
                 board=None,
                 pin=0,
                 voltage=[0,0],
                 amperage=[0,0], 
                 wattage=[0,0], 
                 frequency=[0,0],
                 temperature=[0,0]
                 ):
        self.name = name
        self.board = board
        self.pin = pin
        self.voltage = voltage
        self.amperage = amperage
        self.wattage = wattage
        self.frequency = frequency
        self.temperature = temperature

class MechanicalComponents:
    def __init__(self, 
                 name=None, 
                 material=None):
        self.name = name
        self.material = material