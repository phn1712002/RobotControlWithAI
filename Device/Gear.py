from Device.Components import MechanicalComponents

# Interfaces
class Gear(MechanicalComponents):
    def __init__(self, name=None, material=None):
        super().__init__(name, material)
        self.z = None
        self.i = None
        self.i_inverse = None
    def calcParameter(self, input, inverse): pass
    def calcGear(self, z, inverse): pass

# Class
class MultiGear(Gear):
    def __init__(self, multi_gear=None, name=None, material=None):
        super().__init__(name, material)
        self.multi_gear = multi_gear
    
    def calcParameter(self, input, inverse):
        for index_gear in self.multi_gear:
            input *= index_gear.calcParameter(input, inverse)
        return input    
        
class SpurGear(Gear):
    def __init__(self,
                     z=[1, 2], 
                     material=None, 
                     name=None):
        super().__init__(name=name, material=material)
        self.z = z
        self.i = self.calcGear(z, True)
        self.i_inverse = self.calcGear(z, False)
        
    def calcParameter(self, input, inverse=False):
        if inverse:
            return input * self.i_inverse
        else:
            return input * self.i
        
    def calcGear(self, z, inverse=False):
        i = 1
        for index in range(len(z) - 1):
            i *= z[index + 1] / z[index]
        if inverse : i = 1/i
        return i